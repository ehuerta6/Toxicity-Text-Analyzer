"""
🎯 Clasificador de Machine Learning Optimizado - ToxiGuard
Implementa el mejor modelo identificado (Linear SVM) para clasificación de toxicidad
"""

import pickle
import logging
import time
from typing import Dict, List
from pathlib import Path
import numpy as np

# Configurar logging
logger = logging.getLogger(__name__)

class MLToxicityClassifier:
    """Clasificador de toxicidad basado en machine learning optimizado"""
    
    def __init__(self, model_path: str = "../models/linear_svm_trained.pkl", 
                 vectorizer_path: str = "../models/linear_svm_vectorizer.pkl"):
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self.model = None
        self.vectorizer = None
        self.is_loaded = False
        self.classification_technique = self._determine_technique_from_path()
        
        # Cargar modelo y vectorizer
        self._load_model()
    
    def _determine_technique_from_path(self) -> str:
        """Determina la técnica de clasificación basada en la ruta del modelo"""
        model_name = self.model_path.stem.lower()
        
        if "linear_svm" in model_name or "svm" in model_name:
            return "Support Vector Machine (SVM)"
        elif "naive_bayes" in model_name or "bayes" in model_name:
            return "Naïve Bayes"
        elif "random_forest" in model_name or "forest" in model_name:
            return "Random Forest"
        elif "logistic_regression" in model_name or "logistic" in model_name:
            return "Logistic Regression"
        elif "gradient_boosting" in model_name or "boosting" in model_name:
            return "Gradient Boosting"
        elif "ensemble" in model_name:
            return "Ensemble (Múltiples Modelos)"
        else:
            return "Machine Learning Avanzado"
    
    def _load_model(self) -> bool:
        """Carga el modelo y vectorizer entrenados"""
        try:
            if not self.model_path.exists():
                logger.warning(f"⚠️ Modelo no encontrado en {self.model_path}")
                return False
            
            if not self.vectorizer_path.exists():
                logger.warning(f"⚠️ Vectorizer no encontrado en {self.vectorizer_path}")
                return False
            
            # Cargar modelo
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Cargar vectorizer
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            self.is_loaded = True
            logger.info("✅ Modelo ML cargado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando modelo ML: {e}")
            return False
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis de toxicidad usando el modelo de machine learning
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad
        """
        if not text or not text.strip():
            return self._get_default_response()
        
        if not self.is_loaded:
            logger.warning("⚠️ Modelo ML no cargado, usando respuesta por defecto")
            return self._get_default_response()
        
        try:
            start_time = time.time()
            
            # Preprocesar texto
            processed_text = self._preprocess_text(text)
            
            # Vectorizar texto
            text_vectorized = self.vectorizer.transform([processed_text])
            
            # Predecir toxicidad
            prediction = self.model.predict(text_vectorized)[0]
            
            # Obtener probabilidades si están disponibles
            try:
                probability = self.model.predict_proba(text_vectorized)[0]
                toxicity_percentage = probability[1] * 100 if len(probability) > 1 else 0
                confidence = max(probability)
            except AttributeError:
                # Para modelos como LinearSVC que no tienen predict_proba
                # Usar decision_function para obtener un score
                try:
                    decision_score = self.model.decision_function(text_vectorized)[0]
                    # Normalizar el score a un porcentaje (0-100)
                    toxicity_percentage = max(0, min(100, (decision_score + 1) * 50))
                    confidence = 0.8  # Confianza por defecto para modelos sin probabilidades
                except AttributeError:
                    # Fallback si no hay decision_function
                    toxicity_percentage = 50.0 if prediction else 0.0
                    confidence = 0.7
            
            # Determinar categoría
            toxicity_level = self._determine_toxicity_level(toxicity_percentage)
            
            # Obtener categorías detectadas
            detected_categories = self._get_detected_categories(toxicity_percentage)
            
            # Generar explicaciones
            explanations = self._generate_explanations(text, toxicity_percentage, detected_categories)
            
            # Calcular tiempo de respuesta
            response_time = (time.time() - start_time) * 1000
            
            return {
                "is_toxic": bool(prediction),
                "toxicity_percentage": round(toxicity_percentage, 2),
                "toxicity_level": toxicity_level,
                "confidence": round(confidence, 3),
                "model_used": "linear_svm_optimized",
                "classification_technique": self.classification_technique,
                "details": {
                    "toxicity_score": round(toxicity_percentage / 100, 4),
                    "detected_categories": detected_categories,
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "prediction_confidence": round(confidence, 3),
                    "response_time_ms": round(response_time, 2),
                    "explanations": explanations
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en análisis ML: {e}")
            return self._get_default_response()
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocesa el texto para el modelo ML"""
        # Limpieza básica
        text = text.lower().strip()
        
        # Remover caracteres especiales excesivos
        import re
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _determine_toxicity_level(self, toxicity_percentage: float) -> str:
        """Determina el nivel de toxicidad basado en el porcentaje"""
        if toxicity_percentage < 30:
            return "safe"
        elif toxicity_percentage < 70:
            return "moderate"
        else:
            return "high_risk"
    
    def _get_detected_categories(self, toxicity_percentage: float) -> List[str]:
        """Determina las categorías detectadas basadas en el porcentaje de toxicidad"""
        categories = []
        
        if toxicity_percentage > 80:
            categories.extend(["insulto_severo", "acoso", "discriminacion"])
        elif toxicity_percentage > 60:
            categories.extend(["insulto_moderado", "acoso"])
        elif toxicity_percentage > 30:
            categories.append("insulto_leve")
        
        return categories
    
    def _generate_explanations(self, text: str, toxicity_percentage: float, detected_categories: List[str]) -> Dict[str, str]:
        """Genera explicaciones para las categorías detectadas por el modelo ML"""
        explanations = {}
        
        # Mapeo de nombres de categorías a español
        category_names = {
            "insulto_leve": "insulto leve",
            "insulto_moderado": "insulto moderado", 
            "insultos_severo": "insulto severo",
            "acoso": "acoso",
            "discriminacion": "discriminación"
        }
        
        for category in detected_categories:
            readable_category = category_names.get(category, category)
            
            if toxicity_percentage > 80:
                explanation = f"Modelo ML detectó {readable_category} con alta confianza ({toxicity_percentage:.1f}%)"
            elif toxicity_percentage > 60:
                explanation = f"Modelo ML detectó {readable_category} con confianza moderada ({toxicity_percentage:.1f}%)"
            else:
                explanation = f"Modelo ML detectó {readable_category} con confianza baja ({toxicity_percentage:.1f}%)"
            
            explanations[category] = explanation
        
        return explanations
    
    def _get_default_response(self) -> Dict:
        """Respuesta por defecto cuando el modelo no está disponible"""
        return {
            "is_toxic": False,
            "toxicity_percentage": 0.0,
            "toxicity_level": "safe",
            "confidence": 0.0,
            "model_used": "linear_svm_optimized",
            "classification_technique": self.classification_technique,
            "details": {
                "toxicity_score": 0.0,
                "detected_categories": [],
                "text_length": 0,
                "word_count": 0,
                "prediction_confidence": 0.0,
                "response_time_ms": 0.0,
                "explanations": {}
            }
        }
    
    def get_model_info(self) -> Dict:
        """Obtiene información del modelo cargado"""
        return {
            "model_type": "Linear SVM",
            "classification_technique": self.classification_technique,
            "is_loaded": self.is_loaded,
            "model_path": str(self.model_path),
            "vectorizer_path": str(self.vectorizer_path),
            "performance": {
                "f1_score": 0.7324,
                "precision": 0.7363,
                "recall": 0.7350,
                "accuracy": 0.7350
            }
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Análisis en lote de múltiples textos"""
        results = []
        
        for text in texts:
            try:
                result = self.analyze_text(text)
                results.append({
                    "text": text,
                    "is_toxic": result["is_toxic"],
                    "toxicity_percentage": result["toxicity_percentage"],
                    "toxicity_level": result["toxicity_level"],
                    "confidence": result["confidence"],
                    "detected_categories": result["details"]["detected_categories"],
                    "word_count": result["details"]["word_count"],
                    "explanations": result["details"].get("explanations", {})
                })
            except Exception as e:
                logger.error(f"Error analizando texto en lote: {e}")
                results.append({
                    "text": text,
                    "error": str(e)
                })
        
        return results

# Instancia global del clasificador ML
ml_classifier = MLToxicityClassifier()
