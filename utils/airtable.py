from datetime import datetime
import requests
from utils.config import AIRTABLE_URL, AIRTABLE_HEADERS

field_mapping = {
    "Banker or Advisor": "fldFCWSJAkSmbRmlQ",
    "Date": "fldAX63LEJFh4sZnq",
    "Address": "fldQAtiIqoFP6Fknf",
    "Engaged Customer/Client": "fldDjTQMQRNxpM3JA",
    "Engaged Customer/Client registration location": "fldm87dbvh9bq7xkh",
    "Engaged customer Legal Name": "flduGcC4AfqQnQvRZ",
    "Exclusivity?": "fldGU24n5zJRjK0vG",
    "Type of Service to be provided by Bank": "fld9AYrknsqEYPfTL",
    "Services to be provided by Bank": "fldiRtcMXdk7wnmEf",
    "Retainer?": "fldymaxWwTpEK12wb",
    "Retainer to be credited against the Transaction Fee?": "fld0uCrUm17iyoIDt",
    "Success Fee?": "fldshQjtv1VQ8wpss",
    "Success Fee Amount": "fldN3mFtvuYDiR32U",
    "Reimbursement of Expenses?": "fldoOg33wNtIbLSFI",
    "If applicable, Cap for Reimbursement of Expenses?": "fldw7coaIdzwoUb1A",
    "Termination Clause specified?": "fldO7gCAjNKd8sYpn",
    "Termination Clause wording": "fldKREv3ge1DapisR",
    "Right of the Banker of Advertising or Disclosing the transaction?": "fldv9azfenG4t2A1s",
    "Jurisdiction (Geographically)": "fldAcTtTxdHGvuLfE",
    "Tail Provision conditions": "fldyg3gT4Ks0gz1A5",
    "Tail Provision time": "fld9H4QjF8OOwy8uO",
    "Summary": "fldaZrgq6erRo6Jpd",
    "Logs": "fld2YlOwxSu8Lftac",
    "Creation Date": "fldluH5pMmKAypF53"
}

def create_payload(consolidated_data, logs=""):
    """
    Construye el payload usando los datos consolidados, asegurando que todos los valores sean cadenas.
    """
    payload = {"fields": {}}

    for key, airtable_field in field_mapping.items():
        # Obtener el valor del dato consolidado
        value = consolidated_data.get(key, "Not specified")

        # Si el valor es una lista, convertirlo en una cadena separada por comas
        if isinstance(value, list):
            value = ", ".join(map(str, value))

        # Asegurar que el valor sea una cadena
        payload["fields"][airtable_field] = str(value)

    # Agregar los logs al payload si están presentes
    if logs:
        logs_field = field_mapping.get("Logs")
        if logs_field:
            payload["fields"][logs_field] = logs

    # Agregar la fecha y hora actual en formato ISO 8601
    current_datetime = datetime.utcnow().isoformat() + "Z"  # Incluye el sufijo "Z" para UTC
    creation_date_field = field_mapping.get("Creation Date")
    if creation_date_field:
        payload["fields"][creation_date_field] = current_datetime

    return payload

def create_airtable_record(consolidated_data, logs=""):
    """
    Crea una nueva fila en Airtable con los datos proporcionados.
    """
    # Construir el payload
    payload = create_payload(consolidated_data, logs)

    # Hacer la solicitud POST a Airtable
    response = requests.post(AIRTABLE_URL, headers=AIRTABLE_HEADERS, json=payload)

    if response.status_code == 200:
        print("Fila creada exitosamente en Airtable.")
        return response.json()
    else:
        error_message = f"Error al crear la fila en Airtable: {response.status_code} - {response.text}"
        print(error_message)
        raise Exception(error_message)
