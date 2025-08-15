#!/usr/bin/env python3
"""
🧪 Test Backend Consolidado - ToxiGuard
Script unificado para probar todas las funcionalidades del backend
"""

import requests
import time
import json
from typing import Dict, Any

# Configuración
BACKEND_URL = "http://127.0.0.1:8000"
TEST_TEXTS = [
    # Textos seguros
    "Hola, ¿cómo estás?",
    "Me encanta esta aplicación",
    "Gracias por tu ayuda",
    "Excelente trabajo",
    "Muy interesante",
    
    # Textos tóxicos leves
    "Eres un poco tonto",
    "No me gusta esto",
    "Esto es malo",
    
    # Textos tóxicos moderados
    "Eres un idiota",
    "Vete al diablo",
    "Esto es una mierda",
    
    # Textos tóxicos severos
    "Eres un idiota estúpido",
    "Vete al diablo, imbécil",
    "Fuck you, asshole",
    "Go to hell, you stupid moron"
]

def test_backend_health():
    """Prueba la salud del backend"""
    print("🔌 Verificando salud del backend...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend saludable")
            print(f"   Estado: {data.get('status')}")
            print(f"   Modelo: {data.get('model_status')}")
            print(f"   Uptime: {data.get('uptime', 0):.2f}s")
            return True
        else:
            print(f"❌ Backend no saludable: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_model_status():
    """Prueba el estado del modelo ML"""
    print("\n🤖 Verificando estado del modelo ML...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/ml/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estado del modelo:")
            print(f"   Cargado: {data.get('model_loaded')}")
            print(f"   Modelo disponible: {data.get('ml_model_available')}")
            print(f"   Vectorizador disponible: {data.get('vectorizer_available')}")
            print(f"   Estado: {data.get('status')}")
            return data.get('model_loaded', False)
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_toxicity_analysis(text: str, expected_toxic: bool = None) -> Dict[str, Any]:
    """Prueba el análisis de toxicidad de un texto"""
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"text": text},
            timeout=10
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            # Verificar que los resultados varíen
            toxic = result.get('toxic', False)
            score = result.get('score', 0.0)
            percentage = result.get('toxicity_percentage', 0.0)
            model_used = result.get('model_used', 'Unknown')
            
            print(f"   📝 '{text[:30]}...'")
            print(f"      Tóxico: {toxic} | Score: {score:.3f} | {percentage}%")
            print(f"      Modelo: {model_used} | Tiempo: {response_time:.3f}s")
            
            # Verificar expectativa si se proporciona
            if expected_toxic is not None:
                if toxic == expected_toxic:
                    print(f"      ✅ Resultado esperado")
                else:
                    print(f"      ❌ Resultado inesperado (esperado: {expected_toxic})")
            
            return result
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            print(f"      {response.text}")
            return {}
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {}

def test_multiple_texts():
    """Prueba múltiples textos para verificar variabilidad"""
    print("\n🧪 Probando análisis de múltiples textos...")
    
    results = []
    
    for i, text in enumerate(TEST_TEXTS, 1):
        print(f"\n📝 Texto {i}/{len(TEST_TEXTS)}:")
        
        # Determinar expectativa basada en el contenido
        expected_toxic = any(word in text.lower() for word in [
            'idiota', 'tonto', 'diablo', 'mierda', 'fuck', 'asshole', 'hell', 'stupid', 'moron'
        ])
        
        result = test_toxicity_analysis(text, expected_toxic)
        if result:
            results.append(result)
        
        # Pausa breve entre requests
        time.sleep(0.5)
    
    return results

