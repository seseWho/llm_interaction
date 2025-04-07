import requests
import time
from typing import Dict, Any, Optional

class LLMClient:
    def __init__(
        self, 
        api_key: str, 
        base_url: str, 
        model: str
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self._validate_connection()

    def _validate_connection(self):
        """Validar conexión inicial con la API"""
        try:
            response = self._make_test_request()
            if not response:
                raise ConnectionError("No se pudo establecer conexión con el modelo LLM")
        except Exception as e:
            raise ConnectionError(f"Error de conexión: {e}")

    def _make_test_request(self, max_retries: int = 3) -> Optional[Dict[str, Any]]:
        """Realizar solicitud de prueba"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'prompt': 'Hola, ¿puedes confirmar que estás funcionando?',
            'max_tokens': 10
        }

        for attempt in range(max_retries):
            try:
                start_time = time.time()
                response = requests.post(
                    f'{self.base_url}/chat/completions', 
                    headers=headers, 
                    json=payload
                )
                response.raise_for_status()
                
                response_time = time.time() - start_time
                return {
                    'status': response.status_code,
                    'response_time': response_time
                }
            except requests.exceptions.RequestException:
                if attempt == max_retries - 1:
                    return None
                time.sleep(1)

    def generate_response(
        self, 
        prompt: str, 
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generar respuesta del modelo"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': temperature
        }

        response = requests.post(
            f'{self.base_url}/chat/completions', 
            headers=headers, 
            json=payload
        )
        
        response.raise_for_status()
        return response.json()

    def get_model_info(self) -> Dict[str, Any]:
        """Obtener información del modelo"""
        return {
            'name': self.model,
            'api_base': self.base_url
        }