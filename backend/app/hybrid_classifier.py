"""
🎯 Clasificador Híbrido de Toxicidad - ToxiGuard
Combina el clasificador avanzado ultra-sensible, contextual con embeddings, modelo de ML y clasificador basado en reglas
"""

import logging
from typing import Dict, List
from .ml_classifier import ml_classifier
from .improved_classifier import optimized_classifier
from .contextual_classifier import contextual_classifier
from .advanced_toxicity_classifier import advanced_toxicity_classifier

# Configurar logging
logger = logging.getLogger(__name__)

class HybridToxicityClassifier:
    """Clasificador híbrido que combina avanzado ultra-sensible, contextual, ML y reglas"""
    
    def __init__(self):
        self.advanced_classifier = advanced_toxicity_classifier
        self.contextual_classifier = contextual_classifier
        self.ml_classifier = ml_classifier
        self.rule_classifier = optimized_classifier
        
        # Orden de prioridad: avanzado > contextual > ML > reglas
        self.classifier_priority = ["advanced", "contextual", "ml", "rules"]
        self.current_primary = "advanced"
        self.classification_technique = "Híbrido Ultra-Sensible (Avanzado + Contextual + ML + Reglas)"
        
        logger.info("✅ Clasificador híbrido ultra-sensible mejorado inicializado")
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis híbrido ultra-sensible de toxicidad con prioridad al clasificador avanzado
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad ultra-sensible
        """
        if not text or not text.strip():
            return self._get_default_response()
        
        try:
            # Usar el clasificador avanzado ultra-sensible primero (nuevo)
            if self.current_primary == "advanced":
                logger.debug("🚨 Usando clasificador avanzado ultra-sensible para análisis")
                result = self.advanced_classifier.analyze_text(text)
                
                # Verificar que el resultado sea válido
                if result and result.get("toxicity_percentage") is not None:
                    result["classification_technique"] = f"Híbrido Ultra-Sensible - {result.get('classification_technique', 'Avanzado')}"
                    return result
                else:
                    logger.warning("⚠️ Clasificador avanzado devolvió resultado inválido, usando fallback")
            
            # Intentar usar el clasificador contextual como segundo fallback
            if self.current_primary in ["contextual", "advanced"] and self.contextual_classifier.embedding_model:
                logger.debug("🧠 Usando clasificador contextual para análisis")
                result = self.contextual_classifier.analyze_text(text)
                
                # Verificar que el resultado sea válido
                if result and result.get("toxicity_percentage") is not None:
                    result["classification_technique"] = f"Híbrido - {result.get('classification_technique', 'Contextual')}"
                    return result
                else:
                    logger.warning("⚠️ Clasificador contextual devolvió resultado inválido, usando fallback")
            
            # Intentar usar el modelo ML como tercer fallback
            if self.current_primary in ["ml", "contextual", "advanced"] and self.ml_classifier.is_loaded:
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
            logger.error(f"❌ Error en análisis híbrido ultra-sensible: {e}")
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
                    "explanations": rule_result.get("details", {}).get("explanations", {}),
                    "severity_breakdown": rule_result.get("details", {}).get("severity_breakdown", {}),
                    "ultra_sensitive_analysis": False
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
                "explanations": {},
                "severity_breakdown": {},
                "ultra_sensitive_analysis": False
            }
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Análisis en lote usando el clasificador híbrido ultra-sensible"""
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
                    "explanations": result["details"].get("explanations", {}),
                    "severity_breakdown": result["details"].get("severity_breakdown", {}),
                    "ultra_sensitive_analysis": result["details"].get("ultra_sensitive_analysis", False)
                })
            except Exception as e:
                logger.error(f"Error analizando texto en lote: {e}")
                results.append({
                    "text": text,
                    "error": str(e)
                })
        
        return results
    
    def get_classifier_info(self) -> Dict:
        """Obtiene información de todos los clasificadores incluyendo el avanzado"""
        return {
            "primary_classifier": {
                "type": "Advanced Ultra-Sensitive",
                "technique": self.advanced_classifier.classification_technique,
                "is_available": True,
                "ultra_sensitive": True,
                "severity_weighting": True,
                "context_analysis": True
            },
            "secondary_classifier": {
                "type": "Contextual (Embeddings)",
                "technique": self.contextual_classifier.classification_technique,
                "is_available": self.contextual_classifier.embedding_model is not None,
                "embedding_model": self.contextual_classifier.model_name,
                "context_analysis": True
            },
            "tertiary_classifier": {
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
            "hybrid_mode": "Advanced Ultra-Sensitive primary + Contextual secondary + ML tertiary + Rules fallback",
            "current_technique": self.classification_technique,
            "ultra_sensitive_features": {
                "sentence_analysis": True,
                "embedding_similarity": True,
                "context_awareness": True,
                "negation_detection": True,
                "severity_weighting": True,
                "ultra_sensitive_thresholds": True
            }
        }
    
    def set_primary_classifier(self, classifier_type: str = "advanced"):
        """Cambia el clasificador principal"""
        if classifier_type in ["advanced", "contextual", "ml", "rules"]:
            self.current_primary = classifier_type
            logger.info(f"🔄 Clasificador principal cambiado a: {classifier_type}")
        else:
            logger.warning(f"⚠️ Tipo de clasificador no válido: {classifier_type}")

# Instancia global del clasificador híbrido ultra-sensible mejorado
hybrid_classifier = HybridToxicityClassifier()
