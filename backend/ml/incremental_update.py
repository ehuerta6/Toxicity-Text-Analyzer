#!/usr/bin/env python3
"""
🔄 ToxiGuard Incremental Update Script
Script para actualizaciones incrementales del modelo ML
"""

import sys
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime

# Configuración de paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.ml.model_manager import ModelManager

def load_new_data_from_csv(csv_path: str) -> pd.DataFrame:
    """
    Carga nuevos datos desde un archivo CSV
    El CSV debe tener las columnas: text, toxic
    """
    try:
        df = pd.read_csv(csv_path)
        
        # Validar columnas requeridas
        required_columns = ['text', 'toxic']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Columnas faltantes: {missing_columns}")
        
        # Convertir la columna toxic a int
        df['toxic'] = df['toxic'].astype(int)
        
        print(f"✅ Datos cargados: {len(df)} muestras")
        print(f"   Tóxicos: {df['toxic'].sum()}")
        print(f"   No tóxicos: {len(df) - df['toxic'].sum()}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        raise

def simulate_new_data(num_samples: int = 100) -> pd.DataFrame:
    """
    Simula nuevos datos para pruebas
    """
    import random
    
    # Datos de ejemplo para pruebas
    toxic_examples = [
        "eres un idiota",
        "vete al diablo",
        "odio este lugar",
        "esto es una mierda",
        "que pendejo eres",
        "fuck you asshole",
        "go to hell",
        "you are stupid",
        "damn this shit",
        "stupid moron"
    ]
    
    safe_examples = [
        "buenos días a todos",
        "gracias por la ayuda",
        "excelente trabajo",
        "me gusta mucho",
        "muy interesante",
        "good morning everyone",
        "thank you for helping",
        "excellent work",
        "I really like it",
        "very interesting"
    ]
    
    data = []
    for _ in range(num_samples):
        if random.random() < 0.3:  # 30% tóxicos
            text = random.choice(toxic_examples)
            toxic = 1
        else:  # 70% seguros
            text = random.choice(safe_examples)
            toxic = 0
        
        # Agregar variaciones
        if random.random() < 0.5:
            text = text + " " + random.choice(["por favor", "gracias", "eh", "jaja"])
        
        data.append({'text': text, 'toxic': toxic})
    
    df = pd.DataFrame(data)
    print(f"🎲 Datos simulados generados: {len(df)} muestras")
    return df

def incremental_update_from_history():
    """
    Realiza actualización incremental usando datos del historial de la aplicación
    """
    print("🔄 ACTUALIZACIÓN DESDE HISTORIAL")
    print("=" * 50)
    
    try:
        # Conectar a la base de datos de historial
        import sqlite3
        import json
        
        db_path = PROJECT_ROOT / "backend" / "history.db"
        if not db_path.exists():
            print("❌ Base de datos de historial no encontrada")
            return False
        
        # Leer datos del historial
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT text, result_json 
            FROM analysis_history 
            WHERE created_at >= datetime('now', '-7 days')
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("⚠️  No hay datos nuevos en el historial (últimos 7 días)")
            return False
        
        # Procesar datos del historial
        data = []
        for text, result_json in rows:
            try:
                result = json.loads(result_json)
                toxic = 1 if result.get('toxic', False) else 0
                data.append({'text': text, 'toxic': toxic})
            except:
                continue
        
        if not data:
            print("❌ No se pudieron procesar datos del historial")
            return False
        
        new_data = pd.DataFrame(data)
        print(f"📊 Datos del historial procesados: {len(new_data)} muestras")
        
        # Realizar actualización incremental
        manager = ModelManager()
        return manager.incremental_training(new_data)
        
    except Exception as e:
        print(f"❌ Error en actualización desde historial: {e}")
        return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Actualización incremental del modelo ToxiGuard")
    parser.add_argument('--csv', type=str, help='Archivo CSV con nuevos datos')
    parser.add_argument('--simulate', type=int, default=0, help='Generar datos simulados (número de muestras)')
    parser.add_argument('--from-history', action='store_true', help='Usar datos del historial de la aplicación')
    parser.add_argument('--status', action='store_true', help='Mostrar estado del modelo')
    
    args = parser.parse_args()
    
    print("🔄 TOXIGUARD - ACTUALIZACIÓN INCREMENTAL")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    manager = ModelManager()
    
    # Mostrar estado si se solicita
    if args.status:
        status = manager.get_model_status()
        print("📊 ESTADO DEL MODELO")
        print("-" * 30)
        print(f"   Modelo entrenado: {'✅' if status['model_exists'] else '❌'}")
        print(f"   Edad del modelo: {status['model_age'] or 'N/A'}")
        print(f"   Necesita reentrenamiento: {'✅' if status['needs_retraining'] else '❌'}")
        print(f"   Backups disponibles: {status['backups_count']}")
        
        if status['metadata']:
            metadata = status['metadata']
            print(f"   Muestras de entrenamiento: {metadata.get('training_samples', 'N/A'):,}")
            print(f"   Tipo de modelo: {metadata.get('model_type', 'N/A')}")
            print(f"   Características: {metadata.get('vectorizer_features', 'N/A'):,}")
        print()
    
    # Verificar si hay modelo base
    if not manager.is_model_trained():
        print("❌ No hay modelo base entrenado.")
        print("🔧 Ejecute primero el entrenamiento completo:")
        print("   cd backend/ml && python train_model.py")
        return
    
    # Procesar según argumentos
    success = False
    
    if args.csv:
        print(f"📁 Cargando datos desde: {args.csv}")
        try:
            new_data = load_new_data_from_csv(args.csv)
            success = manager.incremental_training(new_data)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif args.simulate > 0:
        print(f"🎲 Generando {args.simulate} datos simulados...")
        new_data = simulate_new_data(args.simulate)
        success = manager.incremental_training(new_data)
    
    elif args.from_history:
        success = incremental_update_from_history()
    
    else:
        print("🤖 Modo automático: Verificando si se necesita actualización...")
        
        if manager.needs_retraining():
            print("✅ El modelo necesita actualización")
            print("🔄 Intentando actualización desde historial...")
            success = incremental_update_from_history()
            
            if not success:
                print("⚠️  No hay datos nuevos en historial")
                print("💡 Considere usar datos simulados:")
                print("   python incremental_update.py --simulate 50")
        else:
            print("✅ El modelo está actualizado, no se requiere entrenamiento")
            success = True
    
    # Resultado final
    print("\n" + "=" * 60)
    if success:
        print("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        
        # Mostrar estado actualizado
        status = manager.get_model_status()
        if status['metadata']:
            metadata = status['metadata']
            print(f"📊 Muestras totales: {metadata.get('training_samples', 'N/A'):,}")
            print(f"🕒 Última actualización: {metadata.get('last_updated', 'N/A')}")
    else:
        print("❌ ACTUALIZACIÓN FALLÓ")
        print("🔧 Verifique los logs anteriores para más detalles")

if __name__ == "__main__":
    main()
