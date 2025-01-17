from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

# Configuración de claves y constantes
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
GPT_HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
UPLOAD_FOLDER = "/tmp"

# Airtable API configuration
API_KEY = os.getenv("API_KEY")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = os.getenv("TABLE_NAME")

# Airtable endpoint URL
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# HEADERS for Airtable API
AIRTABLE_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
