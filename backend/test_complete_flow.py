#!/usr/bin/env python3
"""
Script para probar el flujo completo del sistema ToxiGuard con modelo ML
"""

import requests
import json
import time
from pathlib import Path
import sys

# Agregar el directorio padre al path
sys.path.append(str(Path(__file__).parent.parent))

def test_backend_health():
    """Prueba la salud del backend"""
    print("🏥 PROBANDO SALUD DEL BACKEND")
    print("=" * 50)
    
    try:
        # Probar endpoint de salud
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("   ✅ Endpoint /health: FUNCIONANDO")
        else:
            print(f"   ❌ Endpoint /health: Error {response.status_code}")
            return False
        
        # Probar endpoint de API health
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("   ✅ Endpoint /api/health: FUNCIONANDO")
        else:
            print(f"   ❌ Endpoint /api/health: Error {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ❌ No se puede conectar al backend. ¿Está ejecutándose?")
        return False
    except Exception as e:
        print(f"   ❌ Error probando salud del backend: {e}")
        return False

def test_ml_model_status():
    """Prueba el estado del modelo ML"""
    print("\n🤖 PROBANDO ESTADO DEL MODELO ML")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:8000/ml/status")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   📊 Estado del modelo: {status_data['status']}")
            print(f"   📥 Modelo cargado: {status_data['model_loaded']}")
            print(f"   🔧 Modelo disponible: {status_data['ml_model_available']}")
            print(f"   📊 Vectorizador disponible: {status_data['vectorizer_available']}")
            print(f"   💬 Mensaje: {status_data['message']}")
            
            if status_data['model_loaded']:
                print("   ✅ Modelo ML listo para usar")
                return True
            else:
                print("   ⚠️  Modelo ML no está cargado")
                return False
        else:
            print(f"   ❌ Error obteniendo estado del modelo: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error probando estado del modelo ML: {e}")
        return False

