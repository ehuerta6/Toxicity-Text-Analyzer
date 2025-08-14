#!/usr/bin/env python3
"""
Script de prueba para el endpoint /analyze de ToxiGuard
"""

import requests
import json

def test_analyze_endpoint():
    """Prueba el endpoint /analyze con diferentes tipos de texto"""
    base_url = "http://localhost:8000"
    
    print("🧪 Probando endpoint /analyze de ToxiGuard...")
    print(f"📍 URL base: {base_url}")
    print("-" * 60)
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Texto normal",
            "text": "Hola, ¿cómo estás? Es un día hermoso.",
            "expected_toxic": False
        },
        {
            "name": "Texto con insulto leve",
            "text": "Eres un poco tonto, pero no te enojes.",
            "expected_toxic": True
        },
        {
            "name": "Texto muy tóxico",
            "text": "Eres un idiota estupido y pendejo, ojalá te mueras.",
            "expected_toxic": True
        },
        {
            "name": "Texto en inglés tóxico",
            "text": "You are a stupid idiot and asshole!",
            "expected_toxic": True
        },
        {
            "name": "Texto mixto español-inglés",
            "text": "Eres un idiot y tonto, pero no te odio.",
            "expected_toxic": True
        },
        {
            "name": "Texto largo normal",
            "text": "Este es un texto muy largo que contiene muchas palabras pero no tiene contenido tóxico. " * 10,
            "expected_toxic": False
        },
        {
            "name": "Texto vacío",
            "text": "",
            "expected_toxic": False
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}: {test_case['name']}")
        print(f"   Texto: {test_case['text'][:50]}{'...' if len(test_case['text']) > 50 else ''}")
        
        try:
            # Hacer petición POST al endpoint
            response = requests.post(
                f"{base_url}/analyze",
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   🎯 Tóxico: {result['toxic']} (esperado: {test_case['expected_toxic']})")
                print(f"   📊 Score: {result['score']}")
                print(f"   🏷️  Labels: {result['labels']}")
                print(f"   📏 Longitud: {result['text_length']}")
                print(f"   🔍 Palabras clave: {result['keywords_found']}")
                
                # Verificar si el resultado coincide con lo esperado
                if result['toxic'] == test_case['expected_toxic']:
                    print("   ✅ Resultado correcto")
                else:
                    print("   ⚠️  Resultado inesperado")
                    
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "-" * 60)
    print("🎉 Pruebas del endpoint /analyze completadas!")

def test_keywords_endpoints():
    """Prueba los endpoints relacionados con palabras clave"""
    base_url = "http://localhost:8000"
    
    print("\n🔑 Probando endpoints de palabras clave...")
    print("-" * 40)
    
    try:
        # Obtener lista de palabras clave
        response = requests.get(f"{base_url}/keywords")
        if response.status_code == 200:
            keywords_data = response.json()
            print(f"✅ GET /keywords - Total palabras: {keywords_data['count']}")
            print(f"   Umbral: {keywords_data['threshold']}")
            print(f"   Primeras 5 palabras: {keywords_data['keywords'][:5]}")
        else:
            print(f"❌ GET /keywords - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en /keywords: {e}")

if __name__ == "__main__":
    test_analyze_endpoint()
    test_keywords_endpoints()
