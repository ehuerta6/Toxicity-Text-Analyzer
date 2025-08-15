"""
🧪 Script de prueba para verificar el endpoint de análisis - ToxiGuard
Prueba que el endpoint /analyze funcione correctamente y devuelva el formato esperado
"""

import requests
import json

def test_analyze_endpoint():
    """Prueba el endpoint de análisis"""
    
    url = "http://127.0.0.1:8000/analyze"
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die"
    ]
    
    print("🧪 PRUEBA DEL ENDPOINT DE ANÁLISIS - TOXIGUARD")
    print("=" * 60)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        
        try:
            # Enviar solicitud
            payload = {"text": text}
            response = requests.post(url, json=payload, timeout=10)
            
            print(f"📡 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Respuesta exitosa:")
                print(f"  • is_toxic: {data.get('is_toxic')}")
                print(f"  • toxicity_percentage: {data.get('toxicity_percentage')}%")
                print(f"  • toxicity_category: {data.get('toxicity_category')}")
                print(f"  • confidence: {data.get('confidence')}")
                print(f"  • model_used: {data.get('model_used')}")
                print(f"  • classification_technique: {data.get('classification_technique')}")
                print(f"  • detected_categories: {data.get('detected_categories')}")
                print(f"  • word_count: {data.get('word_count')}")
                print(f"  • response_time_ms: {data.get('response_time_ms')}ms")
                print(f"  • explanations: {data.get('explanations', 'No disponible')}")
                
                # Verificar campos requeridos
                required_fields = [
                    'text', 'is_toxic', 'toxicity_percentage', 'toxicity_category',
                    'confidence', 'detected_categories', 'word_count', 'response_time_ms',
                    'timestamp', 'model_used', 'classification_technique', 'explanations'
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"⚠️ Campos faltantes: {missing_fields}")
                else:
                    print("✅ Todos los campos requeridos están presentes")
                    
            else:
                print(f"❌ Error del servidor: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  • Detalle: {error_data.get('detail', 'Sin detalle')}")
                except:
                    print(f"  • Respuesta: {response.text}")
                    
        except requests.exceptions.ConnectionError:
            print("❌ No se pudo conectar al servidor. Verifica que esté ejecutándose.")
        except requests.exceptions.Timeout:
            print("⏰ Timeout en la solicitud.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

def test_health_endpoint():
    """Prueba el endpoint de salud"""
    
    url = "http://127.0.0.1:8000/health"
    
    print("\n🏥 PRUEBA DEL ENDPOINT DE SALUD:")
    print("-" * 40)
    
    try:
        response = requests.get(url, timeout=5)
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Servidor saludable:")
            print(f"  • Status: {data.get('status')}")
            print(f"  • Classifier: {data.get('classifier')}")
            print(f"  • Database: {data.get('database')}")
        else:
            print(f"❌ Error del servidor: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        test_health_endpoint()
        test_analyze_endpoint()
        print("\n✅ Todas las pruebas completadas!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
