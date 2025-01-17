import json
import re
import requests
from utils.config import OPENAI_API_KEY, OPENAI_ENDPOINT, GPT_HEADERS

def consultar_gpt(text):
    extraction_prompt = f"""
    Extract the following data from the provided document text. The response must be in JSON format with the following fields. If a field is not explicitly stated in the document, return "Not specified". If applicable, make sure to format values correctly (e.g., dates, numbers, percentages, etc.).

    The fields to extract are:

    1. "Banker or Advisor": Extract the name of the Banker or Advisor as explicitly stated in the document.
    2. "Engaged Customer/Client": Extract the name of the engaged client or customer.
    3. "Engaged Customer/Client registration location": Extract the registration location (country or jurisdiction) of the client or customer.
    4. "Engaged customer Legal Name": Extract the legal name of the engaged customer, if explicitly mentioned.
    5. "Exclusivity?": Determine if the document specifies exclusivity. Return "Yes" or "No" and provide the relevant section if applicable.
    6. "Type of Service to be provided by Bank": Extract the types of services offered by the bank (e.g., Financial advisory, Investment banking services).
    7. "Services to be provided by Bank": Provide a detailed description of the services to be performed by the bank as stated in the document.
    8. "Retainer?": Indicate whether a retainer is mentioned in the document. Return "Yes" or "No."
    9. "Retainer to be credited against the Transaction Fee?": Specify if the retainer is credited towards the transaction fee.
    10. "Total Amount of Retainer if mentioned": Extract the total amount of the retainer, if explicitly stated.
    11. "Retainer to be paid in Installments?": Indicate if the retainer is to be paid in installments.
    12. "Retainer Periodicity Type": Specify the periodicity type of the retainer (e.g., Monthly, Quarterly, or Irregular).
    13. "Retainer downpayment upon signature?": Indicate if a downpayment is required upon signature of the agreement.
    14. "Periodicity of the Retainer, if applicable": Specify the periodicity details of the retainer if applicable.
    15. "Amount of each Retainer Installment, if applicable": Extract the amount of each retainer installment, if mentioned.
    16. "Amount of Installments, if applicable": Specify the total number of retainer installments, if mentioned.
    17. "Irregular Retainer installments": Provide details of irregular retainer installments, if applicable.
    18. "Success Fee?": Determine if a success fee is mentioned. Return "Yes" or "No."
    19. "Minimum Transaction Fee": Extract the minimum transaction fee, if stated.
    20. "Minimum Success Fee (%)": Specify the minimum success fee percentage, if mentioned.
    21. "Maximum Success Fee (%)": Specify the maximum success fee percentage, if mentioned.
    22. "Success Fee Single Scale or a Scale?": Indicate if the success fee is structured as a single scale or a tiered scale.
    23. "If Single Scale, Success Fee Percentage (%)": If applicable, provide the success fee percentage for a single scale.
    24. "If Scale, Success Fees Breakpoints and Percentages": Provide the breakpoints and percentages for a tiered success fee scale, if applicable.
    25. "Reimbursement of Expenses?": Indicate if reimbursement of expenses is mentioned. Return "Yes" or "No."
    26. "If applicable, Cap for Reimbursement of Expenses?": Specify the cap for reimbursement of expenses, if stated.
    27. "Termination Clause specified?": Indicate if a termination clause is explicitly stated. Return "Yes" or "No."
    28. "Termination Clause wording": Extract the exact wording of the termination clause, if mentioned.
    29. "Right of Advertising or Disclosing the transaction?": Specify if the document includes a clause about advertising or disclosing the transaction.
    30. "Jurisdiction (Geographically)": Extract the jurisdiction (geographical location) mentioned in the document.
    31. "Signed by (Bank)": Extract the name of the person signing on behalf of the bank.
    32. "Signed by Bank (Date)": Provide the date the bank signed the document, if stated.
    33. "Signed by (Client)": Extract the name of the person signing on behalf of the client.
    34. "Signed by Client (Date)": Provide the date the client signed the document, if stated.
    35. "Definition of aggregated consideration": Extract the definition of "aggregated consideration," if explicitly stated.
    36. "Tail Provision conditions": Provide the conditions under which the tail provision applies, if mentioned.
    37. "Tail Provision time": Specify the time period for the tail provision, if applicable.
    38. "Pre-considered targets": Extract any pre-considered targets mentioned in the document.
    39. "Direct Investment, or through SPVs/Funds?": Specify if the investment is direct or through SPVs/Funds.

    The response must be in the following JSON format:

    {{
        "Banker or Advisor": "value",
        "Engaged Customer/Client": "value",
        "Engaged Customer/Client registration location": "value",
        "Engaged customer Legal Name": "value",
        "Exclusivity?": "value",
        "Type of Service to be provided by Bank": "value",
        "Services to be provided by Bank": "value",
        "Retainer?": "value",
        "Retainer to be credited against the Transaction Fee?": "value",
        "Total Amount of Retainer if mentioned": "value",
        "Retainer to be paid in Installments?": "value",
        "Retainer Periodicity Type": "value",
        "Retainer downpayment upon signature?": "value",
        "Periodicity of the Retainer, if applicable": "value",
        "Amount of each Retainer Installment, if applicable": "value",
        "Amount of Installments, if applicable": "value",
        "Irregular Retainer installments": "value",
        "Success Fee?": "value",
        "Minimum Transaction Fee": "value",
        "Minimum Success Fee (%)": "value",
        "Maximum Success Fee (%)": "value",
        "Success Fee Single Scale or a Scale?": "value",
        "If Single Scale, Success Fee Percentage (%)": "value",
        "If Scale, Success Fees Breakpoints and Percentages": "value",
        "Reimbursement of Expenses?": "value",
        "If applicable, Cap for Reimbursement of Expenses?": "value",
        "Termination Clause specified?": "value",
        "Termination Clause wording": "value",
        "Right of Advertising or Disclosing the transaction?": "value",
        "Jurisdiction (Geographically)": "value",
        "Signed by (Bank)": "value",
        "Signed by Bank (Date)": "value",
        "Signed by (Client)": "value",
        "Signed by Client (Date)": "value",
        "Definition of aggregated consideration": "value",
        "Tail Provision conditions": "value",
        "Tail Provision time": "value",
        "Pre-considered targets": "value",
        "Direct Investment, or through SPVs/Funds?": "value"
    }}
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a data extraction assistant."},
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
# Function to request GPT to consolidate data into a single JSON
def consolidate_with_gpt(prepared_data):
    """
    Consolidates data extracted from documents into a structured JSON.
    Prioritize the most common values for each field, and handle multiple values when necessary.
    If values like 'Not specified' or 'Not Stated' appear, give priority to actual values if available.
    """
    
    # Convertir los datos a JSON para ser pasados a GPT en el prompt
    data_json = json.dumps(prepared_data, indent=2)

    # Prompt para la consolidación con los 39 ítems especificados
    prompt = f"""
    Act as a data consolidation assistant. From the extracted data points across multiple chunks, combine them into a
    single JSON that reflects the most common or most contextually accurate values for each field. Prioritize confirmed values over "Not specified" or "Not Stated".

    Data to consolidate:
    {data_json}

    Return the consolidated data in the following JSON format:
    {{
        "Banker or Advisor": "Most common or most contextually accurate value.",
        "Engaged Customer/Client": "Most common or most contextually accurate value.",
        "Engaged Customer/Client registration location": "Most common or most contextually accurate value.",
        "Engaged customer Legal Name": "Most common or most contextually accurate value.",
        "Exclusivity?": "Most common or most contextually accurate value.",
        "Type of Service to be provided by Bank": "Most common or most contextually accurate value.",
        "Services to be provided by Bank": "Most common or most contextually accurate value.",
        "Retainer?": "Most common or most contextually accurate value.",
        "Retainer to be credited against the Transaction Fee?": "Most common or most contextually accurate value.",
        "Total Amount of Retainer if mentioned": "Most common or most contextually accurate value.",
        "Retainer to be paid in Installments?": "Most common or most contextually accurate value.",
        "Retainer Periodicity Type": "Most common or most contextually accurate value.",
        "Retainer downpayment upon signature?": "Most common or most contextually accurate value.",
        "Periodicity of the Retainer, if applicable": "Most common or most contextually accurate value.",
        "Amount of each Retainer Installment, if applicable": "Most common or most contextually accurate value.",
        "Amount of Installments, if applicable": "Most common or most contextually accurate value.",
        "Irregular Retainer installments": "Most common or most contextually accurate value.",
        "Success Fee?": "Most common or most contextually accurate value.",
        "Minimum Transaction Fee": "Most common or most contextually accurate value.",
        "Minimum Success Fee (%)": "Most common or most contextually accurate value.",
        "Maximum Success Fee (%)": "Most common or most contextually accurate value.",
        "Success Fee Single Scale or a Scale?": "Most common or most contextually accurate value.",
        "If Single Scale, Success Fee Percentage (%)": "Most common or most contextually accurate value.",
        "If Scale, Success Fees Breakpoints and Percentages": "Most common or most contextually accurate value.",
        "Reimbursement of Expenses?": "Most common or most contextually accurate value.",
        "If applicable, Cap for Reimbursement of Expenses?": "Most common or most contextually accurate value.",
        "Termination Clause specified?": "Most common or most contextually accurate value.",
        "Termination Clause wording": "Most common or most contextually accurate value.",
        "Right of Advertising or Disclosing the transaction?": "Most common or most contextually accurate value.",
        "Jurisdiction (Geographically)": "Most common or most contextually accurate value.",
        "Signed by (Bank)": "Most common or most contextually accurate value.",
        "Signed by Bank (Date)": "Most common or most contextually accurate value.",
        "Signed by (Client)": "Most common or most contextually accurate value.",
        "Signed by Client (Date)": "Most common or most contextually accurate value.",
        "Definition of aggregated consideration": "Most common or most contextually accurate value.",
        "Tail Provision conditions": "Most common or most contextually accurate value.",
        "Tail Provision time": "Most common or most contextually accurate value.",
        "Pre-considered targets": "Most common or most contextually accurate value.",
        "Direct Investment, or through SPVs/Funds?": "Most common or most contextually accurate value."
    }}
    """

    # Construcción del payload para el API de GPT
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a data consolidation assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
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