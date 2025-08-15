"""
🤖 Modelos ML Optimizados - ToxiGuard
Implementa múltiples algoritmos de Machine Learning para clasificación de toxicidad
"""

import re
import logging
import numpy as np
from typing import List, Tuple, Dict, Union, Optional
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline
import joblib
import os

# Configurar logging
logger = logging.getLogger(__name__)

class MLToxicityClassifier:
    """Clasificador de toxicidad usando múltiples algoritmos ML"""
    
    def __init__(self, model_type: str = "logistic_regression"):
        """
        Inicializa el clasificador ML
        
        Args:
            model_type: Tipo de modelo ('logistic_regression', 'random_forest', 'naive_bayes')
        """
        self.model_type = model_type
        self.model = None
        self.vectorizer = None
        self.pipeline = None
        self.is_trained = False
        
        # Configuración de modelos
        self.model_configs = {
            "logistic_regression": {
                "classifier": LogisticRegression(random_state=42, max_iter=1000),
                "description": "Regresión Logística con regularización L2"
            },
            "random_forest": {
                "classifier": RandomForestClassifier(n_estimators=100, random_state=42),
                "description": "Random Forest con 100 árboles"
            },
            "naive_bayes": {
                "classifier": MultinomialNB(),
                "description": "Naive Bayes Multinomial"
            }
        }
        
        # Configuración del vectorizador TF-IDF
        self.vectorizer_config = {
            "max_features": 5000,
            "ngram_range": (1, 3),  # Unigramas, bigramas y trigramas
            "min_df": 2,            # Frecuencia mínima de documento
            "max_df": 0.95,         # Frecuencia máxima de documento
            "stop_words": "english"  # Palabras de parada en inglés
        }
        
        self._initialize_model()
        logger.info(f"Clasificador ML inicializado: {model_type}")
    
    def _initialize_model(self):
        """Inicializa el modelo y vectorizador"""
        if self.model_type not in self.model_configs:
            raise ValueError(f"Tipo de modelo no válido: {self.model_type}")
        
        # Obtener configuración del modelo
        config = self.model_configs[self.model_type]
        self.model = config["classifier"]
        
        # Inicializar vectorizador TF-IDF
        self.vectorizer = TfidfVectorizer(**self.vectorizer_config)
        
        # Crear pipeline
        self.pipeline = Pipeline([
            ('vectorizer', self.vectorizer),
            ('classifier', self.model)
        ])
        
        # Intentar cargar modelo entrenado automáticamente
        self._auto_load_trained_model()
    
    def _auto_load_trained_model(self):
        """Intenta cargar automáticamente un modelo entrenado"""
        try:
            # Buscar modelos entrenados en el directorio models/
            models_dir = "models"
            if not os.path.exists(models_dir):
                logger.info(f"Directorio de modelos no encontrado: {models_dir}")
                return
            
            # Buscar archivos de modelo para este tipo
            model_files = []
            for file in os.listdir(models_dir):
                if file.endswith('.pkl') and self.model_type in file:
                    model_files.append(file)
            
            if not model_files:
                logger.info(f"No se encontraron modelos entrenados para {self.model_type}")
                return
            
            # Cargar el primer modelo encontrado
            model_file = os.path.join(models_dir, model_files[0])
            logger.info(f"Intentando cargar modelo automáticamente: {model_file}")
            
            if self.load_model(model_file):
                logger.info(f"✅ Modelo cargado automáticamente: {model_file}")
            else:
                logger.warning(f"⚠️ Fallo al cargar modelo automáticamente: {model_file}")
                
        except Exception as e:
            logger.warning(f"Error en carga automática de modelo: {e}")
    
    def train_model(self, texts: List[str], labels: List[int], 
                   test_size: float = 0.2, random_state: int = 42) -> Dict[str, float]:
        """
        Entrena el modelo con datos de entrenamiento
        
        Args:
            texts: Lista de textos de entrenamiento
            labels: Lista de etiquetas (0: no tóxico, 1: tóxico)
            test_size: Proporción de datos de prueba
            random_state: Semilla para reproducibilidad
            
        Returns:
            Diccionario con métricas de rendimiento
        """
        if len(texts) != len(labels):
            raise ValueError("El número de textos y etiquetas debe ser igual")
        
        if len(set(labels)) < 2:
            raise ValueError("Se necesitan al menos 2 clases diferentes")
        
        logger.info(f"Entrenando modelo {self.model_type} con {len(texts)} muestras")
        
        # Dividir datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state, stratify=labels
        )
        
        # Entrenar el pipeline
        self.pipeline.fit(X_train, y_train)
        
        # Evaluar en datos de prueba
        y_pred = self.pipeline.predict(X_test)
        
        # Calcular métricas
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average='weighted'),
            "recall": recall_score(y_test, y_pred, average='weighted'),
            "f1": f1_score(y_test, y_pred, average='weighted')
        }
        
        # Validación cruzada
        cv_scores = cross_val_score(self.pipeline, texts, labels, cv=5)
        metrics["cv_accuracy_mean"] = cv_scores.mean()
        metrics["cv_accuracy_std"] = cv_scores.std()
        
        self.is_trained = True
        
        logger.info(f"Modelo entrenado. Accuracy: {metrics['accuracy']:.3f}")
        return metrics
    
    def predict_toxicity(self, text: str) -> Tuple[bool, float, float]:
        """
        Predice la toxicidad de un texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tuple con (es_toxico, probabilidad_toxico, score_normalizado)
        """
        if not self.is_trained:
            raise RuntimeError("El modelo debe ser entrenado antes de hacer predicciones")
        
        if not text or not text.strip():
            return False, 0.0, 0.0
        
        try:
            # Predecir probabilidades
            proba = self.pipeline.predict_proba([text])[0]
            prob_toxic = proba[1] if len(proba) > 1 else 0.0
            
            # Determinar si es tóxico (umbral 0.5)
            is_toxic = prob_toxic > 0.5
            
            # Normalizar score a rango [0, 1]
            normalized_score = prob_toxic
            
            return is_toxic, prob_toxic, normalized_score
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            return False, 0.0, 0.0
    
    def get_feature_importance(self, top_n: int = 20) -> List[Tuple[str, float]]:
        """
        Obtiene las características más importantes del modelo
        
        Args:
            top_n: Número de características a retornar
            
        Returns:
            Lista de tuplas (característica, importancia)
        """
        if not self.is_trained:
            return []
        
        try:
            if hasattr(self.model, 'feature_importances_'):
                # Random Forest
                feature_names = self.vectorizer.get_feature_names_out()
                importances = self.model.feature_importances_
            elif hasattr(self.model, 'coef_'):
                # Logistic Regression
                feature_names = self.vectorizer.get_feature_names_out()
                importances = np.abs(self.model.coef_[0])
            else:
                # Naive Bayes no tiene feature importance
                return []
            
            # Ordenar por importancia
            feature_importance = list(zip(feature_names, importances))
            feature_importance.sort(key=lambda x: x[1], reverse=True)
            
            return feature_importance[:top_n]
            
        except Exception as e:
            logger.error(f"Error obteniendo feature importance: {e}")
            return []
    
    def save_model(self, filepath: str) -> bool:
        """
        Guarda el modelo entrenado
        
        Args:
            filepath: Ruta donde guardar el modelo
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            if not self.is_trained:
                logger.warning("No se puede guardar un modelo no entrenado")
                return False
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Guardar el pipeline completo
            joblib.dump(self.pipeline, filepath)
            logger.info(f"Modelo guardado en: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando modelo: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """
        Carga un modelo entrenado desde archivo
        
        Args:
            filepath: Ruta al archivo del modelo
            
        Returns:
            True si se cargó exitosamente, False en caso contrario
        """
        try:
            if not os.path.exists(filepath):
                logger.error(f"Archivo de modelo no encontrado: {filepath}")
                return False
            
            # Cargar el pipeline completo
            loaded_pipeline = joblib.load(filepath)
            
            if isinstance(loaded_pipeline, Pipeline):
                self.pipeline = loaded_pipeline
                self.vectorizer = loaded_pipeline.named_steps['vectorizer']
                self.model = loaded_pipeline.named_steps['classifier']
                self.is_trained = True
                logger.info(f"Modelo cargado exitosamente desde: {filepath}")
                return True
            else:
                logger.error(f"Archivo no contiene un pipeline válido: {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Error cargando modelo desde {filepath}: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Union[str, bool, int]]:
        """
        Retorna información del modelo actual
        
        Returns:
            Diccionario con información del modelo
        """
        config = self.model_configs.get(self.model_type, {})
        
        return {
            "model_type": self.model_type,
            "description": config.get("description", "Modelo no configurado"),
            "is_trained": self.is_trained,
            "vectorizer_features": len(self.vectorizer.get_feature_names_out()) if self.vectorizer else 0,
            "model_params": str(self.model.get_params()) if self.model else "N/A"
        }

class HybridToxicityClassifier:
    """Clasificador híbrido que combina ML y reglas basadas en palabras clave"""
    
    def __init__(self, ml_model_type: str = "logistic_regression"):
        """
        Inicializa el clasificador híbrido
        
        Args:
            ml_model_type: Tipo de modelo ML a usar
        """
        self.ml_classifier = MLToxicityClassifier(ml_model_type)
        self.rule_based_classifier = None  # Se puede integrar con el clasificador existente
        
        # Pesos para combinar predicciones
        self.ml_weight = 0.7
        self.rule_weight = 0.3
        
        logger.info("Clasificador híbrido inicializado")
    
    def has_trained_ml_model(self) -> bool:
        """Verifica si el clasificador ML está entrenado"""
        return self.ml_classifier.is_trained
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str], int, int, str, float]:
        """
        Análisis híbrido combinando ML y reglas
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tuple con (es_toxico, score, etiquetas, longitud_texto, palabras_encontradas, categoria, porcentaje)
        """
        if not text or not text.strip():
            return False, 0.0, [], 0, 0, None, 0.0
        
        # Análisis basado en ML si está disponible
        if self.ml_classifier.is_trained:
            try:
                ml_is_toxic, ml_prob, ml_score = self.ml_classifier.predict_toxicity(text)
                logger.debug(f"Predicción ML: {ml_score:.3f}")
            except Exception as e:
                logger.warning(f"Error en predicción ML: {e}")
                ml_score = 0.0
        else:
            ml_score = 0.0
            logger.debug("Modelo ML no entrenado, usando solo reglas")
        
        # Análisis basado en reglas (placeholder - se puede integrar con el clasificador existente)
        rule_score = 0.0  # Por ahora, placeholder
        
        # Combinar predicciones
        combined_score = (self.ml_weight * ml_score + self.rule_weight * rule_score)
        
        # Determinar toxicidad final
        is_toxic = combined_score > 0.5
        
        # Calcular porcentaje
        toxicity_percentage = round(combined_score * 100, 1)
        
        # Información básica
        text_length = len(text)
        word_count = len(text.split())
        
        # Categoría basada en el score
        if combined_score <= 0.3:
            category = "leve"
        elif combined_score <= 0.6:
            category = "moderado"
        else:
            category = "alto"
        
        # Etiquetas
        labels = [category, "hybrid_ml" if self.ml_classifier.is_trained else "hybrid_rules"]
        
        return is_toxic, combined_score, labels, text_length, word_count, category, toxicity_percentage
    
    def train_ml_model(self, texts: List[str], labels: List[int]) -> Dict[str, float]:
        """
        Entrena el modelo ML del clasificador híbrido
        
        Args:
            texts: Lista de textos de entrenamiento
            labels: Lista de etiquetas (0: no tóxico, 1: tóxico)
            
        Returns:
            Métricas de rendimiento del modelo ML
        """
        return self.ml_classifier.train_model(texts, labels)
    
    def save_model(self, filepath: str) -> bool:
        """Guarda el modelo ML entrenado"""
        return self.ml_classifier.save_model(filepath)
    
    def load_model(self, filepath: str) -> bool:
        """Carga un modelo ML pre-entrenado"""
        return self.ml_classifier.load_model(filepath)

# Instancias globales
ml_classifier = MLToxicityClassifier()
hybrid_classifier = HybridToxicityClassifier()
