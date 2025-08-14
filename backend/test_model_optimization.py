#!/usr/bin/env python3
"""
🧪 Test Model Optimization Scripts
Script para probar las funcionalidades de optimización del modelo
"""

import sys
import requests
import time
from pathlib import Path

# Configuración
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

BACKEND_URL = "http://127.0.0.1:8000"

def test_endpoints():
    """Prueba los nuevos endpoints de gestión del modelo"""
    print("🧪 PRUEBA DE ENDPOINTS DE GESTIÓN DEL MODELO")
    print("=" * 60)
    
    endpoints_to_test = [
        ("GET", "/model/status", "Estado del modelo"),
        ("GET", "/model/needs-retrain", "Verificar necesidad de reentrenamiento"),
        ("POST", "/model/backup", "Crear backup"),
        ("POST", "/model/reload", "Recargar modelo")
    ]
    
    for method, endpoint, description in endpoints_to_test:
        print(f"\n🔍 Probando: {description}")
        print(f"   {method} {endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(f"{BACKEND_URL}{endpoint}")
            else:
                response = requests.post(f"{BACKEND_URL}{endpoint}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Éxito: {response.status_code}")
                
                # Mostrar información relevante
                if endpoint == "/model/status":
                    print(f"      Modelo entrenado: {result.get('model_exists')}")
                    print(f"      Edad: {result.get('model_age')}")
                    print(f"      Servidor cargado: {result.get('server_model_loaded')}")
                    
                elif endpoint == "/model/needs-retrain":
                    print(f"      Necesita reentrenamiento: {result.get('needs_retraining')}")
                    print(f"      Recomendación: {result.get('recommendation')}")
                    
                elif endpoint == "/model/backup":
                    print(f"      Backup creado: {result.get('backup_created')}")
                    
                elif endpoint == "/model/reload":
                    print(f"      Modelo cargado: {result.get('model_loaded')}")
                    print(f"      Tipo: {result.get('model_type')}")
                    
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"      {response.text}")
                
        except Exception as e:
            print(f"   ❌ Excepción: {e}")

def test_model_manager():
    """Prueba el ModelManager directamente"""
    print("\n🔧 PRUEBA DEL MODEL MANAGER")
    print("=" * 40)
    
    try:
        from backend.ml.model_manager import ModelManager
        
        manager = ModelManager()
        
        # Estado del modelo
        print("📊 Estado del modelo:")
        status = manager.get_model_status()
        print(f"   Existe: {status['model_exists']}")
        print(f"   Edad: {status['model_age']}")
        print(f"   Necesita reentrenamiento: {status['needs_retraining']}")
        print(f"   Backups: {status['backups_count']}")
        
        # Metadatos
        if status['metadata']:
            metadata = status['metadata']
            print(f"\n📋 Metadatos:")
            print(f"   Muestras: {metadata.get('training_samples', 'N/A')}")
            print(f"   Tipo: {metadata.get('model_type', 'N/A')}")
            print(f"   Última actualización: {metadata.get('last_updated', 'N/A')}")
        
        print("\n✅ ModelManager funcionando correctamente")
        
    except Exception as e:
        print(f"❌ Error en ModelManager: {e}")

def test_scripts_import():
    """Prueba que se puedan importar los scripts"""
    print("\n📦 PRUEBA DE IMPORTS")
    print("=" * 30)
    
    scripts_to_test = [
        ("backend.ml.model_manager", "ModelManager"),
        ("backend.ml.incremental_update", "Script de actualización incremental"),
        ("backend.ml.retrain_model", "Script de reentrenamiento"),
    ]
    
    for module_name, description in scripts_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}: Import exitoso")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")

def main():
    """Función principal"""
    print("🚀 TOXIGUARD - PRUEBA DE OPTIMIZACIÓN DEL MODELO")
    print("=" * 70)
    print(f"⏰ Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print()
    
    # Verificar conectividad del backend
    print("🔌 Verificando conectividad del backend...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            print("✅ Backend conectado")
        else:
            print(f"⚠️ Backend responde con código: {response.status_code}")
    except:
        print("❌ Backend no disponible")
        print("🔧 Asegúrese de que el backend esté ejecutándose:")
        print("   cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        return
    
    # Ejecutar pruebas
    test_scripts_import()
    test_model_manager()
    test_endpoints()
    
    print("\n" + "=" * 70)
    print("✅ PRUEBAS COMPLETADAS")
    print("\n🔧 SCRIPTS DISPONIBLES:")
    print("   📊 Estado del modelo: python backend/ml/model_manager.py")
    print("   🔄 Actualización incremental: python backend/ml/incremental_update.py --status")
    print("   🚀 Reentrenamiento manual: python backend/ml/retrain_model.py --info")
    print("\n📡 ENDPOINTS DISPONIBLES:")
    print("   GET /model/status - Estado del modelo")
    print("   GET /model/needs-retrain - Verificar reentrenamiento")
    print("   POST /model/backup - Crear backup")
    print("   POST /model/reload - Recargar modelo")

if __name__ == "__main__":
    main()
