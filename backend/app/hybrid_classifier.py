"""
🎯 Clasificador Híbrido de Toxicidad - ToxiGuard
Combina el mejor modelo de ML (Linear SVM) con clasificador basado en reglas como fallback
"""

import logging
from typing import Dict, List
from .ml_classifier import ml_classifier
from .improved_classifier import optimized_classifier

# Configurar logging
logger = logging.getLogger(__name__)

class HybridToxicityClassifier:
    """Clasificador híbrido que combina ML y reglas"""
    
    def __init__(self):
        self.ml_classifier = ml_classifier
        self.rule_classifier = optimized_classifier
        self.use_ml_as_primary = True
        self.classification_technique = "Híbrido (ML + Reglas)"
        
        logger.info("✅ Clasificador híbrido inicializado")
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis híbrido de toxicidad
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad
        """
        if not text or not text.strip():
            return self._get_default_response()
        
        try:
            # Intentar usar el modelo ML primero
            if self.use_ml_as_primary and self.ml_classifier.is_loaded:
                logger.debug("🔬 Usando modelo ML para análisis")
                result = self.ml_classifier.analyze_text(text)
                
                # Verificar que el resultado sea válido
                if result and result.get("toxicity_percentage") is not None:
                    # Actualizar técnica de clasificación para reflejar que se usó ML
                    result["classification_technique"] = f"Híbrido - {result.get('classification_technique', 'ML')}"
                    return result
                else:
                    logger.warning("⚠️ Modelo ML devolvió resultado inválido, usando fallback")
            
            # Fallback al clasificador basado en reglas
            logger.debug("📋 Usando clasificador basado en reglas como fallback")
            result = self.rule_classifier.analyze_text(text)
            
            # Asegurar compatibilidad con la estructura esperada
            normalized_result = self._normalize_rule_result(result)
            normalized_result["classification_technique"] = f"Híbrido - {normalized_result.get('classification_technique', 'Reglas')}"
            return normalized_result
            
        except Exception as e:
            logger.error(f"❌ Error en análisis híbrido: {e}")
            return self._get_default_response()
    
    def _normalize_rule_result(self, rule_result: Dict) -> Dict:
        """Normaliza el resultado del clasificador basado en reglas"""
        try:
            return {
                "is_toxic": rule_result.get("is_toxic", False),
                "toxicity_percentage": rule_result.get("toxicity_percentage", 0.0),
                "toxicity_level": rule_result.get("toxicity_level", "safe"),
                "confidence": rule_result.get("confidence", 0.0),
                "model_used": "hybrid_rule_fallback",
                "details": {
                    "toxicity_score": rule_result.get("details", {}).get("toxicity_score", 0.0),
                    "detected_categories": rule_result.get("details", {}).get("detected_categories", []),
                    "text_length": rule_result.get("details", {}).get("text_length", 0),
                    "word_count": rule_result.get("details", {}).get("word_count", 0),
                    "context_score": rule_result.get("details", {}).get("context_score", 0.0)
                }
            }
        except Exception as e:
            logger.error(f"❌ Error normalizando resultado de reglas: {e}")
            return self._get_default_response()
    
    def _get_default_response(self) -> Dict:
        """Respuesta por defecto cuando ambos clasificadores fallan"""
        return {
            "is_toxic": False,
            "toxicity_percentage": 0.0,
            "toxicity_level": "safe",
            "confidence": 0.0,
            "model_used": "hybrid_default",
            "classification_technique": self.classification_technique,
            "details": {
                "toxicity_score": 0.0,
                "detected_categories": [],
                "text_length": 0,
                "word_count": 0,
                "context_score": 0.0
            }
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Análisis en lote usando el clasificador híbrido"""
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
                    "classification_technique": result["classification_technique"]
                })
            except Exception as e:
                logger.error(f"Error analizando texto en lote: {e}")
                results.append({
                    "text": text,
                    "error": str(e)
                })
        
        return results
    
    def get_classifier_info(self) -> Dict:
        """Obtiene información de ambos clasificadores"""
        return {
            "primary_classifier": {
                "type": "ML (Linear SVM)",
                "technique": ml_classifier.classification_technique if hasattr(ml_classifier, 'classification_technique') else "Machine Learning",
                "is_available": self.ml_classifier.is_loaded,
                "performance": self.ml_classifier.get_model_info().get("performance", {})
            },
            "fallback_classifier": {
                "type": "Rules-based",
                "technique": self.rule_classifier.classification_technique if hasattr(self.rule_classifier, 'classification_technique') else "Análisis de Patrones",
                "is_available": True,
                "description": "Clasificador basado en keywords y patrones"
            },
            "hybrid_mode": "ML primary + Rules fallback",
            "current_technique": self.classification_technique
        }
    
    def set_primary_classifier(self, use_ml: bool = True):
        """Cambia el clasificador principal"""
        self.use_ml_as_primary = use_ml
        logger.info(f"🔄 Clasificador principal cambiado a: {'ML' if use_ml else 'Rules'}")

# Instancia global del clasificador híbrido
hybrid_classifier = HybridToxicityClassifier()
