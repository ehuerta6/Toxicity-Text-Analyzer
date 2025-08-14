#!/usr/bin/env python3
"""
🚀 ToxiGuard Manual Retrain Script
Script para reentrenamiento manual completo del modelo ML
"""

import sys
import os
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Configuración de paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.ml.model_manager import ModelManager
from backend.ml.train_model import main as train_main

def backup_current_model():
    """Crea backup del modelo actual"""
    manager = ModelManager()
    return manager.backup_current_model()

def retrain_with_backup():
    """Reentrena el modelo creando backup automático"""
    print("🚀 REENTRENAMIENTO COMPLETO CON BACKUP")
    print("=" * 60)
    
    try:
        manager = ModelManager()
        
        # Crear backup si existe modelo actual
        if manager.is_model_trained():
            print("💾 Creando backup del modelo actual...")
            if backup_current_model():
                print("✅ Backup creado exitosamente")
            else:
                print("⚠️  No se pudo crear backup, continuando...")
        
        # Ejecutar entrenamiento completo
        print("\n🔄 Iniciando entrenamiento completo...")
        print("=" * 40)
        
        # Cambiar al directorio ML para ejecutar entrenamiento
        original_cwd = os.getcwd()
        try:
            os.chdir(SCRIPT_DIR)
            
            # Ejecutar entrenamiento usando el script existente
            train_main()
            
            print("\n✅ REENTRENAMIENTO COMPLETADO")
            return True
            
        finally:
            os.chdir(original_cwd)
            
    except Exception as e:
        print(f"❌ Error en reentrenamiento: {e}")
        return False

def force_retrain():
    """Fuerza reentrenamiento eliminando modelo actual"""
    print("🔥 REENTRENAMIENTO FORZADO")
    print("=" * 40)
    print("⚠️  ADVERTENCIA: Se eliminará el modelo actual sin backup")
    
    confirmation = input("¿Continuar? (y/N): ").lower().strip()
    if confirmation != 'y':
        print("❌ Operación cancelada")
        return False
    
    try:
        manager = ModelManager()
        models_dir = manager.models_dir
        
        # Eliminar archivos del modelo actual
        model_files = [
            "toxic_model.pkl",
            "vectorizer.pkl",
            "all_models.pkl",
            "model_info.txt",
            "model_metadata.json"
        ]
        
        for file_name in model_files:
            file_path = models_dir / file_name
            if file_path.exists():
                file_path.unlink()
                print(f"🗑️  Eliminado: {file_name}")
        
        # Ejecutar reentrenamiento
        print("\n🔄 Iniciando entrenamiento desde cero...")
        return retrain_with_backup()
        
    except Exception as e:
        print(f"❌ Error en reentrenamiento forzado: {e}")
        return False

def quick_retrain():
    """Reentrenamiento rápido con configuración optimizada"""
    print("⚡ REENTRENAMIENTO RÁPIDO")
    print("=" * 40)
    
    try:
        # Crear backup
        backup_current_model()
        
        # Modificar temporalmente la configuración para entrenamiento rápido
        config_path = SCRIPT_DIR / "config.py"
        backup_config = None
        
        if config_path.exists():
            # Hacer backup de la configuración
            backup_config = config_path.read_text(encoding='utf-8')
            
            # Modificar para entrenamiento rápido
            quick_config = backup_config.replace(
                "MODELS_TO_TRAIN = [", 
                "# MODELS_TO_TRAIN = ["
            ).replace(
                "# Quick config for testing",
                "MODELS_TO_TRAIN = ['LogisticRegression']  # Solo modelo rápido"
            )
            
            config_path.write_text(quick_config, encoding='utf-8')
        
        # Ejecutar entrenamiento
        original_cwd = os.getcwd()
        try:
            os.chdir(SCRIPT_DIR)
            train_main()
            success = True
        finally:
            os.chdir(original_cwd)
            
            # Restaurar configuración original
            if backup_config:
                config_path.write_text(backup_config, encoding='utf-8')
        
        print("✅ Reentrenamiento rápido completado")
        return success
        
    except Exception as e:
        print(f"❌ Error en reentrenamiento rápido: {e}")
        return False

