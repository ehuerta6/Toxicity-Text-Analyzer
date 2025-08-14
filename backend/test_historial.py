#!/usr/bin/env python3
"""
Script de prueba para el sistema de historial de ToxiGuard
Paso 3: Historial de análisis
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:8000"

def test_analyze_and_save():
    """Prueba análisis y guardado en historial"""
    print("🧪 Probando análisis y guardado en historial...")
    
    test_texts = [
        "Hola, ¡qué bonito día!",
        "Eres un idiota estúpido",
        "Me encanta esta nueva tecnología",
        "Vete al diablo, nadie te quiere aquí",
        "¡Excelente trabajo en el proyecto!"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Análisis {i}: {text[:30]}...")
        
        response = requests.post(f"{BASE_URL}/analyze", json={"text": text})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Resultado: {'Tóxico' if result.get('toxic') else 'Seguro'} ({result.get('toxicity_percentage', 0):.1f}%)")
            print(f"   📊 Categoría: {result.get('category', 'N/A')}")
            print(f"   ⏱️ Tiempo: {result.get('response_time_ms', 0):.2f}ms")
        else:
            print(f"   ❌ Error: {response.status_code}")
        
        time.sleep(0.5)  # Pausa entre análisis

def test_history_endpoints():
    """Prueba todos los endpoints de historial"""
    print("\n🔍 Probando endpoints de historial...")
    
    # Obtener historial
    print("\n📋 Obteniendo historial...")
    response = requests.get(f"{BASE_URL}/history")
    if response.status_code == 200:
        history = response.json()
        print(f"   ✅ Historial obtenido: {len(history.get('history', []))} análisis")
        if history.get('history'):
            latest = history['history'][0]
            print(f"   📄 Último análisis: {latest.get('text', '')[:30]}...")
    else:
        print(f"   ❌ Error obteniendo historial: {response.status_code}")
    
    # Obtener estadísticas
    print("\n📊 Obteniendo estadísticas...")
    response = requests.get(f"{BASE_URL}/history/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   ✅ Estadísticas obtenidas:")
        print(f"   📈 Total: {stats.get('total_analyses', 0)}")
        print(f"   🟢 Seguros: {stats.get('safe_analyses', 0)}")
        print(f"   🔴 Tóxicos: {stats.get('toxic_analyses', 0)}")
        print(f"   📊 Tasa tóxica: {stats.get('toxicity_rate', 0):.1f}%")
        print(f"   📋 Categorías: {len(stats.get('categories', {}))}")
    else:
        print(f"   ❌ Error obteniendo estadísticas: {response.status_code}")
    
    # Buscar en historial
    print("\n🔍 Probando búsqueda en historial...")
    response = requests.get(f"{BASE_URL}/history/search", params={"q": "idiota"})
    if response.status_code == 200:
        search_results = response.json()
        print(f"   ✅ Búsqueda realizada: {len(search_results.get('results', []))} resultados")
    else:
        print(f"   ❌ Error en búsqueda: {response.status_code}")

def test_server_connection():
    """Verifica la conexión con el servidor"""
    print("🔗 Verificando conexión con el servidor...")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Servidor funcionando correctamente")
            return True
        else:
            print(f"   ⚠️ Servidor responde con código: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ No se pudo conectar al servidor: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("🚀 PRUEBA COMPLETA DEL SISTEMA DE HISTORIAL")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 URL Base: {BASE_URL}")
    
    # Verificar conexión
    if not test_server_connection():
        print("\n❌ No se puede continuar sin conexión al servidor")
        return
    
    # Realizar análisis para generar historial
    test_analyze_and_save()
    
    # Probar endpoints de historial
    test_history_endpoints()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print("\n📱 Ahora puedes:")
    print("   1. Abrir http://localhost:5173 para ver el frontend")
    print("   2. Hacer clic en 'Ver Historial' para ver los análisis")
    print("   3. Hacer clic en 'Ver Gráficos' para ver las visualizaciones")
    print("   4. Probar los diferentes gráficos: pastel, barras y categorías")

if __name__ == "__main__":
    main()
