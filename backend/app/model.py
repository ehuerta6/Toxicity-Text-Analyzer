"""
🤖 Módulo de Modelo ML - ToxiGuard
Maneja la carga, predicción y gestión del modelo de Machine Learning
"""

import joblib
import logging
import re
from pathlib import Path
from typing import Tuple, Optional

# Configurar logging
logger = logging.getLogger(__name__)

class ToxicityMLModel:
    """Clase para manejar el modelo ML de detección de toxicidad"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.is_loaded = False
        self.models_dir = Path(__file__).parent.parent.parent / "models"
    
    def load_model(self) -> bool:
        """Carga el modelo ML y vectorizador - UNA SOLA VEZ"""
        if self.is_loaded:
            logger.info("Modelo ML ya está cargado")
            return True
        
        try:
            # Cargar modelo
            model_path = self.models_dir / "toxic_model.pkl"
            if not model_path.exists():
                logger.warning(f"Modelo ML no encontrado: {model_path}")
                return False
            
            self.model = joblib.load(model_path)
            logger.info(f"Modelo ML cargado: {type(self.model).__name__}")
            
            # Cargar vectorizador
            vectorizer_path = self.models_dir / "vectorizer.pkl"
            if not vectorizer_path.exists():
                logger.warning(f"Vectorizador ML no encontrado: {vectorizer_path}")
                return False
            
            self.vectorizer = joblib.load(vectorizer_path)
            logger.info(f"Vectorizador ML cargado: {type(self.vectorizer).__name__}")
            
            self.is_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error cargando modelo ML: {e}")
            self.is_loaded = False
            self.model = None
            self.vectorizer = None
            return False
    
    def preprocess_text(self, text: str) -> str:
        """Preprocesamiento optimizado para el modelo ML"""
        if not text:
            return ""
        
        # Normalización básica
        text = text.lower().strip()
        
        # Remover caracteres extraños pero mantener estructura
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def predict(self, text: str) -> Tuple[bool, float, float, list]:
        """
        Realiza predicción con el modelo ML
        
        Returns:
            Tuple con (es_toxico, score, porcentaje_toxicidad, labels)
        """
        if not self.is_loaded:
            raise RuntimeError("Modelo ML no está cargado")
        
        try:
            # Preprocesar texto
            processed_text = self.preprocess_text(text)
            
            if not processed_text:
                return False, 0.0, 0.0, ["empty_text"]
            
            # Vectorizar
            X = self.vectorizer.transform([processed_text])
            
            # Predicción
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            
            # Resultados
            is_toxic = bool(prediction)
            score = float(probabilities[int(prediction)])
            toxicity_percentage = round(score * 100, 1)
            
            # Logs para debugging
            logger.debug(f"Texto: '{text[:50]}...' -> Procesado: '{processed_text[:50]}...'")
            logger.debug(f"Predicción: {prediction}, Probabilidades: {probabilities}")
            logger.debug(f"Score: {score}, Porcentaje: {toxicity_percentage}%")
            
            return is_toxic, score, toxicity_percentage, ["ml_detected"]
            
        except Exception as e:
            logger.error(f"Error en predicción ML: {e}")
            raise
    
    def get_status(self) -> dict:
        """Retorna el estado actual del modelo"""
        return {
            "model_loaded": self.is_loaded,
            "ml_model_available": self.model is not None,
            "vectorizer_available": self.vectorizer is not None,
            "status": "ready" if self.is_loaded else "not_ready",
            "message": "Modelo ML cargado y listo" if self.is_loaded else "Modelo ML no disponible"
        }

# Instancia global del modelo ML
ml_model = ToxicityMLModel()
