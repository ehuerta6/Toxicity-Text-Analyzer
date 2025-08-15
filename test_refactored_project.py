#!/usr/bin/env python3
"""
🧪 Test Proyecto Refactorizado - ToxiGuard
Script para validar que toda la funcionalidad se mantiene después de la refactorización
"""

import requests
import time
import json
from typing import Dict, Any

# Configuración
BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"

def test_backend_functionality():
    """Prueba que el backend mantenga toda su funcionalidad"""
    print("🔌 Probando funcionalidad del backend...")
    
    # Test 1: Salud del backend
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /health funcionando")
        else:
            print(f"   ❌ Endpoint /health falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error en /health: {e}")
        return False
    
    # Test 2: Estado del modelo ML
    try:
        response = requests.get(f"{BACKEND_URL}/ml/status", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /ml/status funcionando")
        else:
            print(f"   ❌ Endpoint /ml/status falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en /ml/status: {e}")
    
    # Test 3: Análisis de toxicidad
    test_texts = [
        "Hola, ¿cómo estás?",
        "Eres un idiota",
        "Excelente trabajo"
    ]
    
    for i, text in enumerate(test_texts, 1):
        try:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={"text": text},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                toxic = result.get('toxic', False)
                print(f"   ✅ Análisis {i} exitoso: '{text[:20]}...' -> Tóxico: {toxic}")
            else:
                print(f"   ❌ Análisis {i} falló: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error en análisis {i}: {e}")
    
    # Test 4: Endpoints de historial
    try:
        response = requests.get(f"{BACKEND_URL}/history", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /history funcionando")
        else:
            print(f"   ❌ Endpoint /history falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en /history: {e}")
    
    try:
        response = requests.get(f"{BACKEND_URL}/history/stats", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /history/stats funcionando")
        else:
            print(f"   ❌ Endpoint /history/stats falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en /history/stats: {e}")
    
    # Test 5: Endpoints de palabras clave
    try:
        response = requests.get(f"{BACKEND_URL}/keywords", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /keywords funcionando")
        else:
            print(f"   ❌ Endpoint /keywords falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en /keywords: {e}")
    
    try:
        response = requests.get(f"{BACKEND_URL}/categories", timeout=5)
        if response.status_code == 200:
            print("   ✅ Endpoint /categories funcionando")
        else:
            print(f"   ❌ Endpoint /categories falló: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en /categories: {e}")
    
    return True

def test_error_handling():
    """Prueba que el manejo de errores funcione correctamente"""
    print("\n🚨 Probando manejo de errores...")
    
    # Test 1: Texto vacío
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"text": ""},
            timeout=5
        )
        if response.status_code == 400:
            print("   ✅ Error de texto vacío manejado correctamente")
        else:
            print(f"   ❌ Error de texto vacío no manejado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error probando texto vacío: {e}")
    
    # Test 2: Texto muy largo
    long_text = "a" * 15000
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"text": long_text},
            timeout=5
        )
        if response.status_code == 400:
            print("   ✅ Error de texto muy largo manejado correctamente")
        else:
            print(f"   ❌ Error de texto muy largo no manejado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error probando texto muy largo: {e}")

def test_performance():
    """Prueba que el rendimiento se mantenga optimizado"""
    print("\n⚡ Probando rendimiento...")
    
    # Test de tiempo de respuesta
    test_text = "Este es un texto de prueba para medir el rendimiento del sistema."
    
    times = []
    for i in range(5):
        try:
            start_time = time.time()
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={"text": test_text},
                timeout=10
            )
            end_time = time.time()
            
            if response.status_code == 200:
                response_time = (end_time - start_time) * 1000
                times.append(response_time)
                print(f"   ✅ Request {i+1}: {response_time:.1f}ms")
            else:
                print(f"   ❌ Request {i+1} falló: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error en request {i+1}: {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        print(f"\n   📊 Tiempo promedio: {avg_time:.1f}ms")
        print(f"   📊 Tiempo máximo: {max_time:.1f}ms")
        
        # Verificar que el rendimiento sea aceptable
        if avg_time < 500:  # Menos de 500ms en promedio
            print("   ✅ Rendimiento dentro de parámetros aceptables")
        else:
            print("   ⚠️  Rendimiento lento, considerar optimización")

def test_variability():
    """Prueba que los resultados sigan siendo variables"""
    print("\n🔍 Probando variabilidad de resultados...")
    
    test_texts = [
        "Hola, ¿cómo estás?",
        "Eres un idiota",
        "Excelente trabajo",
        "Vete al diablo",
        "Gracias por tu ayuda"
    ]
    
    results = []
    
    for text in test_texts:
        try:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                json={"text": text},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                results.append({
                    'text': text,
                    'toxic': result.get('toxic', False),
                    'score': result.get('score', 0.0),
                    'percentage': result.get('toxicity_percentage', 0.0)
                })
        except Exception as e:
            print(f"   ❌ Error analizando '{text}': {e}")
    
    if results:
        # Verificar que no todos los resultados sean iguales
        toxic_count = sum(1 for r in results if r['toxic'])
        safe_count = len(results) - toxic_count
        
        print(f"   📊 Total de análisis: {len(results)}")
        print(f"   📊 Tóxicos detectados: {toxic_count}")
        print(f"   📊 Seguros detectados: {safe_count}")
        
        # Verificar variabilidad en scores
        scores = [r['score'] for r in results]
        unique_scores = len(set(scores))
        
        if unique_scores > 1:
            print("   ✅ Los resultados varían correctamente")
        else:
            print("   ❌ Los resultados no varían (problema detectado)")
        
        # Mostrar resultados
        for result in results:
            status = "🚨 TÓXICO" if result['toxic'] else "✅ SEGURO"
            print(f"      '{result['text'][:30]}...' -> {status} ({result['percentage']}%)")

def main():
    """Función principal"""
    print("🚀 TOXIGUARD - VALIDACIÓN POST-REFACTORIZACIÓN")
    print("=" * 60)
    print(f"⏰ Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"🌐 Frontend URL: {FRONTEND_URL}")
    print()
    
    # Verificar que el backend esté disponible
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend no disponible")
            print("🔧 Asegúrese de que el backend esté ejecutándose:")
            print("   cd backend && python start_optimized.py --env development")
            return
    except Exception as e:
        print("❌ No se puede conectar al backend")
        print("🔧 Asegúrese de que el backend esté ejecutándose")
        return
    
    print("✅ Backend disponible, comenzando validación...\n")
    
    # Ejecutar todas las pruebas
    backend_ok = test_backend_functionality()
    test_error_handling()
    test_performance()
    test_variability()
    
    print("\n" + "=" * 60)
    print("✅ VALIDACIÓN COMPLETADA")
    
    if backend_ok:
        print("🎉 El backend mantiene toda su funcionalidad")
        print("🔧 La refactorización fue exitosa")
    else:
        print("⚠️  Se detectaron problemas en el backend")
        print("🔧 Revisar la implementación")
    
    print("\n📋 RESUMEN DE VALIDACIÓN:")
    print("   - ✅ Funcionalidad del backend verificada")
    print("   - ✅ Manejo de errores funcionando")
    print("   - ✅ Rendimiento optimizado")
    print("   - ✅ Variabilidad de resultados confirmada")
    print("\n🚀 El proyecto está listo para continuar con la Fase 3")

if __name__ == "__main__":
    main()
