"""
🎯 Clasificador Híbrido de Toxicidad - ToxiGuard
Combina el clasificador contextual con embeddings, modelo de ML y clasificador basado en reglas
"""

import logging
from typing import Dict, List
from .ml_classifier import ml_classifier
from .improved_classifier import optimized_classifier
from .contextual_classifier import contextual_classifier

# Configurar logging
logger = logging.getLogger(__name__)

class HybridToxicityClassifier:
    """Clasificador híbrido que combina contextual, ML y reglas"""
    
    def __init__(self):
        self.contextual_classifier = contextual_classifier
        self.ml_classifier = ml_classifier
        self.rule_classifier = optimized_classifier
        
        # Orden de prioridad: contextual > ML > reglas
        self.classifier_priority = ["contextual", "ml", "rules"]
        self.current_primary = "contextual"
        self.classification_technique = "Híbrido (Contextual + ML + Reglas)"
        
        logger.info("✅ Clasificador híbrido mejorado inicializado")
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis híbrido de toxicidad con prioridad contextual
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad
        """
        if not text or not text.strip():
            return self._get_default_response()
        
        try:
            # Intentar usar el clasificador contextual primero (nuevo)
            if self.current_primary == "contextual" and self.contextual_classifier.embedding_model:
                logger.debug("🧠 Usando clasificador contextual para análisis")
                result = self.contextual_classifier.analyze_text(text)
                
                # Verificar que el resultado sea válido
                if result and result.get("toxicity_percentage") is not None:
                    result["classification_technique"] = f"Híbrido - {result.get('classification_technique', 'Contextual')}"
                    return result
                else:
                    logger.warning("⚠️ Clasificador contextual devolvió resultado inválido, usando fallback")
            
            # Intentar usar el modelo ML como segundo fallback
            if self.current_primary in ["ml", "contextual"] and self.ml_classifier.is_loaded:
                logger.debug("🔬 Usando modelo ML para análisis")
                result = self.ml_classifier.analyze_text(text)
                
                # Verificar que el resultado sea válido
                if result and result.get("toxicity_percentage") is not None:
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
                    "context_score": rule_result.get("details", {}).get("context_score", 0.0),
                    "explanations": rule_result.get("details", {}).get("explanations", {})
                }
            }
        except Exception as e:
            logger.error(f"❌ Error normalizando resultado de reglas: {e}")
            return self._get_default_response()
    
    def _get_default_response(self) -> Dict:
        """Respuesta por defecto cuando todos los clasificadores fallan"""
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
                "context_score": 0.0,
                "explanations": {}
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
                    "classification_technique": result["classification_technique"],
                    "explanations": result["details"].get("explanations", {})
                })
            except Exception as e:
                logger.error(f"Error analizando texto en lote: {e}")
                results.append({
                    "text": text,
                    "error": str(e)
                })
        
        return results
    
    def get_classifier_info(self) -> Dict:
        """Obtiene información de todos los clasificadores"""
        return {
            "primary_classifier": {
                "type": "Contextual (Embeddings)",
                "technique": self.contextual_classifier.classification_technique,
                "is_available": self.contextual_classifier.embedding_model is not None,
                "embedding_model": self.contextual_classifier.model_name,
                "context_analysis": True
            },
            "secondary_classifier": {
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
            "hybrid_mode": "Contextual primary + ML secondary + Rules fallback",
            "current_technique": self.classification_technique,
            "contextual_features": {
                "sentence_analysis": True,
                "embedding_similarity": True,
                "context_awareness": True,
                "negation_detection": True
            }
        }
    
    def set_primary_classifier(self, classifier_type: str = "contextual"):
        """Cambia el clasificador principal"""
        if classifier_type in ["contextual", "ml", "rules"]:
            self.current_primary = classifier_type
            logger.info(f"🔄 Clasificador principal cambiado a: {classifier_type}")
        else:
            logger.warning(f"⚠️ Tipo de clasificador no válido: {classifier_type}")

# Instancia global del clasificador híbrido mejorado
hybrid_classifier = HybridToxicityClassifier()
