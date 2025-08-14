#!/usr/bin/env python3
"""
Prueba rápida del endpoint /analyze
"""

import requests

def quick_test():
    """Prueba rápida del endpoint"""
    try:
        # Probar con un texto tóxico
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"text": "Eres un idiota estupido!"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Endpoint /analyze funcionando!")
            print(f"   Texto: 'Eres un idiota estupido!'")
            print(f"   Tóxico: {result['toxic']}")
            print(f"   Score: {result['score']}")
            print(f"   Labels: {result['labels']}")
            print(f"   Longitud: {result['text_length']}")
            print(f"   Palabras clave: {result['keywords_found']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    quick_test()
