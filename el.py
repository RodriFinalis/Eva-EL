import streamlit as st
import os
from time import sleep
from datetime import datetime
from utils.pdf import leer_pdfs, crear_chunks
from utils.gpt import process_chunks, consolidate_with_gpt
from utils.airtable import create_airtable_record
from utils.config import UPLOAD_FOLDER
from utils.data import prepare_consolidated_data
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
AUTHENTICATION_PASSWORD = os.getenv("AUTHENTICATION_PASSWORD")

# Configuración inicial
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Autenticación
def authenticate():
    st.title("Authentication Required")
    password = st.text_input("Enter Password", type="password")
    if password == AUTHENTICATION_PASSWORD:
        st.success("Authenticated successfully!")
        return True
    elif password:
        st.error("Incorrect password. Please try again.")
    return False

if authenticate():
    # Subir un archivo PDF
    uploaded_file = st.file_uploader("Upload an EL", type=["pdf"])

    if uploaded_file:
        # Limpiar `st.session_state` si se carga un nuevo archivo
        if "current_file" in st.session_state and st.session_state["current_file"] != uploaded_file.name:
            st.session_state.clear()

        # Guardar el nombre del archivo en `st.session_state` para comparar en el futuro
        st.session_state["current_file"] = uploaded_file.name

        # Guardar el archivo en el directorio temporal
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.write(f"EL Loaded: {uploaded_file.name}")

        # Inicializar barra de progreso
        progress_bar = st.progress(0)

        # Procesar el archivo si no hay datos consolidados previos
        if "consolidated_data" not in st.session_state:
            progress_bar.progress(10)  # Carga del archivo
            textos_pdfs = leer_pdfs(UPLOAD_FOLDER)

            progress_bar.progress(30)  # Extracción de texto
            chunks_por_pdf = {filename: crear_chunks(texto) for filename, texto in textos_pdfs.items()}

            progress_bar.progress(50)  # Creación de chunks
            resultados_por_pdf, logs = process_chunks(chunks_por_pdf)

            progress_bar.progress(70)  # Procesamiento con GPT
            prepared_data = prepare_consolidated_data(resultados_por_pdf)
            consolidated_data = consolidate_with_gpt(prepared_data)

            progress_bar.progress(90)  # Consolidación de datos
            st.session_state["consolidated_data"] = consolidated_data
            st.session_state["logs"] = logs

            progress_bar.progress(100)  # Finalización
        else:
            consolidated_data = st.session_state["consolidated_data"]
            logs = st.session_state["logs"]

        # Crear un formulario editable para los datos consolidados
        st.write("Data (Edit if necessary):")

        updated_data = {}

        # Generar el formulario dinámicamente (excluir Summary)
        with st.form(key="edit_form"):
            for key, value in consolidated_data.items():
                if key != "Summary":  # Excluir el campo Summary del formulario
                    if isinstance(value, list):
                        value = ", ".join(value)  # Convertir listas a cadenas para edición
                    updated_data[key] = st.text_input(key, value=str(value) if value else "Not specified")
            
            # Botón para guardar el formulario
            submit_button = st.form_submit_button(label="Save Data")

        # Si se presiona el botón, enviar los datos a Airtable
        if submit_button:
            # Agregar el campo Summary al payload sin modificarlo
            if "Summary" in consolidated_data:
                updated_data["Summary"] = consolidated_data["Summary"]

            # Crear registro en Airtable
            create_airtable_record(updated_data, logs="; ".join(logs))
            st.toast("Successfully Saved Data🥳", icon="✅")

            # Eliminar el archivo PDF después de guardar los datos
            if os.path.exists(file_path):
                os.remove(file_path)
                st.write(f"The file '{uploaded_file.name}' has been deleted.")
