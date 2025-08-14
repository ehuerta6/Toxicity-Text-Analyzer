#!/usr/bin/env python3
"""
Script de prueba para verificar que el servidor FastAPI esté funcionando
"""

import requests
import time

def test_server():
    """Prueba los endpoints del servidor"""
    base_url = "http://localhost:8000"
    
    print("🧪 Probando servidor ToxiGuard...")
    print(f"📍 URL base: {base_url}")
    print("-" * 50)
    
    # Probar endpoint raíz
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ GET / - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ GET / - Error: {e}")
    
    # Probar endpoint de salud
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ GET /health - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ GET /health - Error: {e}")
    
    # Probar endpoint de salud de la API
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ GET /api/health - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ GET /api/health - Error: {e}")
    
    print("-" * 50)
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    test_server()