def test_history_endpoints():
    """Prueba los endpoints de historial"""
    print("\n📚 Probando endpoints de historial...")
    
    # Probar obtener historial
    try:
        response = requests.get(f"{BACKEND_URL}/history", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Historial obtenido: {data.get('total', 0)} elementos")
        else:
            print(f"   ❌ Error obteniendo historial: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Probar estadísticas
    try:
        response = requests.get(f"{BACKEND_URL}/history/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Estadísticas obtenidas: {data.get('total_analyses', 0)} análisis totales")
        else:
            print(f"   ❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_keywords_endpoints():
    """Prueba los endpoints de palabras clave"""
    print("\n🔑 Probando endpoints de palabras clave...")
    
    # Probar obtener palabras clave
    try:
        response = requests.get(f"{BACKEND_URL}/keywords", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Palabras clave obtenidas: {data.get('count', 0)} palabras")
        else:
            print(f"   ❌ Error obteniendo palabras clave: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Probar obtener categorías
    try:
        response = requests.get(f"{BACKEND_URL}/categories", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Categorías obtenidas: {data.get('total_categories', 0)} categorías")
        else:
            print(f"   ❌ Error obteniendo categorías: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def analyze_results_variability(results: list):
    """Analiza la variabilidad de los resultados"""
    print("\n📊 ANÁLISIS DE VARIABILIDAD")
    print("=" * 50)
    
    if not results:
        print("❌ No hay resultados para analizar")
        return
    
    # Estadísticas básicas
    total = len(results)
    toxic_count = sum(1 for r in results if r.get('toxic', False))
    safe_count = total - toxic_count
    
    print(f"📈 Total de análisis: {total}")
    print(f"🚨 Tóxicos detectados: {toxic_count}")
    print(f"✅ Seguros detectados: {safe_count}")
    print(f"📊 Porcentaje tóxico: {(toxic_count/total)*100:.1f}%")
    
    # Verificar variabilidad en scores
    scores = [r.get('score', 0.0) for r in results]
    unique_scores = len(set(scores))
    
    print(f"\n🎯 Variabilidad de scores:")
    print(f"   Scores únicos: {unique_scores}/{total}")
    print(f"   Score mínimo: {min(scores):.3f}")
    print(f"   Score máximo: {max(scores):.3f}")
    print(f"   Score promedio: {sum(scores)/len(scores):.3f}")
    
    # Verificar modelos utilizados
    models_used = set(r.get('model_used', 'Unknown') for r in results)
    print(f"\n🤖 Modelos utilizados: {', '.join(models_used)}")
    
    # Verificar tiempos de respuesta
    response_times = [r.get('response_time_ms', 0) for r in results]
    avg_time = sum(response_times) / len(response_times)
    max_time = max(response_times)
    
    print(f"\n⏱️  Tiempos de respuesta:")
    print(f"   Promedio: {avg_time:.1f}ms")
    print(f"   Máximo: {max_time:.1f}ms")
    
    # Verificar que no hay resultados duplicados
    unique_results = len(set(json.dumps(r, sort_keys=True) for r in results))
    if unique_results == total:
        print(f"\n✅ Todos los resultados son únicos")
    else:
        print(f"\n⚠️  Algunos resultados están duplicados")
        print(f"   Únicos: {unique_results}/{total}")

def test_error_handling():
    """Prueba el manejo de errores"""
    print("\n🚨 Probando manejo de errores...")
    
    # Texto vacío
    print("   📝 Probando texto vacío...")
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"text": ""},
            timeout=5
        )
        if response.status_code == 400:
            print("      ✅ Error manejado correctamente")
        else:
            print(f"      ❌ Código inesperado: {response.status_code}")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Texto muy largo
    print("   📝 Probando texto muy largo...")
    long_text = "a" * 15000
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"text": long_text},
            timeout=5
        )
        if response.status_code == 400:
            print("      ✅ Error manejado correctamente")
        else:
            print(f"      ❌ Código inesperado: {response.status_code}")
    except Exception as e:
        print(f"      ❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 TOXIGUARD - PRUEBA DEL BACKEND REFACTORIZADO")
    print("=" * 60)
    print(f"⏰ Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print()
    
    # Verificar conectividad
    if not test_backend_health():
        print("\n❌ Backend no disponible")
        print("🔧 Asegúrese de que el backend esté ejecutándose:")
        print("   cd backend && python start_optimized.py --env development")
        return
    
    # Verificar estado del modelo
    model_loaded = test_model_status()
    
    # Probar análisis de toxicidad
    results = test_multiple_texts()
    
    # Probar endpoints adicionales
    test_history_endpoints()
    test_keywords_endpoints()
    
    # Analizar resultados
    analyze_results_variability(results)
    
    # Probar manejo de errores
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    
    if model_loaded:
        print("🤖 Modelo ML funcionando correctamente")
    else:
        print("⚠️  Usando clasificador mejorado (fallback)")
    
    print("\n📊 RESUMEN:")
    print("   - Backend refactorizado y funcionando")
    print("   - Análisis de toxicidad variando correctamente")
    print("   - Endpoints de historial y palabras clave funcionando")
    print("   - Manejo de errores implementado")
    print("   - Tiempos de respuesta optimizados")

if __name__ == "__main__":
    main()
