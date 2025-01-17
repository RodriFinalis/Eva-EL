import requests
from utils.config import AIRTABLE_URL, AIRTABLE_HEADERS

# Mapeo de campos de la tabla de Airtable
field_mapping = {
    "Banker or Advisor": "fldFCWSJAkSmbRmlQ",
    "Engaged Customer/Client": "fldW5HnhP9I7qUMT4",
    "Engaged Customer/Client registration location": "fldVRO1BVzEmhXxy0",
    "Engaged customer Legal Name": "fldjqmlcL8at1S4Pf",
    "Exclusivity?": "fldQzdpRxmF8OPtWr",
    "Type of Service to be provided by Bank": "fld0EPX8BcsPRyN1T",
    "Services to be provided by Bank": "fldK9v6kZIyYjcUdk",
    "Retainer?": "fldRaW5pTRuWM5lD9",
    "Success Fee?": "flddyBhYKi4PyRhNb",
    "Minimum Success Fee (%)": "fldQCvSY8155uybZi",
    "Maximum Success Fee (%)": "fldbdoWb4GiucJKSN",
    "Minimum Transaction Fee": "fld9C6MhWf6yooo26",
    "Reimbursement of Expenses?": "fldkwtUJbQRIRllSh",
    "If applicable, Cap for Reimbursement of Expenses?": "fldeRRAaI6PxLPrMB",
    "Termination Clause specified?": "fldrn73W4xwe0HdDt",
    "Right of the Banker of Advertising or Disclosing the transaction?": "flddonzsXmqgqePyi",
    "Jurisdiction (Geographically)": "fldndNHePtyjgxMzL",
    "Signator Name (Bank Side)": "fld4B5BzfWOM555Qw",
    "Signator Name (Client Side)": "fld8NWjnWIRj1pcyC",
    "Signing Date (Bank Side)": "fldnraYfAU2o28L73",
    "Signing Date (Client Side)": "fldhgEMnmpBqnotF4",
    "Definition of aggregated consideration": "flduy7xurfleuXqXD",
    "Tail Provision conditions": "fldGyI5rOCu6n3Mpc",
    "Tail Provision time": "fldQPGVq9WrYxvBV0",
    "Pre-considered targets": "fldSqNiuPyhYcpAta",
    "Retainer to be credited against the Transaction Fee?": "fldbnDeynkSSHhsvd",
    "Total Amount of Retainer if mentioned": "fldNPDbhAs40nOCBk",
    "Retainer to be payed in Installments?": "fldkcwLSBy78iW3cV",
    "Retainer Periodicity Type": "fldjpptdDDlWCACON",
    "Retainer downpayment upon signature?": "fld2a55pfcl9GNpSN",
    "Amount of each Retainer Installment, if applicable": "fld4t1fD3o7PpxbZU",
    "Amount of Installments, if applicable": "fldfqFUysq0cdVI33",
    "Irregular Retainer installments": "fldqB2fi38wCosTDX",
    "Success Fee Single Scale or a Scale?": "fldJZa3zAiW46x0NK",
    "If Single Scale, Success Fee Percentage (%)": "fld5orDGiXFwgb1vf",
    "If Scale, Success Fees Breakpoints and Percentages": "fldp0EJWwf90Zq5ap",
    "Termination Clause wording": "fldtzqCZBiCzTt6Be",
    "Direct Investment, or through SPVs/Funds?": "fld2MxYBuA1yB8MtT",
    "Periodicity of the Retainer, if applicable": "fldDhWh2x8pD3Bx1l",
    "Logs": "fldNtWeqD2oHECaSK",
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
