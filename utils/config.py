# Configuración de claves y constantes
OPENAI_API_KEY = "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"  # Reemplaza con tu clave real
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
GPT_HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
UPLOAD_FOLDER = "/tmp"

# Airtable API configuration
API_KEY = "patvsH8dadMdVzJj0.3d755bca6d70a0d10fa8306da79093553f65643a1398c39de4478b4b0028a357"
BASE_ID = "appl2yXQ5mxXMZWR0"
TABLE_NAME = "tblBes7AC7jbu2vBh"

# Airtable endpoint URL
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# HEADERS for Airtable API
AIRTABLE_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