def show_model_info():
    """Muestra información detallada del modelo"""
    manager = ModelManager()
    
    print("📊 INFORMACIÓN DEL MODELO")
    print("=" * 40)
    
    if not manager.is_model_trained():
        print("❌ No hay modelo entrenado")
        return
    
    # Información básica
    status = manager.get_model_status()
    print(f"✅ Modelo entrenado: {'Sí' if status['model_exists'] else 'No'}")
    print(f"🕒 Edad: {status['model_age'] or 'N/A'}")
    print(f"🔄 Necesita reentrenamiento: {'Sí' if status['needs_retraining'] else 'No'}")
    print(f"💾 Backups: {status['backups_count']}")
    
    # Metadatos
    metadata = status['metadata']
    if metadata:
        print(f"\n📋 METADATOS:")
        print(f"   Muestras de entrenamiento: {metadata.get('training_samples', 'N/A'):,}")
        print(f"   Tipo de modelo: {metadata.get('model_type', 'N/A')}")
        print(f"   Características TF-IDF: {metadata.get('vectorizer_features', 'N/A'):,}")
        print(f"   Última actualización: {metadata.get('last_updated', 'N/A')}")
        print(f"   Tipo de entrenamiento: {metadata.get('last_training_type', 'N/A')}")
    
    # Información de archivos
    models_dir = manager.models_dir
    print(f"\n📁 ARCHIVOS:")
    model_files = [
        ("toxic_model.pkl", "Modelo principal"),
        ("vectorizer.pkl", "Vectorizador TF-IDF"),
        ("all_models.pkl", "Todos los modelos"),
        ("model_info.txt", "Información de entrenamiento"),
        ("model_metadata.json", "Metadatos JSON")
    ]
    
    for file_name, description in model_files:
        file_path = models_dir / file_name
        if file_path.exists():
            size_mb = file_path.stat().st_size / 1024 / 1024
            print(f"   ✅ {file_name}: {description} ({size_mb:.1f} MB)")
        else:
            print(f"   ❌ {file_name}: No encontrado")
    
    # Backups disponibles
    backups = list(manager.backup_dir.glob('model_backup_*'))
    if backups:
        print(f"\n💾 BACKUPS DISPONIBLES:")
        for backup in sorted(backups, reverse=True)[:5]:  # Últimos 5
            backup_date = backup.name.replace('model_backup_', '')
            print(f"   📦 {backup_date}")

def restore_from_backup():
    """Restaura modelo desde backup"""
    manager = ModelManager()
    backups = list(manager.backup_dir.glob('model_backup_*'))
    
    if not backups:
        print("❌ No hay backups disponibles")
        return False
    
    print("💾 BACKUPS DISPONIBLES:")
    print("=" * 30)
    
    for i, backup in enumerate(sorted(backups, reverse=True), 1):
        backup_date = backup.name.replace('model_backup_', '')
        print(f"{i}. {backup_date}")
    
    try:
        choice = input(f"\nSeleccione backup (1-{len(backups)}) o 'q' para cancelar: ").strip()
        
        if choice.lower() == 'q':
            print("❌ Operación cancelada")
            return False
        
        backup_index = int(choice) - 1
        selected_backup = sorted(backups, reverse=True)[backup_index]
        
        print(f"🔄 Restaurando desde: {selected_backup.name}")
        
        # Crear backup del estado actual antes de restaurar
        if manager.is_model_trained():
            manager.backup_current_model()
        
        # Copiar archivos del backup
        model_files = ["toxic_model.pkl", "vectorizer.pkl", "model_info.txt", "model_metadata.json"]
        
        for file_name in model_files:
            src_path = selected_backup / file_name
            dst_path = manager.models_dir / file_name
            
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                print(f"✅ Restaurado: {file_name}")
        
        print("✅ Restauración completada")
        return True
        
    except (ValueError, IndexError):
        print("❌ Selección inválida")
        return False
    except Exception as e:
        print(f"❌ Error en restauración: {e}")
        return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Reentrenamiento manual del modelo ToxiGuard")
    parser.add_argument('--full', action='store_true', help='Reentrenamiento completo con backup')
    parser.add_argument('--force', action='store_true', help='Reentrenamiento forzado (sin backup)')
    parser.add_argument('--quick', action='store_true', help='Reentrenamiento rápido')
    parser.add_argument('--info', action='store_true', help='Mostrar información del modelo')
    parser.add_argument('--backup', action='store_true', help='Crear backup del modelo actual')
    parser.add_argument('--restore', action='store_true', help='Restaurar desde backup')
    parser.add_argument('--cleanup', action='store_true', help='Limpiar backups antiguos')
    
    args = parser.parse_args()
    
    print("🚀 TOXIGUARD - REENTRENAMIENTO MANUAL")
    print("=" * 60)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    manager = ModelManager()
    
    # Ejecutar según argumentos
    if args.info:
        show_model_info()
    
    elif args.backup:
        print("💾 Creando backup manual...")
        if backup_current_model():
            print("✅ Backup creado exitosamente")
        else:
            print("❌ Error creando backup")
    
    elif args.restore:
        restore_from_backup()
    
    elif args.cleanup:
        print("🗑️  Limpiando backups antiguos...")
        manager.cleanup_old_backups()
    
    elif args.force:
        force_retrain()
    
    elif args.quick:
        quick_retrain()
    
    elif args.full:
        retrain_with_backup()
    
    else:
        # Modo interactivo
        print("🤖 MODO INTERACTIVO")
        print("-" * 20)
        show_model_info()
        
        print(f"\n🔧 OPCIONES DISPONIBLES:")
        print("1. Reentrenamiento completo (con backup)")
        print("2. Reentrenamiento rápido")
        print("3. Crear backup manual")
        print("4. Restaurar desde backup")
        print("5. Limpiar backups antiguos")
        print("6. Salir")
        
        try:
            choice = input("\nSeleccione opción (1-6): ").strip()
            
            if choice == '1':
                retrain_with_backup()
            elif choice == '2':
                quick_retrain()
            elif choice == '3':
                backup_current_model()
            elif choice == '4':
                restore_from_backup()
            elif choice == '5':
                manager.cleanup_old_backups()
            elif choice == '6':
                print("👋 ¡Hasta luego!")
            else:
                print("❌ Opción inválida")
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")

if __name__ == "__main__":
    main()
