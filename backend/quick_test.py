#!/usr/bin/env python3
"""
Script de prueba rápida para verificar el backend de ToxiGuard
"""

import requests
import time

def quick_test():
    """Prueba rápida del backend"""
    print("🚀 PRUEBA RÁPIDA DEL BACKEND - ToxiGuard")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # 1. Probar salud del backend
    print("\n🏥 1. Probando salud del backend...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Backend funcionando")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except:
        print("   ❌ No se puede conectar al backend")
        return False
    
    # 2. Probar estado del modelo ML
    print("\n🤖 2. Probando estado del modelo ML...")
    try:
        response = requests.get(f"{base_url}/ml/status")
        if response.status_code == 200:
            status = response.json()
            print(f"   📊 Estado: {status['status']}")
            print(f"   📥 Modelo cargado: {status['model_loaded']}")
            if status['model_loaded']:
                print("   ✅ Modelo ML listo")
            else:
                print("   ⚠️  Modelo ML no cargado")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Probar endpoint de análisis
    print("\n🔍 3. Probando endpoint de análisis...")
    test_texts = [
        "Hello world! This is a nice comment.",
        "You are an idiot and I hate you!",
        "Thank you for your help."
    ]
    
    for i, text in enumerate(test_texts, 1):
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/analyze",
                json={"text": text}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"   📝 Texto {i}: {'Tóxico' if result['toxic'] else 'No Tóxico'}")
                print(f"      Score: {result['score']:.3f}")
                print(f"      Tiempo: {response_time:.3f}s")
            else:
                print(f"   ❌ Error en texto {i}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error en texto {i}: {e}")
    
    print("\n✅ Prueba rápida completada!")
    return True

if __name__ == "__main__":
    quick_test()