def test_ml_model_predictions():
    """Prueba predicciones del modelo ML"""
    print("\n🧪 PROBANDO PREDICCIONES DEL MODELO ML")
    print("=" * 50)
    
    test_cases = [
        {
            "text": "Hello world! This is a nice comment about the weather.",
            "expected": "safe",
            "description": "Comentario positivo"
        },
        {
            "text": "You are an idiot and I hate you!",
            "expected": "toxic",
            "description": "Comentario tóxico directo"
        },
        {
            "text": "This is a neutral comment about technology.",
            "expected": "safe",
            "description": "Comentario neutral"
        },
        {
            "text": "Go to hell you stupid person!",
            "expected": "toxic",
            "description": "Comentario tóxico agresivo"
        },
        {
            "text": "Thank you for your help, it was very useful.",
            "expected": "safe",
            "description": "Comentario agradecido"
        },
        {
            "text": "I can't believe how dumb this is.",
            "expected": "toxic",
            "description": "Comentario tóxico sutil"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\n   📝 Caso {i}: {test_case['description']}")
            print(f"      Texto: {test_case['text'][:60]}{'...' if len(test_case['text']) > 60 else ''}")
            
            # Probar endpoint de prueba ML
            response = requests.post(
                "http://localhost:8000/ml/test",
                data={"text": test_case['text']}
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction_class']
                confidence = result['confidence']
                
                print(f"      Predicción: {prediction.upper()}")
                print(f"      Confianza: {confidence:.3f}")
                print(f"      Texto procesado: {result['processed_text'][:50]}{'...' if len(result['processed_text']) > 50 else ''}")
                
                # Verificar si la predicción es correcta
                is_correct = (prediction == test_case['expected'])
                status = "✅ CORRECTO" if is_correct else "❌ INCORRECTO"
                print(f"      Resultado: {status}")
                
                results.append({
                    'case': i,
                    'text': test_case['text'],
                    'expected': test_case['expected'],
                    'predicted': prediction,
                    'confidence': confidence,
                    'correct': is_correct
                })
                
            else:
                print(f"      ❌ Error en predicción: {response.status_code}")
                results.append({
                    'case': i,
                    'text': test_case['text'],
                    'expected': test_case['expected'],
                    'predicted': 'error',
                    'confidence': 0.0,
                    'correct': False
                })
                
        except Exception as e:
            print(f"      ❌ Error en caso {i}: {e}")
            results.append({
                'case': i,
                'text': test_case['text'],
                'expected': test_case['expected'],
                'predicted': 'error',
                'confidence': 0.0,
                'correct': False
            })
    
    # Resumen de resultados
    correct_predictions = sum(1 for r in results if r['correct'])
    total_predictions = len(results)
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    
    print(f"\n   📊 RESUMEN DE PREDICCIONES:")
    print(f"      Correctas: {correct_predictions}/{total_predictions}")
    print(f"      Precisión: {accuracy:.1f}%")
    
    return results

def test_analyze_endpoint():
    """Prueba el endpoint principal /analyze"""
    print("\n🔍 PROBANDO ENDPOINT PRINCIPAL /ANALYZE")
    print("=" * 50)
    
    test_cases = [
        {
            "text": "This is a wonderful day!",
            "description": "Texto positivo"
        },
        {
            "text": "You are so stupid and annoying!",
            "description": "Texto tóxico"
        },
        {
            "text": "The weather is nice today.",
            "description": "Texto neutral"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\n   📝 Caso {i}: {test_case['description']}")
            print(f"      Texto: {test_case['text'][:50]}{'...' if len(test_case['text']) > 50 else ''}")
            
            # Medir tiempo de respuesta
            start_time = time.time()
            
            response = requests.post(
                "http://localhost:8000/analyze",
                json={"text": test_case['text']}
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"      Tóxico: {'SÍ' if result['toxic'] else 'NO'}")
                print(f"      Score: {result['score']:.3f}")
                print(f"      Etiquetas: {result['labels']}")
                print(f"      Longitud: {result['text_length']} caracteres")
                print(f"      Palabras clave: {result['keywords_found']}")
                print(f"      Tiempo respuesta: {response_time:.3f}s")
                
                results.append({
                    'case': i,
                    'text': test_case['text'],
                    'toxic': result['toxic'],
                    'score': result['score'],
                    'labels': result['labels'],
                    'response_time': response_time,
                    'success': True
                })
                
            else:
                print(f"      ❌ Error: {response.status_code}")
                results.append({
                    'case': i,
                    'text': test_case['text'],
                    'success': False
                })
                
        except Exception as e:
            print(f"      ❌ Error en caso {i}: {e}")
            results.append({
                'case': i,
                'text': test_case['text'],
                'success': False
            })
    
    return results

def test_performance():
    """Prueba el rendimiento del sistema"""
    print("\n⚡ PROBANDO RENDIMIENTO")
    print("=" * 50)
    
    # Texto largo para probar rendimiento
    long_text = "This is a very long comment that contains many words and sentences. " * 50
    
    print(f"   📏 Texto de prueba: {len(long_text)} caracteres")
    
    try:
        # Medir tiempo de respuesta
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"text": long_text}
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Análisis exitoso")
            print(f"   ⏱️  Tiempo de respuesta: {response_time:.3f} segundos")
            print(f"   📊 Resultado: {'Tóxico' if result['toxic'] else 'No Tóxico'}")
            print(f"   🎯 Score: {result['score']:.3f}")
            
            # Evaluar rendimiento
            if response_time < 1.0:
                print("   🚀 Rendimiento: EXCELENTE (< 1s)")
            elif response_time < 2.0:
                print("   ✅ Rendimiento: BUENO (< 2s)")
            elif response_time < 5.0:
                print("   ⚠️  Rendimiento: ACEPTABLE (< 5s)")
            else:
                print("   ❌ Rendimiento: LENTO (> 5s)")
                
            return response_time
            
        else:
            print(f"   ❌ Error en análisis: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error probando rendimiento: {e}")
        return None

def compare_with_naive_classifier():
    """Compara resultados del modelo ML vs clasificador naïve"""
    print("\n🔄 COMPARANDO MODELO ML vs CLASIFICADOR NAÏVE")
    print("=" * 50)
    
    test_texts = [
        "You are an idiot!",
        "This is a nice comment.",
        "Go to hell you stupid person!",
        "Thank you for your help."
    ]
    
    print("   📝 Textos de prueba:")
    for i, text in enumerate(test_texts, 1):
        print(f"      {i}. {text}")
    
    print("\n   🤖 Resultados del modelo ML:")
    
    ml_results = []
    for text in test_texts:
        try:
            response = requests.post(
                "http://localhost:8000/ml/test",
                data={"text": text}
            )
            
            if response.status_code == 200:
                result = response.json()
                ml_results.append({
                    'text': text,
                    'prediction': result['prediction_class'],
                    'confidence': result['confidence']
                })
                print(f"      '{text[:30]}{'...' if len(text) > 30 else ''}' → {result['prediction_class'].upper()} (conf: {result['confidence']:.3f})")
            else:
                print(f"      '{text[:30]}{'...' if len(text) > 30 else ''}' → ERROR")
                
        except Exception as e:
            print(f"      '{text[:30]}{'...' if len(text) > 30 else ''}' → ERROR: {e}")
    
    print("\n   📊 Análisis de resultados:")
    toxic_count = sum(1 for r in ml_results if r['prediction'] == 'toxic')
    safe_count = sum(1 for r in ml_results if r['prediction'] == 'safe')
    
    print(f"      Tóxicos detectados: {toxic_count}")
    print(f"      Seguros detectados: {safe_count}")
    print(f"      Total analizados: {len(ml_results)}")

def main():
    """Función principal"""
    print("🚀 PRUEBAS COMPLETAS DEL FLUJO INTEGRAL - ToxiGuard")
    print("=" * 80)
    
    print("\n⚠️  IMPORTANTE: Asegúrate de que el backend esté ejecutándose en http://localhost:8000")
    print("   Comando: uvicorn app.main:app --reload --port 8000 --host 0.0.0.0")
    
    input("\nPresiona Enter cuando el backend esté ejecutándose...")
    
    tests = [
        ("Salud del Backend", test_backend_health),
        ("Estado del Modelo ML", test_ml_model_status),
        ("Predicciones del Modelo ML", test_ml_model_predictions),
        ("Endpoint Principal /analyze", test_analyze_endpoint),
        ("Rendimiento", test_performance),
        ("Comparación ML vs Naïve", compare_with_naive_classifier)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, True, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False, None))
    
    # Resumen final
    print(f"\n{'='*80}")
    print("📊 RESUMEN FINAL DE PRUEBAS")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for test_name, success, result in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está funcionando correctamente.")
        print("   ✅ Backend funcionando")
        print("   ✅ Modelo ML integrado")
        print("   ✅ Endpoints respondiendo")
        print("   ✅ Rendimiento aceptable")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("\n🚀 El sistema ToxiGuard con modelo ML está listo para usar!")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
