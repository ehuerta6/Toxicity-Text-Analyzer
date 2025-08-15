"""
🎯 Clasificador Optimizado de Toxicidad - ToxiGuard
Implementa análisis contextual y scoring adaptativo para mayor precisión y rendimiento
"""

import re
import logging
from typing import List, Tuple, Dict, Set
from collections import Counter
from .advanced_preprocessor import advanced_preprocessor

# Configurar logging
logger = logging.getLogger(__name__)

class OptimizedToxicityClassifier:
    """Clasificador optimizado con análisis contextual y scoring adaptativo"""
    
    def __init__(self):
        # Categorías de toxicidad optimizadas con palabras clave específicas
        self.toxicity_categories = {
            "insulto_leve": {
                "keywords": {"tonto", "feo", "lento", "aburrido", "stupid", "ugly", "slow", "boring"},
                "base_weight": 0.15,
                "context_multiplier": 0.5,
                "requires_context": True
            },
            "insulto_moderado": {
                "keywords": {"idiota", "estupido", "imbecil", "idiot", "stupid", "moron", "fool"},
                "base_weight": 0.4,
                "context_multiplier": 0.9,
                "requires_context": False
            },
            "insulto_severo": {
                "keywords": {"pendejo", "cabron", "hijo de puta", "asshole", "bitch", "bastard"},
                "base_weight": 0.85,
                "context_multiplier": 1.1,
                "requires_context": False
            },
            "acoso": {
                "keywords": {"matar", "morir", "odio", "destruir", "kill", "die", "hate", "destroy"},
                "base_weight": 0.75,
                "context_multiplier": 1.0,
                "requires_context": True
            },
            "discriminacion": {
                "keywords": {"racista", "xenofobo", "homofobo", "racist", "xenophobic", "homophobic"},
                "base_weight": 0.9,
                "context_multiplier": 1.2,
                "requires_context": True
            },
            "spam": {
                "keywords": {"spam", "basura", "mierda", "garbage", "trash", "comprar", "vender"},
                "base_weight": 0.25,
                "context_multiplier": 0.7,
                "requires_context": False
            }
        }
        
        # Umbrales adaptativos optimizados
        self.adaptive_thresholds = {
            "low_context": 0.4,
            "medium_context": 0.3,
            "high_context": 0.25,
            "isolated_words": 0.6
        }
        
        # Compilar patrones regex una sola vez
        self._compile_patterns()
        
        logger.info("Clasificador optimizado inicializado")
    
    def _compile_patterns(self):
        """Compila patrones regex para búsqueda eficiente"""
        self.category_patterns = {}
        
        for category_name, category_info in self.toxicity_categories.items():
            keywords = category_info["keywords"]
            if keywords:
                # Patrón optimizado con word boundaries
                pattern = re.compile(
                    r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b',
                    re.IGNORECASE | re.UNICODE
                )
                self.category_patterns[category_name] = pattern
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis optimizado de toxicidad con contexto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad
        """
        if not text or not text.strip():
            return {
                "is_toxic": False,
                "toxicity_percentage": 0.0,
                "toxicity_level": "safe",
                "confidence": 0.0,
                "model_used": "optimized_classifier_v2",
                "details": {}
            }
        
        # Preprocesamiento avanzado
        preprocessed_data = advanced_preprocessor.preprocess_text(text)
        
        # Análisis de toxicidad optimizado
        toxicity_score, detected_categories, word_count = self._calculate_toxicity_score(
            preprocessed_data["cleaned_text"],
            preprocessed_data["word_count"],
            preprocessed_data["context_score"]
        )
        
        # Determinar categoría y toxicidad
        is_toxic, category, percentage = self._determine_toxicity_level(
            toxicity_score, 
            preprocessed_data["context_score"],
            word_count
        )
        
        # Calcular confianza
        confidence = self._calculate_confidence(toxicity_score, word_count, len(detected_categories))
        
        return {
            "is_toxic": is_toxic,
            "toxicity_percentage": round(percentage, 2),
            "toxicity_level": category,
            "confidence": round(confidence, 3),
            "model_used": "optimized_classifier_v2",
            "details": {
                "toxicity_score": round(toxicity_score, 4),
                "detected_categories": detected_categories,
                "text_length": len(text),
                "word_count": word_count,
                "context_score": round(preprocessed_data["context_score"], 3)
            }
        }
    
    def _calculate_toxicity_score(self, cleaned_text: str, word_count: int, context_score: float) -> Tuple[float, List[str], int]:
        """Calcula el score de toxicidad de manera optimizada"""
        total_score = 0.0
        detected_categories = []
        
        # Análisis por categoría optimizado
        for category_name, category_info in self.toxicity_categories.items():
            pattern = self.category_patterns.get(category_name)
            if not pattern:
                continue
                
            matches = pattern.findall(cleaned_text.lower())
            if matches:
                match_count = len(matches)
                base_weight = category_info["base_weight"]
                context_mult = category_info["context_multiplier"]
                
                # Cálculo optimizado del score
                if category_info["requires_context"]:
                    score = base_weight * context_mult * (match_count / max(word_count, 1))
                else:
                    score = base_weight * (match_count / max(word_count, 1))
                
                total_score += score
                detected_categories.append(category_name)
        
        # Normalización del score
        if word_count > 0:
            total_score = min(1.0, total_score * (word_count ** 0.5))
        
        return total_score, detected_categories, word_count
    
    def _determine_toxicity_level(self, score: float, context_score: float, word_count: int) -> Tuple[bool, str, float]:
        """Determina el nivel de toxicidad de manera optimizada"""
        # Ajuste basado en contexto
        if context_score > 0.7:
            threshold = self.adaptive_thresholds["high_context"]
        elif context_score > 0.4:
            threshold = self.adaptive_thresholds["medium_context"]
        else:
            threshold = self.adaptive_thresholds["low_context"]
        
        # Ajuste para palabras aisladas
        if word_count <= 3:
            threshold = self.adaptive_thresholds["isolated_words"]
        
        # Determinar toxicidad
        is_toxic = score >= threshold
        
        # Categorización optimizada
        if score < 0.3:
            category = "safe"
        elif score < 0.6:
            category = "moderate"
        else:
            category = "high_risk"
        
        # Porcentaje normalizado
        percentage = min(100.0, score * 100)
        
        return is_toxic, category, percentage
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """Obtiene análisis detallado optimizado"""
        result = self.analyze_text(text)
        
        return {
            "is_toxic": result["is_toxic"],
            "toxicity_score": result["details"]["toxicity_score"],
            "detected_categories": result["details"]["detected_categories"],
            "text_length": result["details"]["text_length"],
            "word_count": result["details"]["word_count"],
            "toxicity_category": result["toxicity_level"],
            "toxicity_percentage": result["toxicity_percentage"],
            "confidence": result["confidence"]
        }
    
    def _calculate_confidence(self, score: float, word_count: int, category_count: int) -> float:
        """Calcula la confianza del análisis de manera optimizada"""
        # Factores de confianza
        score_factor = min(1.0, score * 2)  # Score más alto = más confianza
        word_factor = min(1.0, word_count / 50)  # Más palabras = más confianza
        category_factor = min(1.0, category_count / 3)  # Más categorías = más confianza
        
        # Promedio ponderado
        confidence = (score_factor * 0.5 + word_factor * 0.3 + category_factor * 0.2)
        return round(confidence, 3)
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Análisis en lote optimizado para múltiples textos"""
        results = []
        
        for text in texts:
            try:
                result = self.analyze_text(text)
                results.append({
                    "is_toxic": result["is_toxic"],
                    "toxicity_score": result["details"]["toxicity_score"],
                    "detected_categories": result["details"]["detected_categories"],
                    "text_length": result["details"]["text_length"],
                    "word_count": result["details"]["word_count"],
                    "toxicity_category": result["toxicity_level"],
                    "toxicity_percentage": result["toxicity_percentage"],
                    "confidence": result["confidence"]
                })
            except Exception as e:
                logger.error(f"Error analizando texto: {e}")
                results.append({
                    "is_toxic": False,
                    "toxicity_score": 0.0,
                    "detected_categories": [],
                    "text_length": len(text) if text else 0,
                    "word_count": 0,
                    "toxicity_category": "error",
                    "toxicity_percentage": 0.0,
                    "confidence": 0.0,
                    "error": str(e)
                })
        
        return results

# Instancia global optimizada
optimized_classifier = OptimizedToxicityClassifier()
