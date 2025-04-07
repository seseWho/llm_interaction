import os
from dotenv import load_dotenv

load_dotenv()

# Configuraciones de la API
API_KEY = os.getenv('LLM_API_KEY')
BASE_URL = os.getenv('LLM_BASE_URL', 'https://api.example.com/v1')
MODEL_NAME = os.getenv('LLM_MODEL', 'claude-3-haiku')