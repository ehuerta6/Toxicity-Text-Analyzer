#!/usr/bin/env python3
"""Test rápido de toxicidad"""
import requests

# Prueba en puerto 8001
try:
    response = requests.post("http://127.0.0.1:8001/analyze", json={"text": "Eres un idiota estúpido"})
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Servidor OK en puerto 8001")
        print(f"Resultado: {'Tóxico' if result.get('toxic') else 'Seguro'}")
        print(f"Porcentaje: {result.get('toxicity_percentage', 0):.1f}%")
        print(f"Score: {result.get('score', 0):.3f}")
        print(f"Palabras encontradas: {result.get('keywords_found', 0)}")
    else:
        print(f"❌ Error HTTP: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
