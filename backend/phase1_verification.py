#!/usr/bin/env python3
"""
Verificación completa de la Fase 1 de ToxiGuard
Prueba backend, frontend y CORS
"""

import requests
import json
import time

def test_backend_health():
    """Prueba el endpoint de salud del backend"""
    print("🏥 Probando endpoint /health...")
    
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Response: {result}")
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_analyze_endpoint():
    """Prueba el endpoint de análisis con diferentes casos"""
    print("\n🔍 Probando endpoint /analyze...")
    
    test_cases = [
        {
            "name": "Texto normal (no tóxico)",
            "text": "Hola, ¿cómo estás? Es un día hermoso.",
            "expected_toxic": False
        },
        {
            "name": "Texto tóxico (español)",
            "text": "Eres un idiota estupido!",
            "expected_toxic": True
        },
        {
            "name": "Texto tóxico (inglés)",
            "text": "You are a stupid idiot and asshole!",
            "expected_toxic": True
        },
        {
            "name": "Texto mixto español-inglés",
            "text": "Eres un idiot y tonto, pero no te odio.",
            "expected_toxic": True
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n   📝 Caso: {test_case['name']}")
        print(f"      Texto: {test_case['text']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/analyze",
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"      ✅ Status: {response.status_code}")
                print(f"      🎯 Tóxico: {result['toxic']} (esperado: {test_case['expected_toxic']})")
                print(f"      📊 Score: {result['score']}")
                print(f"      🏷️  Labels: {result['labels']}")
                print(f"      📏 Longitud: {result['text_length']}")
                print(f"      🔍 Palabras clave: {result['keywords_found']}")
                
                # Verificar estructura de respuesta
                required_fields = ['toxic', 'score', 'labels', 'text_length', 'keywords_found']
                missing_fields = [field for field in required_fields if field not in result]
                
                if missing_fields:
                    print(f"      ❌ Campos faltantes: {missing_fields}")
                    all_passed = False
                else:
                    print(f"      ✅ Estructura de respuesta correcta")
                
                # Verificar tipos de datos
                if not isinstance(result['toxic'], bool):
                    print(f"      ❌ Campo 'toxic' no es boolean")
                    all_passed = False
                
                if not isinstance(result['score'], (int, float)) or not (0 <= result['score'] <= 1):
                    print(f"      ❌ Campo 'score' no es float entre 0 y 1")
                    all_passed = False
                
                if not isinstance(result['labels'], list):
                    print(f"      ❌ Campo 'labels' no es lista")
                    all_passed = False
                
                # Verificar lógica del clasificador
                if result['toxic'] == test_case['expected_toxic']:
                    print(f"      ✅ Clasificación correcta")
                else:
                    print(f"      ⚠️  Clasificación inesperada")
                    all_passed = False
                    
            else:
                print(f"      ❌ Status: {response.status_code}")
                print(f"      Error: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
            all_passed = False
    
    return all_passed

def test_cors():
    """Prueba que CORS esté configurado correctamente"""
    print("\n🌐 Probando configuración CORS...")
    
    try:
        # Simular petición desde el frontend
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"text": "Test CORS"},
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:5173"
            }
        )
        
        if response.status_code == 200:
            print("   ✅ CORS permite peticiones desde frontend")
            return True
        else:
            print(f"   ❌ CORS bloqueó la petición: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error probando CORS: {e}")
        return False

def test_frontend_dev_server():
    """Verifica que el frontend esté funcionando"""
    print("\n🎨 Verificando servidor frontend...")
    
    try:
        response = requests.get("http://localhost:5173")
        if response.status_code == 200:
            print("   ✅ Servidor frontend funcionando en puerto 5173")
            return True
        else:
            print(f"   ❌ Frontend respondió con status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error conectando al frontend: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN COMPLETA DE LA FASE 1 - ToxiGuard")
    print("=" * 70)
    
    results = {}
    
    # Probar backend
    print("\n🔧 VERIFICANDO BACKEND...")
    results['backend_health'] = test_backend_health()
    results['analyze_endpoint'] = test_analyze_endpoint()
    results['cors'] = test_cors()
    
    # Probar frontend
    print("\n🎨 VERIFICANDO FRONTEND...")
    results['frontend_server'] = test_frontend_dev_server()
    
    # Resumen de resultados
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{test_name:.<30} {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\n📈 RESULTADOS: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡FASE 1 COMPLETADA EXITOSAMENTE!")
        print("\n📋 Para probar manualmente:")
        print("1. Abre http://localhost:5173 en tu navegador")
        print("2. Escribe un texto en el textarea")
        print("3. Haz clic en 'Analizar'")
        print("4. Verifica que se muestren los resultados correctamente")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} pruebas fallaron")
        print("   Revisa los errores arriba y corrige los problemas")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
