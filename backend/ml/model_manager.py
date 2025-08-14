#!/usr/bin/env python3
"""
🔧 ToxiGuard Model Manager
Sistema de gestión avanzada de modelos ML para detección de toxicidad
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report
import pickle

# Configuración de paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data"

# Agregar path del proyecto
sys.path.append(str(PROJECT_ROOT))
from backend.ml.preprocess import preprocess_text

class ModelManager:
    """Gestor avanzado de modelos ML para ToxiGuard"""
    
    def __init__(self):
        self.models_dir = MODELS_DIR
        self.data_dir = DATA_DIR
        self.models_dir.mkdir(exist_ok=True)
        
        # Metadatos del modelo
        self.metadata_path = self.models_dir / "model_metadata.json"
        self.backup_dir = self.models_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def get_model_metadata(self) -> Dict:
        """Obtiene los metadatos del modelo actual"""
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_model_metadata(self, metadata: Dict):
        """Guarda los metadatos del modelo"""
        metadata['last_updated'] = datetime.now().isoformat()
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def is_model_trained(self) -> bool:
        """Verifica si existe un modelo entrenado"""
        model_path = self.models_dir / "toxic_model.pkl"
        vectorizer_path = self.models_dir / "vectorizer.pkl"
        return model_path.exists() and vectorizer_path.exists()
    
    def get_model_age(self) -> Optional[timedelta]:
        """Obtiene la antigüedad del modelo actual"""
        metadata = self.get_model_metadata()
        if 'last_updated' in metadata:
            last_updated = datetime.fromisoformat(metadata['last_updated'])
            return datetime.now() - last_updated
        return None
    
    def needs_retraining(self, max_age_days: int = 30) -> bool:
        """Determina si el modelo necesita reentrenamiento"""
        if not self.is_model_trained():
            return True
        
        age = self.get_model_age()
        if age and age.days > max_age_days:
            return True
        
        # Verificar si hay datos nuevos
        metadata = self.get_model_metadata()
        last_data_count = metadata.get('training_samples', 0)
        current_data_count = self._get_current_data_count()
        
        # Reentrenar si hay más de 20% de datos nuevos
        if current_data_count > last_data_count * 1.2:
            return True
        
        return False
    
    def _get_current_data_count(self) -> int:
        """Obtiene el conteo actual de datos"""
        dataset_path = self.data_dir / "toxic_comments_processed.csv"
        if dataset_path.exists():
            df = pd.read_csv(dataset_path)
            return len(df)
        return 0
    
    def backup_current_model(self) -> bool:
        """Crea un backup del modelo actual"""
        if not self.is_model_trained():
            print("⚠️  No hay modelo actual para respaldar")
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_subdir = self.backup_dir / f"model_backup_{timestamp}"
            backup_subdir.mkdir(exist_ok=True)
            
            # Copiar archivos del modelo
            model_files = [
                "toxic_model.pkl",
                "vectorizer.pkl", 
                "model_info.txt",
                "model_metadata.json"
            ]
            
            for file_name in model_files:
                src_path = self.models_dir / file_name
                if src_path.exists():
                    dst_path = backup_subdir / file_name
                    import shutil
                    shutil.copy2(src_path, dst_path)
            
            print(f"✅ Backup creado: {backup_subdir}")
            return True
            
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return False
    
    def load_current_model(self) -> Tuple[Optional[object], Optional[object]]:
        """Carga el modelo y vectorizador actuales"""
        try:
            model_path = self.models_dir / "toxic_model.pkl"
            vectorizer_path = self.models_dir / "vectorizer.pkl"
            
            if not (model_path.exists() and vectorizer_path.exists()):
                return None, None
            
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            
            return model, vectorizer
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return None, None
    
    def incremental_training(self, new_data: pd.DataFrame) -> bool:
        """
        Realiza entrenamiento incremental con nuevos datos
        """
        print("🔄 INICIANDO ENTRENAMIENTO INCREMENTAL")
        print("=" * 50)
        
        # Verificar que existe un modelo base
        if not self.is_model_trained():
            print("❌ No hay modelo base. Use entrenamiento completo primero.")
            return False
        
        try:
            # Crear backup antes de actualizar
            self.backup_current_model()
            
            # Cargar modelo y vectorizador actuales
            current_model, current_vectorizer = self.load_current_model()
            if current_model is None:
                print("❌ No se pudo cargar el modelo actual")
                return False
            
            # Validar datos nuevos
            if 'text' not in new_data.columns or 'toxic' not in new_data.columns:
                print("❌ Los datos nuevos deben tener columnas 'text' y 'toxic'")
                return False
            
            print(f"📊 Procesando {len(new_data)} nuevas muestras...")
            
            # Preprocesar nuevos datos
            new_data['text_clean'] = new_data['text'].apply(preprocess_text)
            
            # Vectorizar con el vectorizador existente
            X_new = current_vectorizer.transform(new_data['text_clean'])
            y_new = new_data['toxic'].values
            
            # Realizar entrenamiento incremental (si el modelo lo soporta)
            if hasattr(current_model, 'partial_fit'):
                print("🔄 Entrenamiento incremental...")
                current_model.partial_fit(X_new, y_new)
            else:
                print("⚠️  Modelo no soporta entrenamiento incremental")
                print("🔄 Combinando con datos históricos...")
                
                # Cargar datos históricos
                historical_data = self._load_historical_data()
                if historical_data is not None:
                    # Combinar datos
                    combined_data = pd.concat([historical_data, new_data], ignore_index=True)
                    
                    # Reentrenar completamente
                    return self._retrain_with_combined_data(combined_data, current_vectorizer)
                else:
                    print("❌ No se pudieron cargar datos históricos")
                    return False
            
            # Guardar modelo actualizado
            self._save_updated_model(current_model, current_vectorizer, len(new_data))
            
            # Evaluar rendimiento
            self._evaluate_model(current_model, current_vectorizer, X_new, y_new)
            
            print("✅ Entrenamiento incremental completado")
            return True
            
        except Exception as e:
            print(f"❌ Error en entrenamiento incremental: {e}")
            return False
    
    def _load_historical_data(self) -> Optional[pd.DataFrame]:
        """Carga datos históricos de entrenamiento"""
        dataset_path = self.data_dir / "toxic_comments_processed.csv"
        if dataset_path.exists():
            return pd.read_csv(dataset_path)
        return None
    
    def _retrain_with_combined_data(self, combined_data: pd.DataFrame, vectorizer: object) -> bool:
        """Reentrena el modelo con datos combinados"""
        try:
            # Preparar datos
            X_text = combined_data['text_clean']
            y = combined_data['toxic'].values
            
            # Vectorizar
            X = vectorizer.transform(X_text)
            
            # Dividir en entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Reentrenar modelo (usar el tipo de modelo actual)
            current_model, _ = self.load_current_model()
            model_type = type(current_model)
            
            new_model = model_type()
            new_model.fit(X_train, y_train)
            
            # Evaluar
            y_pred = new_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            print(f"📊 Accuracy: {accuracy:.4f}")
            print(f"📊 F1-Score: {f1:.4f}")
            
            # Guardar modelo reentrenado
            self._save_updated_model(new_model, vectorizer, len(combined_data))
            
            return True
            
        except Exception as e:
            print(f"❌ Error en reentrenamiento: {e}")
            return False
    
    def _save_updated_model(self, model: object, vectorizer: object, training_samples: int):
        """Guarda el modelo actualizado"""
        try:
            # Guardar modelo
            model_path = self.models_dir / "toxic_model.pkl"
            joblib.dump(model, model_path)
            
            # Guardar vectorizador
            vectorizer_path = self.models_dir / "vectorizer.pkl"
            joblib.dump(vectorizer, vectorizer_path)
            
            # Actualizar metadatos
            metadata = self.get_model_metadata()
            metadata.update({
                'training_samples': training_samples,
                'model_type': type(model).__name__,
                'vectorizer_features': len(vectorizer.get_feature_names_out()),
                'last_training_type': 'incremental'
            })
            self.save_model_metadata(metadata)
            
            print(f"✅ Modelo actualizado guardado")
            
        except Exception as e:
            print(f"❌ Error guardando modelo: {e}")
    
    def _evaluate_model(self, model: object, vectorizer: object, X_test: object, y_test: object):
        """Evalúa el rendimiento del modelo"""
        try:
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            print(f"\n📊 EVALUACIÓN DEL MODELO")
            print(f"   Accuracy: {accuracy:.4f}")
            print(f"   F1-Score: {f1:.4f}")
            
        except Exception as e:
            print(f"❌ Error evaluando modelo: {e}")
    
    def get_model_status(self) -> Dict:
        """Obtiene el estado completo del modelo"""
        status = {
            'model_exists': self.is_model_trained(),
            'model_age': None,
            'needs_retraining': False,
            'metadata': self.get_model_metadata(),
            'backups_count': len(list(self.backup_dir.glob('model_backup_*')))
        }
        
        age = self.get_model_age()
        if age:
            status['model_age'] = f"{age.days} días"
            status['needs_retraining'] = self.needs_retraining()
        
        return status
    
    def cleanup_old_backups(self, keep_last: int = 5):
        """Limpia backups antiguos, manteniendo solo los más recientes"""
        try:
            backups = sorted(self.backup_dir.glob('model_backup_*'))
            if len(backups) > keep_last:
                for backup in backups[:-keep_last]:
                    import shutil
                    shutil.rmtree(backup)
                    print(f"🗑️  Backup eliminado: {backup.name}")
                print(f"✅ Limpieza completada. {keep_last} backups mantenidos.")
        except Exception as e:
            print(f"❌ Error limpiando backups: {e}")


def main():
    """Función principal de demostración"""
    manager = ModelManager()
    
    print("🔧 TOXIGUARD MODEL MANAGER")
    print("=" * 50)
    
    status = manager.get_model_status()
    print(f"📊 Estado del modelo:")
    print(f"   Existe: {'✅' if status['model_exists'] else '❌'}")
    print(f"   Edad: {status['model_age'] or 'N/A'}")
    print(f"   Necesita reentrenamiento: {'✅' if status['needs_retraining'] else '❌'}")
    print(f"   Backups disponibles: {status['backups_count']}")

if __name__ == "__main__":
    main()
