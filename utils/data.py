def prepare_consolidated_data(resultados_por_pdf):
    # Estructura inicial de datos con los campos clave y el nuevo campo "Success Fee Amount"
    prepared_data = {
        "Banker or Advisor": [],
        "Date": [],  
        "Address": [],  
        "Engaged Customer/Client": [],
        "Engaged Customer/Client registration location": [],
        "Engaged customer Legal Name": [],
        "Exclusivity?": [],
        "Type of Service to be provided by Bank": [],
        "Services to be provided by Bank": [],
        "Retainer?": [],
        "Retainer credited against Transaction Fee?": [],
        "Success Fee?": [],
        "Success Fee Amount": [],  
        "Reimbursement of Expenses?": [],
        "If applicable, Cap for Reimbursement of Expenses?": [],
        "Termination Clause specified?": [],
        "Termination Clause wording": [],
        "Right of the Banker of Advertising or Disclosing the transaction?": [],
        "Jurisdiction (Geographically)": [],
        "Tail Provision conditions": [],
        "Tail Provision time": [],
        "Summary": [],  
        "Logs": []  # Mantener registros del historial de procesamiento
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
