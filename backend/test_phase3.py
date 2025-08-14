#!/usr/bin/env python3
"""
Test script para verificar la implementación de Fase 3 de ToxiGuard
Prueba todas las nuevas funcionalidades implementadas
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:8000"
TEST_TEXTS = [
    "Hola, ¿cómo estás?",
    "Eres un idiota estúpido",
    "Te voy a matar, odio tu existencia",
    "Eres un racista de mierda",
    "Comprar barato, oferta especial",
    "",  # Texto vacío para probar validación
    "x" * 10001,  # Texto muy largo para probar validación
]

def test_health_endpoints():
    """Prueba los endpoints de salud"""
    print("🔍 Probando endpoints de salud...")
    
    # Test /health
    response = requests.get(f"{BASE_URL}/health")
    print(f"  /health: {response.status_code} - {response.json()}")
    
    # Test /api/health
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"  /api/health: {response.status_code} - {response.json()}")
    
    # Test /ml/status
    response = requests.get(f"{BASE_URL}/ml/status")
    print(f"  /ml/status: {response.status_code} - {response.json()}")

def test_analyze_endpoint():
    """Prueba el endpoint /analyze mejorado"""
    print("\n🔍 Probando endpoint /analyze mejorado...")
    
    for i, text in enumerate(TEST_TEXTS):
        print(f"\n  Test {i+1}: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/analyze",
                json={"text": text}
            )
            end_time = time.time()
            
            print(f"    Status: {response.status_code}")
            print(f"    Response time: {round((end_time - start_time) * 1000, 2)}ms")
            
            if response.status_code == 200:
                data = response.json()
                print(f"    Toxic: {data.get('toxic')}")
                print(f"    Score: {data.get('score')}")
                print(f"    Toxicity %: {data.get('toxicity_percentage')}%")
                print(f"    Category: {data.get('category')}")
                print(f"    Labels: {data.get('labels')}")
                print(f"    Model used: {data.get('model_used')}")
                print(f"    Response time (API): {data.get('response_time_ms')}ms")
            else:
                print(f"    Error: {response.json()}")
                
        except Exception as e:
            print(f"    Exception: {e}")

def test_categories_endpoint():
    """Prueba el endpoint /categories"""
    print("\n🔍 Probando endpoint /categories...")
    
    try:
        response = requests.get(f"{BASE_URL}/categories")
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total categories: {data.get('total_categories')}")
            print(f"  Categories: {list(data.get('categories', {}).keys())}")
            print(f"  Weights: {data.get('weights')}")
        else:
            print(f"  Error: {response.json()}")
            
    except Exception as e:
        print(f"  Exception: {e}")

def test_keywords_endpoints():
    """Prueba los endpoints de palabras clave"""
    print("\n🔍 Probando endpoints de palabras clave...")
    
    # Test /keywords
    try:
        response = requests.get(f"{BASE_URL}/keywords")
        print(f"  /keywords Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"    Total keywords: {data.get('count')}")
            print(f"    Categories: {list(data.get('categories', {}).keys())}")
    except Exception as e:
        print(f"  Exception: {e}")
    
    # Test añadir palabra clave
    try:
        response = requests.post(
            f"{BASE_URL}/keywords/add",
            params={"keyword": "testword", "category": "insulto"}
        )
        print(f"  /keywords/add Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"    Message: {data.get('message')}")
    except Exception as e:
        print(f"  Exception: {e}")

def test_error_handling():
    """Prueba el manejo de errores mejorado"""
    print("\n🔍 Probando manejo de errores...")
    
    # Test texto vacío
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={"text": ""}
        )
        print(f"  Empty text: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"  Exception: {e}")
    
    # Test texto muy largo
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={"text": "x" * 10001}
        )
        print(f"  Long text: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"  Exception: {e}")

def test_cors():
    """Prueba la configuración de CORS"""
    print("\n🔍 Probando configuración de CORS...")
    
    try:
        # Simular request con Origin header
        headers = {"Origin": "http://localhost:5173"}
        response = requests.get(f"{BASE_URL}/health", headers=headers)
        
        cors_headers = response.headers.get("access-control-allow-origin")
        print(f"  CORS Origin header: {cors_headers}")
        
        if cors_headers:
            print("  ✅ CORS configurado correctamente")
        else:
            print("  ⚠️  CORS no configurado")
            
    except Exception as e:
        print(f"  Exception: {e}")

def main():
    """Función principal de testing"""
    print("🚀 Iniciando tests de Fase 3 - ToxiGuard Enhanced API")
    print("=" * 60)
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Servidor no disponible en {BASE_URL}")
            return
        print("✅ Servidor disponible")
        
        # Ejecutar todos los tests
        test_health_endpoints()
        test_analyze_endpoint()
        test_categories_endpoint()
        test_keywords_endpoints()
        test_error_handling()
        test_cors()
        
        print("\n" + "=" * 60)
        print("✅ Tests de Fase 3 completados")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ No se pudo conectar al servidor en {BASE_URL}")
        print("   Asegúrate de que el servidor esté corriendo con: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error durante los tests: {e}")

if __name__ == "__main__":
    main()
