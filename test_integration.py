#!/usr/bin/env python3
"""
Script de prueba para verificar la integración Frontend ↔ Backend
"""

import requests
import time
import json

def test_backend():
    """Prueba que el backend esté funcionando"""
    print("🧪 Probando backend...")
    
    try:
        # Probar endpoint de salud
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
            return True
        else:
            print(f"❌ Backend respondió con status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_analyze_endpoint():
    """Prueba el endpoint de análisis"""
    print("\n🔍 Probando endpoint /analyze...")
    
    test_cases = [
        {
            "name": "Texto normal",
            "text": "Hola, ¿cómo estás? Es un día hermoso.",
            "expected_toxic": False
        },
        {
            "name": "Texto tóxico",
            "text": "Eres un idiota estupido!",
            "expected_toxic": True
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📝 Probando: {test_case['name']}")
        print(f"   Texto: {test_case['text']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/analyze",
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: {response.status_code}")
                print(f"   🎯 Tóxico: {result['toxic']} (esperado: {test_case['expected_toxic']})")
                print(f"   📊 Score: {result['score']}")
                print(f"   🏷️  Labels: {result['labels']}")
                
                if result['toxic'] == test_case['expected_toxic']:
                    print("   ✅ Resultado correcto")
                else:
                    print("   ⚠️  Resultado inesperado")
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_frontend_dev_server():
    """Verifica que el frontend esté funcionando"""
    print("\n🌐 Verificando servidor frontend...")
    
    try:
        response = requests.get("http://localhost:5173")
        if response.status_code == 200:
            print("✅ Servidor frontend funcionando en puerto 5173")
            return True
        else:
            print(f"❌ Frontend respondió con status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al frontend: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de integración Frontend ↔ Backend")
    print("=" * 60)
    
    # Probar backend
    backend_ok = test_backend()
    
    if backend_ok:
        # Probar endpoint de análisis
        test_analyze_endpoint()
        
        # Probar frontend
        frontend_ok = test_frontend_dev_server()
        
        if frontend_ok:
            print("\n🎉 ¡Integración completa funcionando!")
            print("\n📋 Para probar manualmente:")
            print("1. Abre http://localhost:5173 en tu navegador")
            print("2. Escribe un texto en el textarea")
            print("3. Haz clic en 'Analizar'")
            print("4. Verifica que se muestren los resultados")
        else:
            print("\n⚠️  Backend funcionando pero frontend no disponible")
            print("   Ejecuta 'npm run dev' en la carpeta frontend")
    else:
        print("\n❌ Backend no disponible")
        print("   Ejecuta 'uvicorn app.main:app --reload --port 8000' en la carpeta backend")

if __name__ == "__main__":
    main()
