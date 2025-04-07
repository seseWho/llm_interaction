# test_suite.py
import unittest
import time
import json
import re
from typing import List, Dict, Any

from llm_client import LLMClient
from config import API_KEY, BASE_URL, MODEL_NAME

class LLMTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para toda la suite de pruebas"""
        cls.client = LLMClient(API_KEY, BASE_URL, MODEL_NAME)
    
    def test_connection(self):
        """Probar conexión inicial"""
        self.assertIsNotNone(self.client, "Fallo en inicialización del cliente")

    def test_response_generation(self):
        """Probar generación de respuesta básica"""
        prompt = "Explica la teoría de la relatividad en una frase"
        response = self.client.generate_response(prompt)
        
        self.assertIn('choices', response, "Respuesta no contiene campo 'choices'")
        self.assertTrue(len(response['choices']) > 0, "Respuesta vacía")
        
        generated_text = response['choices'][0]['message']['content']
        self.assertIsNotNone(generated_text, "No se generó texto de respuesta")
        self.assertTrue(len(generated_text) > 0, "Respuesta generada está vacía")

    def test_response_time(self):
        """Verificar tiempo de respuesta"""
        prompt = "Hola, ¿cómo estás?"
        start_time = time.time()
        response = self.client.generate_response(prompt)
        response_time = time.time() - start_time
        
        self.assertLess(response_time, 5, "Tiempo de respuesta excesivo")

    def test_context_length_limit(self):
        """Probar límite de contexto"""
        # Generar un prompt muy largo para probar el límite de contexto
        long_context = "x" * 100000  # 100,000 caracteres
        
        with self.assertRaises((ValueError, Exception), 
                                msg="No se manejó correctamente el límite de contexto"):
            self.client.generate_response(long_context)

    def test_multilingual_support(self):
        """Probar soporte multilenguaje"""
        test_prompts = [
            # Diferentes idiomas y scripts
            "Hello, how are you?",  # Inglés
            "Bonjour, comment ça va?",  # Francés
            "こんにちは、元気ですか？",  # Japonés
            "¿Cómo estás hoy?",  # Español
            "Wie geht es dir?",  # Alemán
            "Привет, как дела?",  # Ruso
            "你好，今天怎么样？",  # Chino
            "مرحبا، كيف حالك؟"  # Árabe
        ]
        
        for prompt in test_prompts:
            response = self.client.generate_response(prompt)
            generated_text = response['choices'][0]['message']['content']
            
            self.assertIsNotNone(generated_text, 
                f"No se generó respuesta para el prompt en: {prompt}")

    def test_temperature_variation(self):
        """Probar variación de temperaturas"""
        prompt = "Cuenta una historia corta sobre un viaje"
        
        # Generar respuestas con diferentes temperaturas
        responses = {
            'low_temp': self.client.generate_response(prompt, temperature=0.1),
            'medium_temp': self.client.generate_response(prompt, temperature=0.5),
            'high_temp': self.client.generate_response(prompt, temperature=0.9)
        }
        
        # Verificar que las respuestas sean diferentes
        unique_responses = set(
            resp['choices'][0]['message']['content'] 
            for resp in responses.values()
        )
        
        # Con temperaturas más altas, esperamos más variación
        self.assertTrue(len(unique_responses) > 1, 
            "Las respuestas no muestran suficiente variación con diferentes temperaturas")

    def test_json_parsing(self):
        """Probar capacidad de generación de JSON estructurado"""
        prompt = """
        Genera un JSON con información de un libro ficticio. 
        Debe contener: título, autor, año de publicación, géneros (lista), 
        y una breve sinopsis.
        """
        
        response = self.client.generate_response(prompt)
        generated_text = response['choices'][0]['message']['content']
        
        # Intentar parsear el JSON
        try:
            book_data = json.loads(generated_text)
            
            # Verificaciones de estructura
            self.assertIn('titulo', book_data)
            self.assertIn('autor', book_data)
            self.assertIn('año_publicacion', book_data)
            self.assertIn('generos', book_data)
            self.assertIsInstance(book_data['generos'], list)
            self.assertIn('sinopsis', book_data)
        except json.JSONDecodeError:
            self.fail("El modelo no generó un JSON válido")

    def test_code_generation(self):
        """Probar generación de código"""
        prompts = [
            "Escribe una función en Python para calcular el factorial de un número",
            "Crea un algoritmo de ordenamiento en JavaScript"
        ]
        
        for prompt in prompts:
            response = self.client.generate_response(prompt)
            generated_code = response['choices'][0]['message']['content']
            
            # Verificaciones básicas de código
            self.assertIsNotNone(generated_code, "No se generó código")
            self.assertTrue(len(generated_code) > 0, "Código generado está vacío")
            
            # Verificar que contenga elementos de código
            code_indicators = [
                r'\bdef\b',  # Definición de función en Python
                r'\bfunction\b',  # Definición de función en JavaScript
                r'\breturn\b',  # Palabra clave de retorno
                r'\bif\b',  # Condicional
            ]
            
            code_found = any(re.search(pattern, generated_code, re.IGNORECASE) 
                              for pattern in code_indicators)
            self.assertTrue(code_found, "El código generado no parece ser válido")

    def test_reasoning_capability(self):
        """Probar capacidad de razonamiento lógico"""
        reasoning_prompts = [
            "Resuelve este acertijo: Si 5 gatos atrapan 5 ratones en 5 minutos, ¿cuántos gatos se necesitarán para atrapar 100 ratones en 100 minutos?",
            "Un tren sale de la ciudad A a 60 km/h y otro tren sale de la ciudad B a 40 km/h en dirección opuesta. Las ciudades están separadas por 500 km. ¿En cuánto tiempo se encontrarán?"
        ]
        
        for prompt in reasoning_prompts:
            response = self.client.generate_response(prompt)
            solution = response['choices'][0]['message']['content']
            
            self.assertIsNotNone(solution, "No se generó solución")
            self.assertTrue(len(solution) > 10, "Solución demasiado corta")
            
            # Verificar que incluya pasos de razonamiento
            reasoning_indicators = [
                r'\bsi\b',  # "si" en español sugiere razonamiento
                r'\bentonces\b',  # "entonces" indica paso lógico
                r'\bpor lo tanto\b',  # conclusión lógica
                r'\npaso\s*[1-9]',  # indicación de pasos
            ]
            
            reasoning_found = any(re.search(pattern, solution, re.IGNORECASE) 
                                   for pattern in reasoning_indicators)
            self.assertTrue(reasoning_found, "La solución no muestra pasos de razonamiento")

    def test_chain_of_thought(self):
        """Evaluar razonamiento paso a paso"""
        prompt = "Explica paso a paso cómo calcular la media de una lista de números."
        response = self.client.generate_response(prompt)
        content = response['choices'][0]['message']['content']
        self.assertRegex(content, r"paso\s+\d+", msg="No se detectaron pasos en la explicación")

    def test_markdown_table_output(self):
        """Probar si puede generar una tabla en Markdown"""
        prompt = "Genera una tabla en Markdown con tres lenguajes de programación y su año de creación."
        response = self.client.generate_response(prompt)
        content = response['choices'][0]['message']['content']
        self.assertIn('|', content, "No se generó una tabla Markdown")
        self.assertIn('Lenguaje', content, "Faltan encabezados esperados en la tabla")

    def test_emojis_in_response(self):
        """Verificar si puede responder con emojis"""
        prompt = "Dime cómo se siente alguien que gana la lotería, usando emojis"
        response = self.client.generate_response(prompt)
        content = response['choices'][0]['message']['content']
        self.assertRegex(content, r"[😀🎉💰]", msg="No se detectaron emojis en la respuesta")

    def test_ambiguous_instruction(self):
        """Probar respuesta ante instrucciones ambiguas"""
        prompt = "Dime cómo arreglar todo"
        response = self.client.generate_response(prompt)
        content = response['choices'][0]['message']['content']
        self.assertTrue(len(content) > 20, "Respuesta muy corta para una instrucción compleja")
        self.assertNotIn("no sé", content.lower(), "Respuesta evasiva ante ambigüedad")

    def test_get_model_info(self):
        """Verificar método get_model_info"""
        model_info = self.client.get_model_info()
        self.assertIn('name', model_info)
        self.assertIn('api_base', model_info)


def run_tests():
    """Ejecutar la suite de pruebas"""
    suite = unittest.TestLoader().loadTestsFromTestCase(LLMTestSuite)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Imprimir resumen
    print(f"\nPruebas ejecutadas: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()