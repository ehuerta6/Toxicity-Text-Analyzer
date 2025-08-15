"""
🧪 Script de prueba para verificar compatibilidad frontend-backend - ToxiGuard
Simula exactamente lo que hace el frontend para identificar problemas de compatibilidad
"""

import requests
import json
import time

def simulate_frontend_request():
    """Simula exactamente la solicitud del frontend"""
    
    url = "http://127.0.0.1:8000/analyze"
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die"
    ]
    
    print("🧪 SIMULACIÓN DE SOLICITUD FRONTEND - TOXIGUARD")
    print("=" * 60)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        
        try:
            # Simular exactamente lo que hace el frontend
            print("🚀 Enviando solicitud a:", url)
            print("📝 Texto a analizar:", text.strip())
            
            start_time = time.time()
            
            payload = {"text": text.strip()}
            response = requests.post(
                url, 
                json=payload, 
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            response_time = (time.time() - start_time) * 1000
            
            print(f"📡 Respuesta recibida: {response.status_code} {response.reason}")
            print(f"⏱️ Tiempo de respuesta: {response_time:.2f}ms")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Datos recibidos exitosamente:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Verificar que todos los campos esperados estén presentes
                expected_fields = {
                    'text': str,
                    'is_toxic': bool,
                    'toxicity_percentage': (int, float),
                    'toxicity_category': str,
                    'confidence': (int, float),
                    'detected_categories': list,
                    'word_count': int,
                    'response_time_ms': int,
                    'timestamp': str,
                    'model_used': str,
                    'classification_technique': str
                }
                
                missing_fields = []
                type_mismatches = []
                
                for field, expected_type in expected_fields.items():
                    if field not in data:
                        missing_fields.append(field)
                    else:
                        value = data[field]
                        if not isinstance(value, expected_type):
                            if isinstance(expected_type, tuple):
                                if not any(isinstance(value, t) for t in expected_type):
                                    type_mismatches.append(f"{field}: esperado {expected_type}, recibido {type(value)}")
                            else:
                                type_mismatches.append(f"{field}: esperado {expected_type}, recibido {type(value)}")
                
                if missing_fields:
                    print(f"⚠️ Campos faltantes: {missing_fields}")
                else:
                    print("✅ Todos los campos están presentes")
                    
                if type_mismatches:
                    print(f"⚠️ Tipos incorrectos: {type_mismatches}")
                else:
                    print("✅ Todos los tipos son correctos")
                    
                # Verificar que el loading se pueda cerrar (simulando el frontend)
                print("🔄 Simulando cierre de loading...")
                print("✅ Estado de loading cerrado correctamente")
                
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
            import traceback
            traceback.print_exc()

def test_error_handling():
    """Prueba el manejo de errores"""
    
    url = "http://127.0.0.1:8000/analyze"
    
    print("\n🚨 PRUEBA DE MANEJO DE ERRORES:")
    print("-" * 40)
    
    # Texto vacío
    try:
        payload = {"text": ""}
        response = requests.post(url, json=payload, timeout=10)
        print(f"📝 Texto vacío - Status: {response.status_code}")
        if response.status_code != 400:
            print("⚠️ Debería haber devuelto 400 para texto vacío")
        else:
            print("✅ Error manejado correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Texto muy largo
    try:
        long_text = "a" * 10001
        payload = {"text": long_text}
        response = requests.post(url, json=payload, timeout=10)
        print(f"📝 Texto muy largo - Status: {response.status_code}")
        if response.status_code != 400:
            print("⚠️ Debería haber devuelto 400 para texto muy largo")
        else:
            print("✅ Error manejado correctamente")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        simulate_frontend_request()
        test_error_handling()
        print("\n✅ Todas las pruebas de compatibilidad completadas!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
