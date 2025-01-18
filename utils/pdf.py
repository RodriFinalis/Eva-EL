import os
import fitz  # PyMuPDF r

def leer_pdfs(upload_folder):
    textos_pdfs = {}
    for filename in os.listdir(upload_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(upload_folder, filename)
            texto_extraido = procesar_pdf(pdf_path)
            textos_pdfs[filename] = texto_extraido
    return textos_pdfs

def procesar_pdf(pdf_path):
    texto_extraido = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            texto_pagina = page.get_text()
            texto_extraido += f"\n[Texto de la página {page_number + 1}]:\n{texto_pagina}"
        pdf_document.close()
    except Exception as e:
        print(f"Error procesando el archivo PDF {pdf_path}: {e}")
    return texto_extraido

def crear_chunks(texto, max_tokens=32000):
    words = texto.split()
    chunks, current_chunk = [], []
    current_length = 0
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk, current_length = [], 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks
