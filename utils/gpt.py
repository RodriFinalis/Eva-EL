import json
import re
import requests
from utils.config import OPENAI_API_KEY, OPENAI_ENDPOINT, GPT_HEADERS

def consultar_gpt(text):
    extraction_prompt = f"""
    Extract the following data from the provided Engagement Letter. The response must be in JSON format with the specified fields. If a field is not explicitly stated in the document, return "Not specified". Ensure all values are correctly formatted (e.g., dates, numbers, percentages, etc.).

    The fields to extract are:

    1. "Banker or Advisor": Extract the name of the Banker or Advisor as explicitly stated in the document.
    2. "Date": Extract the date of the Engagement Letter (use to be at the beginning).
    3. "Address": Extract the address mentioned in the Engagement Letter (use to be at the beginning).
    4. "Engaged Customer/Client": Extract the name of the engaged client or customer.
    5. "Engaged Customer/Client registration location": Extract the registration location (country or jurisdiction) of the client or customer.
    6. "Engaged customer Legal Name": Extract the legal name of the engaged customer, if explicitly mentioned.
    7. "Exclusivity?": Determine if the document specifies exclusivity. Return "Yes" or "No" and provide the relevant section if applicable.
    8. "Type of Service to be provided by Bank": Extract the types of services offered by the bank (e.g., Financial advisory, Investment banking services).
    9. "Services to be provided by Bank": Provide a detailed description of the services to be performed by the bank as stated in the document.
    10. "Retainer?": Indicate whether a retainer is mentioned in the document. Return "Yes" or "No."
    11. "Retainer credited against Transaction Fee?": Indicate if the retainer is credited towards the transaction fee. Return "Yes" or "No."
    12. "Success Fee?": Determine if a success fee is mentioned. Return "Yes" or "No."
    13. "Success Fee Amount": If a Success Fee is mentioned, extract the amount or percentage value associated with it. If not mentioned, return "Not specified."
    14. "Reimbursement of Expenses?": Indicate if reimbursement of expenses is mentioned in the document. Return "Yes" or "No."
    15. "If applicable, Cap for Reimbursement of Expenses?": Specify the cap for reimbursable expenses, if stated.
    16. "Termination Clause specified?": Indicate if a termination clause is explicitly mentioned. Return "Yes" or "No."
    17. "Termination Clause wording": Provide the exact wording or summary of the termination clause, if mentioned.
    18. "Right of the Banker of Advertising or Disclosing the transaction?": Indicate if the banker has the right to advertise or disclose the transaction. Return "Yes" or "No."
    19. "Jurisdiction (Geographically)": Extract the geographical jurisdiction mentioned in the document.
    20. "Tail Provision conditions": Extract the conditions for the tail provision, if mentioned.
    21. "Tail Provision time": Specify the time period for the tail provision, if explicitly mentioned.
    22. "Summary": Provide a short summary of the Engagement Letter, summarizing the key points in 3-4 sentences.

    The response must be formatted as follows:

    {{
        "Banker or Advisor": "value",
        "Date": "value",
        "Address": "value",
        "Engaged Customer/Client": "value",
        "Engaged Customer/Client registration location": "value",
        "Engaged customer Legal Name": "value",
        "Exclusivity?": "value",
        "Type of Service to be provided by Bank": "value",
        "Services to be provided by Bank": "value",
        "Retainer?": "value",
        "Retainer credited against Transaction Fee?": "value",
        "Success Fee?": "value",
        "Success Fee Amount": "value",
        "Reimbursement of Expenses?": "value",
        "If applicable, Cap for Reimbursement of Expenses?": "value",
        "Termination Clause specified?": "value",
        "Termination Clause wording": "value",
        "Right of the Banker of Advertising or Disclosing the transaction?": "value",
        "Jurisdiction (Geographically)": "value",
        "Tail Provision conditions": "value",
        "Tail Provision time": "value",
        "Summary": "value"
    }}
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a data extraction assistant specialized in Engagement Letters."},
            {"role": "user", "content": extraction_prompt + "\n\n" + text}
        ],
        "temperature": 0,
    }

    response = requests.post(OPENAI_ENDPOINT, headers=GPT_HEADERS, json=payload)

    if response.status_code == 200:
        try:
            content = response.json()["choices"][0]["message"]["content"]
            print(f"GPT response: {content}")  # Mostrar para depuración
            json_content = re.sub(r'^```json\s*|\s*```$', '', content, flags=re.MULTILINE).strip()
            return json.loads(json_content)
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"Error: Invalid JSON received. Response content: {content}")
            print(f"Exception: {e}")
            return None
    else:
        print(f"Error: {response.status_code}, Details: {response.text}")
        return None

# Función para procesar chunks y almacenar resultados
def process_chunks(chunks_por_pdf):
    """
    Procesa los chunks por cada PDF y almacena resultados.
    """
    resultados_por_pdf = {}
    logs = []  # Acumula los logs de todos los chunks procesados

    for filename, chunks in chunks_por_pdf.items():
        print(f"Procesando chunks para el archivo {filename}. Total chunks: {len(chunks)}")
        resultados_pdf = []
        for i, chunk in enumerate(chunks):
            print(f"Procesando chunk {i + 1}/{len(chunks)} del archivo {filename}:\n{chunk[:200]}...")  # Muestra los primeros 200 caracteres del chunk
            resultado = consultar_gpt(chunk)
            if resultado:
                print(f"Resultado procesado para chunk {i + 1}/{len(chunks)} del archivo {filename}:\n{json.dumps(resultado, indent=4)}")
                resultados_pdf.append(resultado)
                
                # Guardar el log del resultado parcial
                logs.append(f"Chunk {i + 1} del archivo {filename}: {json.dumps(resultado, indent=2)}")
            else:
                error_message = f"Error procesando chunk {i + 1} del archivo {filename}. Sin respuesta válida."
                print(error_message)
                logs.append(error_message)
        
        resultados_por_pdf[filename] = resultados_pdf

    return resultados_por_pdf, logs  # Devuelve también los logs

# Function to request GPT to consolidate data into a single JSON
def consolidate_with_gpt(prepared_data):
    """
    Consolidates data extracted from documents into a structured JSON.
    Prioritize the most common values for each field, and handle multiple values when necessary.
    If values like 'Not specified' or 'Not Stated' appear, give priority to actual values if available.
    """
    
    # Convertir los datos a JSON para ser pasados a GPT en el prompt
    data_json = json.dumps(prepared_data, indent=2)

    # Prompt para la consolidación con los puntos clave especificados, incluyendo el resumen
    prompt = f"""
    Act as a data consolidation assistant. From the extracted data points across multiple chunks, combine them into a
    single JSON that reflects the most common or most contextually accurate values for each field. Prioritize confirmed values over "Not specified" or "Not Stated".

    Additionally, provide a short summary of the Engagement Letter that highlights the key points in 2-3 sentences.

    Data to consolidate:
    {data_json}

    Return the consolidated data in the following JSON format:
    {{
        "Banker or Advisor": "Most common or most contextually accurate value.",
        "Date": "Most common or most contextually accurate value.",
        "Address": "Most common or most contextually accurate value.",
        "Engaged Customer/Client": "Most common or most contextually accurate value.",
        "Engaged Customer/Client registration location": "Most common or most contextually accurate value.",
        "Engaged customer Legal Name": "Most common or most contextually accurate value.",
        "Exclusivity?": "Most common or most contextually accurate value.",
        "Type of Service to be provided by Bank": "Most common or most contextually accurate value.",
        "Services to be provided by Bank": "Most common or most contextually accurate value.",
        "Retainer?": "Most common or most contextually accurate value.",
        "Retainer credited against Transaction Fee?": "Most common or most contextually accurate value.",
        "Success Fee?": "Most common or most contextually accurate value.",
        "Success Fee Amount": "Most common or most contextually accurate value.",
        "Reimbursement of Expenses?": "Most common or most contextually accurate value.",
        "If applicable, Cap for Reimbursement of Expenses?": "Most common or most contextually accurate value.",
        "Termination Clause specified?": "Most common or most contextually accurate value.",
        "Termination Clause wording": "Most common or most contextually accurate value.",
        "Right of the Banker of Advertising or Disclosing the transaction?": "Most common or most contextually accurate value.",
        "Jurisdiction (Geographically)": "Most common or most contextually accurate value.",
        "Tail Provision conditions": "Most common or most contextually accurate value.",
        "Tail Provision time": "Most common or most contextually accurate value.",
        "Summary": "Consolidated summary based on extracted data."
    }}
    """

    # Construcción del payload para el API de GPT
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a data consolidation assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
    }

    # Enviar el payload a la API de GPT
    response = requests.post(OPENAI_ENDPOINT, headers=GPT_HEADERS, json=payload)

    if response.status_code == 200:
        try:
            content = response.json()["choices"][0]["message"]["content"]
            # Limpiar la respuesta JSON
            json_content = re.sub(r'^```json\s*|\s*```$', '', content, flags=re.MULTILINE).strip()
            consolidated_data = json.loads(json_content)

            if not isinstance(consolidated_data, dict):
                raise ValueError("La respuesta consolidada no es un diccionario válido.")

            return consolidated_data

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error procesando JSON consolidado: {e}")
            print(f"Respuesta recibida: {response.text}")
            return None
    else:
        print(f"Error: {response.status_code}, Details: {response.text}")
        return None