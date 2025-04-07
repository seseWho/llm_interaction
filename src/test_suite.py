import time
import unittest
from llm_client import LLMClient
from config import API_KEY, BASE_URL, MODEL_NAME

class LLMTestSuite(unittest.TestCase):
    def setUp(self):
        self.client = LLMClient(API_KEY, BASE_URL, MODEL_NAME)

    def test_connection(self):
        """Probar conexión inicial"""
        self.assertIsNotNone(self.client, "Fallo en inicialización del cliente")

    def test_response_generation(self):
        """Probar generación de respuesta"""
        prompt = "Explica la teoría de la relatividad en una frase"
        response = self.client.generate_response(prompt)
        
        self.assertIn('choices', response, "Respuesta no contiene campo 'choices'")
        self.assertTrue(len(response['choices']) > 0, "Respuesta vacía")

    def test_response_time(self):
        """Verificar tiempo de respuesta"""
        prompt = "Hola, ¿cómo estás?"
        start_time = time.time()
        self.client.generate_response(prompt)
        response_time = time.time() - start_time
        
        self.assertLess(response_time, 5, "Tiempo de respuesta excesivo")