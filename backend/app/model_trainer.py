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
import matplotlib.pyplot as plt
import seaborn as sns

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
            labels: Lista de etiquetas
            use_grid_search: Si usar Grid Search para optimización de hiperparámetros
            
        Returns:
            Tuple con (modelo_entrenado, métricas)
        """
        logger.info(f"Entrenando modelo: {model_type}")
        
        # Crear y entrenar modelo
        model = MLToxicityClassifier(model_type)
        
        if use_grid_search and model_type in self.hyperparameter_grids:
            # Optimización de hiperparámetros con Grid Search
            logger.info("Aplicando Grid Search para optimización de hiperparámetros")
            
            # Crear pipeline para Grid Search
            from sklearn.pipeline import Pipeline
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(max_features=5000, ngram_range=(1, 3))),
                ('classifier', model.model)
            ])
            
            # Grid Search
            grid_search = GridSearchCV(
                pipeline, 
                self.hyperparameter_grids[model_type], 
                cv=5, 
                scoring='f1',
                n_jobs=-1
            )
            
            grid_search.fit(texts, labels)
            
            # Actualizar modelo con mejores parámetros
            model.pipeline = grid_search.best_estimator_
            model.model = grid_search.best_estimator_.named_steps['classifier']
            model.vectorizer = grid_search.best_estimator_.named_steps['vectorizer']
            model.is_trained = True
            
            logger.info(f"Mejores parámetros: {grid_search.best_params_}")
            
            # Métricas del mejor modelo
            y_pred = grid_search.predict(texts)
            metrics = self._calculate_metrics(labels, y_pred)
            metrics["best_params"] = grid_search.best_params_
            
        else:
            # Entrenamiento estándar
            metrics = model.train_model(texts, labels)
        
        return model, metrics
    
    def train_all_models(self, texts: List[str], labels: List[int],
                         use_grid_search: bool = False) -> Dict[str, Tuple[MLToxicityClassifier, Dict[str, Any]]]:
        """
        Entrena todos los tipos de modelos disponibles
        
        Args:
            texts: Lista de textos de entrenamiento
            labels: Lista de etiquetas
            use_grid_search: Si usar Grid Search para optimización
            
        Returns:
            Diccionario con todos los modelos entrenados y sus métricas
        """
        model_types = ["logistic_regression", "random_forest", "naive_bayes"]
        results = {}
        
        for model_type in model_types:
            try:
                model, metrics = self.train_single_model(model_type, texts, labels, use_grid_search)
                results[model_type] = (model, metrics)
                
                # Guardar modelo
                model_path = os.path.join(self.models_dir, f"{model_type}_model.pkl")
                model.save_model(model_path)
                
                logger.info(f"Modelo {model_type} entrenado y guardado")
                
            except Exception as e:
                logger.error(f"Error entrenando modelo {model_type}: {e}")
                continue
        
        return results
    
    def compare_models(self, models_results: Dict[str, Tuple[MLToxicityClassifier, Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Compara el rendimiento de diferentes modelos
        
        Args:
            models_results: Resultados de entrenamiento de modelos
            
        Returns:
            Diccionario con comparación de modelos
        """
        comparison = {
            "summary": {},
            "best_model": None,
            "ranking": []
        }
        
        best_score = 0
        best_model_name = None
        
        for model_name, (model, metrics) in models_results.items():
            # Resumen del modelo
            comparison["summary"][model_name] = {
                "accuracy": metrics.get("accuracy", 0),
                "precision": metrics.get("precision", 0),
                "recall": metrics.get("recall", 0),
                "f1": metrics.get("f1", 0),
                "cv_accuracy_mean": metrics.get("cv_accuracy_mean", 0),
                "cv_accuracy_std": metrics.get("cv_accuracy_std", 0)
            }
            
            # Determinar el mejor modelo por F1-score
            f1_score = metrics.get("f1", 0)
            if f1_score > best_score:
                best_score = f1_score
                best_model_name = model_name
        
        # Ranking de modelos por F1-score
        ranking = []
        for model_name, (model, metrics) in models_results.items():
            ranking.append({
                "model": model_name,
                "f1_score": metrics.get("f1", 0),
                "accuracy": metrics.get("accuracy", 0),
                "description": model.get_model_info().get("description", "")
            })
        
        # Ordenar por F1-score descendente
        ranking.sort(key=lambda x: x["f1_score"], reverse=True)
        comparison["ranking"] = ranking
        comparison["best_model"] = best_model_name
        
        return comparison
    
    def evaluate_model_on_test_data(self, model: MLToxicityClassifier, 
                                   test_texts: List[str], test_labels: List[int]) -> Dict[str, Any]:
        """
        Evalúa un modelo en datos de prueba separados
        
        Args:
            model: Modelo entrenado a evaluar
            test_texts: Lista de textos de prueba
            test_labels: Lista de etiquetas de prueba
            
        Returns:
            Diccionario con métricas de evaluación
        """
        if not model.is_trained:
            raise RuntimeError("El modelo debe estar entrenado para evaluación")
        
        try:
            # Predicciones
            y_pred = []
            y_proba = []
            
            for text in test_texts:
                is_toxic, prob, score = model.predict_toxicity(text)
                y_pred.append(1 if is_toxic else 0)
                y_proba.append(prob)
            
            # Métricas básicas
            metrics = self._calculate_metrics(test_labels, y_pred)
            
            # Reporte de clasificación detallado
            report = classification_report(test_labels, y_pred, output_dict=True)
            metrics["classification_report"] = report
            
            # Matriz de confusión
            cm = confusion_matrix(test_labels, y_pred)
            metrics["confusion_matrix"] = cm.tolist()
            
            # Probabilidades promedio por clase
            metrics["avg_probability_toxic"] = sum(y_proba) / len(y_proba)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error en evaluación: {e}")
            return {}
    
    def _calculate_metrics(self, y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
        """
        Calcula métricas básicas de rendimiento
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Etiquetas predichas
            
        Returns:
            Diccionario con métricas
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
            "recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
            "f1": f1_score(y_true, y_pred, average='weighted', zero_division=0)
        }
    
    def save_training_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Guarda los resultados del entrenamiento
        
        Args:
            results: Resultados a guardar
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del archivo guardado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_results_{timestamp}.json"
        
        filepath = os.path.join(self.models_dir, filename)
        
        # Convertir numpy arrays a listas para serialización JSON
        def convert_numpy(obj):
            if hasattr(obj, 'tolist'):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_numpy(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        results_serializable = convert_numpy(results)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results_serializable, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Resultados guardados en: {filepath}")
        return filepath
    
    def load_training_results(self, filepath: str) -> Dict[str, Any]:
        """
        Carga resultados de entrenamiento guardados
        
        Args:
            filepath: Ruta al archivo de resultados
            
        Returns:
            Diccionario con resultados
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            logger.info(f"Resultados cargados desde: {filepath}")
            return results
            
        except Exception as e:
            logger.error(f"Error cargando resultados: {e}")
            return {}
    
    def generate_model_report(self, comparison_results: Dict[str, Any]) -> str:
        """
        Genera un reporte de texto de la comparación de modelos
        
        Args:
            comparison_results: Resultados de comparación de modelos
            
        Returns:
            Reporte en formato texto
        """
        report = []
        report.append("=" * 60)
        report.append("📊 REPORTE DE COMPARACIÓN DE MODELOS - ToxiGuard")
        report.append("=" * 60)
        report.append("")
        
        # Resumen del mejor modelo
        best_model = comparison_results.get("best_model")
        if best_model:
            report.append(f"🏆 MEJOR MODELO: {best_model.upper()}")
            report.append("")
        
        # Ranking de modelos
        report.append("📈 RANKING DE MODELOS (por F1-Score):")
        report.append("-" * 40)
        
        for i, model_info in enumerate(comparison_results.get("ranking", []), 1):
            report.append(f"{i}. {model_info['model'].upper()}")
            report.append(f"   F1-Score: {model_info['f1_score']:.3f}")
            report.append(f"   Accuracy: {model_info['accuracy']:.3f}")
            report.append(f"   Descripción: {model_info['description']}")
            report.append("")
        
        # Detalles por modelo
        report.append("🔍 DETALLES POR MODELO:")
        report.append("-" * 40)
        
        for model_name, metrics in comparison_results.get("summary", {}).items():
            report.append(f"\n{model_name.upper()}:")
            report.append(f"  Accuracy: {metrics['accuracy']:.3f}")
            report.append(f"  Precision: {metrics['precision']:.3f}")
            report.append(f"  Recall: {metrics['recall']:.3f}")
            report.append(f"  F1-Score: {metrics['f1']:.3f}")
            report.append(f"  CV Accuracy: {metrics['cv_accuracy_mean']:.3f} ± {metrics['cv_accuracy_std']:.3f}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)

# Instancia global del entrenador
model_trainer = ModelTrainer()
