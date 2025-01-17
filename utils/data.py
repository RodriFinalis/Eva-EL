import boto3
import os
import json

def prepare_consolidated_data(resultados_por_pdf):
    # Estructura inicial de datos para los 39 ítems
    prepared_data = {
        "Banker or Advisor": [],
        "Engaged Customer/Client": [],
        "Engaged Customer/Client registration location": [],
        "Engaged customer Legal Name": [],
        "Exclusivity?": [],
        "Type of Service to be provided by Bank": [],
        "Services to be provided by Bank": [],
        "Retainer?": [],
        "Retainer to be credited against the Transaction Fee?": [],
        "Total Amount of Retainer if mentioned": [],
        "Retainer to be paid in Installments?": [],
        "Retainer Periodicity Type": [],
        "Retainer downpayment upon signature?": [],
        "Periodicity of the Retainer, if applicable": [],
        "Amount of each Retainer Installment, if applicable": [],
        "Amount of Installments, if applicable": [],
        "Irregular Retainer installments": [],
        "Success Fee?": [],
        "Minimum Transaction Fee": [],
        "Minimum Success Fee (%)": [],
        "Maximum Success Fee (%)": [],
        "Success Fee Single Scale or a Scale?": [],
        "If Single Scale, Success Fee Percentage (%)": [],
        "If Scale, Success Fees Breakpoints and Percentages": [],
        "Reimbursement of Expenses?": [],
        "If applicable, Cap for Reimbursement of Expenses?": [],
        "Termination Clause specified?": [],
        "Termination Clause wording": [],
        "Right of Advertising or Disclosing the transaction?": [],
        "Jurisdiction (Geographically)": [],
        "Signed by (Bank)": [],
        "Signed by Bank (Date)": [],
        "Signed by (Client)": [],
        "Signed by Client (Date)": [],
        "Definition of aggregated consideration": [],
        "Tail Provision conditions": [],
        "Tail Provision time": [],
        "Pre-considered targets": [],
        "Direct Investment, or through SPVs/Funds?": []  # Nuevo ítem añadido
    }

    # Iterar sobre los resultados procesados
    for document_entries in resultados_por_pdf.values():
        for entry in document_entries:
            if isinstance(entry, dict):
                for key in prepared_data:
                    if entry.get(key):
                        # Evitar duplicados si es necesario
                        if entry[key] not in prepared_data[key]:
                            prepared_data[key].append(entry[key])

    return prepared_data
