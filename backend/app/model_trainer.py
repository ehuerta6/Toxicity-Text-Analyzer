"""
🎯 Entrenador de Modelos ML - ToxiGuard
Sistema para entrenar, evaluar y comparar diferentes modelos de clasificación de toxicidad
"""

import logging
import json
import os
from typing import List, Dict, Tuple, Any
from datetime import datetime
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

from .ml_models import MLToxicityClassifier

# Configurar logging
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Entrenador y evaluador de modelos ML para toxicidad"""
    
    def __init__(self, models_dir: str = "models"):
        """
        Inicializa el entrenador de modelos
        
        Args:
            models_dir: Directorio donde guardar los modelos entrenados
        """
        self.models_dir = models_dir
        self.results_history = []
        
        # Crear directorio si no existe
        os.makedirs(models_dir, exist_ok=True)
        
        # Configuración de hiperparámetros para Grid Search
        self.hyperparameter_grids = {
            "logistic_regression": {
                "classifier__C": [0.1, 1.0, 10.0],
                "classifier__penalty": ["l1", "l2"],
                "classifier__solver": ["liblinear", "saga"]
            },
            "random_forest": {
                "classifier__n_estimators": [50, 100, 200],
                "classifier__max_depth": [10, 20, None],
                "classifier__min_samples_split": [2, 5, 10]
            },
            "naive_bayes": {
                "classifier__alpha": [0.1, 0.5, 1.0, 2.0]
            }
        }
        
        logger.info(f"Entrenador de modelos inicializado en: {models_dir}")
    
    def prepare_training_data(self, data_path: str) -> Tuple[List[str], List[int]]:
        """
        Prepara datos de entrenamiento desde un archivo CSV
        
        Args:
            data_path: Ruta al archivo CSV con datos de entrenamiento
            
        Returns:
            Tuple con (textos, etiquetas)
        """
        try:
            # Cargar datos
            df = pd.read_csv(data_path)
            
            # Verificar columnas requeridas
            required_columns = ["text", "label"]
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"El CSV debe contener las columnas: {required_columns}")
            
            # Limpiar datos
            df = df.dropna(subset=["text", "label"])
            df = df[df["text"].str.strip() != ""]
            
            # Convertir etiquetas a formato numérico si es necesario
            if df["label"].dtype == "object":
                # Mapear etiquetas de texto a números
                label_mapping = {"toxic": 1, "non-toxic": 0, "hate": 1, "normal": 0}
                df["label"] = df["label"].map(label_mapping)
            
            texts = df["text"].tolist()
            labels = df["label"].tolist()
            
            logger.info(f"Datos preparados: {len(texts)} muestras")
            return texts, labels
            
        except Exception as e:
            logger.error(f"Error preparando datos: {e}")
            raise
    
    def train_single_model(self, model_type: str, texts: List[str], labels: List[int],
                          use_grid_search: bool = False) -> Tuple[MLToxicityClassifier, Dict[str, Any]]:
        """
        Entrena un modelo individual
        
        Args:
            model_type: Tipo de modelo a entrenar
            texts: Lista de textos de entrenamiento
            labels: Lista de etiquetas de entrenamiento
            use_grid_search: Si usar Grid Search para optimización
            
        Returns:
            Tuple con (modelo entrenado, métricas de entrenamiento)
        """
        try:
            logger.info(f"Entrenando modelo: {model_type}")
            
            # Crear clasificador
            classifier = MLToxicityClassifier(model_type)
            
            if use_grid_search:
                # Usar Grid Search para optimización
                grid_search = GridSearchCV(
                    classifier.pipeline,
                    self.hyperparameter_grids.get(model_type, {}),
                    cv=5,
                    scoring='f1',
                    n_jobs=-1
                )
                
                grid_search.fit(texts, labels)
                
                # Actualizar modelo con mejores parámetros
                classifier.pipeline = grid_search.best_estimator_
                best_params = grid_search.best_params_
                
                logger.info(f"Mejores parámetros: {best_params}")
            else:
                # Entrenamiento directo
                classifier.pipeline.fit(texts, labels)
                best_params = {}
            
            # Evaluar modelo
            y_pred = classifier.pipeline.predict(texts)
            metrics = self._calculate_metrics(labels, y_pred)
            
            # Guardar modelo
            model_path = os.path.join(self.models_dir, f"{model_type}_trained.pkl")
            vectorizer_path = os.path.join(self.models_dir, f"{model_type}_vectorizer.pkl")
            
            classifier.save_model(model_path, vectorizer_path)
            
            # Guardar resultados
            result = {
                "model_type": model_type,
                "best_params": best_params,
                "metrics": metrics,
                "model_path": model_path,
                "vectorizer_path": vectorizer_path,
                "timestamp": datetime.now().isoformat()
            }
            
            self.results_history.append(result)
            
            logger.info(f"Modelo {model_type} entrenado exitosamente")
            return classifier, result
            
        except Exception as e:
            logger.error(f"Error entrenando modelo {model_type}: {e}")
            raise
    
    def train_all_models(self, texts: List[str], labels: List[int], 
                        use_grid_search: bool = False) -> Dict[str, Tuple[MLToxicityClassifier, Dict[str, Any]]]:
        """
        Entrena todos los modelos disponibles
        
        Args:
            texts: Lista de textos de entrenamiento
            labels: Lista de etiquetas de entrenamiento
            use_grid_search: Si usar Grid Search para optimización
            
        Returns:
            Diccionario con todos los modelos entrenados
        """
        results = {}
        
        for model_type in self.hyperparameter_grids.keys():
            try:
                classifier, result = self.train_single_model(
                    model_type, texts, labels, use_grid_search
                )
                results[model_type] = (classifier, result)
            except Exception as e:
                logger.error(f"Error entrenando {model_type}: {e}")
                continue
        
        return results
    
    def compare_models(self, test_texts: List[str], test_labels: List[int]) -> Dict[str, Any]:
        """
        Compara el rendimiento de todos los modelos entrenados
        
        Args:
            test_texts: Textos de prueba
            test_labels: Etiquetas de prueba
            
        Returns:
            Comparación de rendimiento de modelos
        """
        if not self.results_history:
            raise ValueError("No hay modelos entrenados para comparar")
        
        comparison = {
            "test_data_size": len(test_texts),
            "models_evaluated": len(self.results_history),
            "results": {},
            "best_model": None,
            "best_f1": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        for result in self.results_history:
            model_type = result["model_type"]
            
            try:
                # Cargar modelo
                classifier = MLToxicityClassifier(model_type)
                classifier.load_model(
                    result["model_path"], 
                    result["vectorizer_path"]
                )
                
                # Evaluar en datos de prueba
                y_pred = classifier.pipeline.predict(test_texts)
                test_metrics = self._calculate_metrics(test_labels, y_pred)
                
                comparison["results"][model_type] = {
                    "training_metrics": result["metrics"],
                    "test_metrics": test_metrics,
                    "best_params": result["best_params"]
                }
                
                # Actualizar mejor modelo
                if test_metrics["f1"] > comparison["best_f1"]:
                    comparison["best_f1"] = test_metrics["f1"]
                    comparison["best_model"] = model_type
                
            except Exception as e:
                logger.error(f"Error evaluando {model_type}: {e}")
                comparison["results"][model_type] = {"error": str(e)}
        
        return comparison
    
    def _calculate_metrics(self, y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
        """Calcula métricas de evaluación"""
        try:
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
            
            return {
                "accuracy": accuracy_score(y_true, y_pred),
                "precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
                "recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
                "f1": f1_score(y_true, y_pred, average='weighted', zero_division=0)
            }
        except Exception as e:
            logger.error(f"Error calculando métricas: {e}")
            return {"error": str(e)}
    
    def save_results(self, filepath: str = None) -> bool:
        """Guarda los resultados del entrenamiento"""
        try:
            if filepath is None:
                filepath = os.path.join(
                    self.models_dir, 
                    f"training_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results_history, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Resultados guardados en: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando resultados: {e}")
            return False
    
    def load_results(self, filepath: str) -> bool:
        """Carga resultados de entrenamiento previo"""
        try:
            if not os.path.exists(filepath):
                logger.warning(f"Archivo de resultados no encontrado: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                self.results_history = json.load(f)
            
            logger.info(f"Resultados cargados desde: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error cargando resultados: {e}")
            return False
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Retorna un resumen del entrenamiento"""
        if not self.results_history:
            return {"message": "No hay resultados de entrenamiento"}
        
        return {
            "total_models": len(self.results_history),
            "model_types": [r["model_type"] for r in self.results_history],
            "best_f1": max(r["metrics"]["f1"] for r in self.results_history if "f1" in r["metrics"]),
            "average_f1": sum(r["metrics"]["f1"] for r in self.results_history if "f1" in r["metrics"]) / len(self.results_history),
            "last_training": max(r["timestamp"] for r in self.results_history),
            "models_directory": self.models_dir
        }

# Instancia global del entrenador
model_trainer = ModelTrainer()
