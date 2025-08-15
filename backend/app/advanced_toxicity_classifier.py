"""
🚨 Clasificador Avanzado de Toxicidad - ToxiGuard
Implementa análisis ultra-sensible para detectar textos ofensivos, insultos y groserías
con scoring adaptativo y ponderación de palabras por severidad
"""

import re
import logging
from typing import List, Dict, Tuple, Set
from collections import Counter
import numpy as np

# Configurar logging
logger = logging.getLogger(__name__)

class AdvancedToxicityClassifier:
    """Clasificador avanzado ultra-sensible para detección de toxicidad"""
    
    def __init__(self):
        # Categorías de toxicidad con pesos de severidad ultra-sensibles
        self.toxicity_categories = {
            "insulto_leve": {
                "keywords": {
                    "tonto": 0.3, "feo": 0.25, "lento": 0.2, "aburrido": 0.2,
                    "stupid": 0.3, "ugly": 0.25, "slow": 0.2, "boring": 0.2,
                    "bobo": 0.25, "tonto": 0.3, "idiota": 0.4
                },
                "base_weight": 0.4,
                "context_multiplier": 1.2,
                "requires_context": True,
                "severity_level": "leve"
            },
            "insulto_moderado": {
                "keywords": {
                    "idiota": 0.6, "estupido": 0.65, "imbecil": 0.7, "pendejo": 0.75,
                    "idiot": 0.6, "stupid": 0.65, "moron": 0.7, "fool": 0.65,
                    "tonto": 0.6, "bobo": 0.55, "gilipollas": 0.8
                },
                "base_weight": 0.75,
                "context_multiplier": 1.4,
                "requires_context": False,
                "severity_level": "moderado"
            },
            "insulto_severo": {
                "keywords": {
                    "pendejo": 0.9, "cabron": 0.95, "hijo de puta": 1.0, "puta": 0.9,
                    "perra": 0.85, "zorra": 0.85, "bastardo": 0.9, "malparido": 0.95,
                    "asshole": 0.9, "bitch": 0.85, "whore": 0.9, "bastard": 0.9,
                    "fuck": 0.8, "shit": 0.75, "damn": 0.7, "hell": 0.7
                },
                "base_weight": 0.95,
                "context_multiplier": 1.6,
                "requires_context": False,
                "severity_level": "severo"
            },
            "acoso_directo": {
                "keywords": {
                    "matar": 0.95, "morir": 0.8, "odio": 0.85, "destruir": 0.9,
                    "kill": 0.95, "die": 0.8, "hate": 0.85, "destroy": 0.9,
                    "muerte": 0.85, "asesinar": 0.95, "eliminar": 0.9
                },
                "base_weight": 0.9,
                "context_multiplier": 1.5,
                "requires_context": True,
                "severity_level": "alto"
            },
            "discriminacion": {
                "keywords": {
                    "racista": 0.95, "xenofobo": 0.95, "homofobo": 0.95, "machista": 0.9,
                    "racist": 0.95, "xenophobic": 0.95, "homophobic": 0.95, "sexist": 0.9,
                    "nazi": 0.95, "fascista": 0.95, "supremacista": 0.95
                },
                "base_weight": 0.98,
                "context_multiplier": 1.8,
                "requires_context": True,
                "severity_level": "crítico"
            },
            "amenazas": {
                "keywords": {
                    "te voy a matar": 1.0, "te mato": 1.0, "te rompo": 0.9,
                    "i will kill you": 1.0, "i kill you": 1.0, "i break you": 0.9,
                    "te destrozo": 0.95, "te aniquilo": 0.95, "te elimino": 0.95
                },
                "base_weight": 1.0,
                "context_multiplier": 2.0,
                "requires_context": False,
                "severity_level": "crítico"
            },
            "spam_toxico": {
                "keywords": {
                    "spam": 0.3, "basura": 0.4, "mierda": 0.6, "garbage": 0.4,
                    "trash": 0.4, "comprar": 0.2, "vender": 0.2, "oferta": 0.1
                },
                "base_weight": 0.3,
                "context_multiplier": 0.8,
                "requires_context": False,
                "severity_level": "bajo"
            }
        }
        
        # Umbrales ultra-sensibles para evitar valores triviales
        self.ultra_sensitive_thresholds = {
            "low_context": 0.15,      # Más sensible para textos con poco contexto
            "medium_context": 0.1,    # Ultra-sensible para contexto medio
            "high_context": 0.05,     # Extremadamente sensible para contexto alto
            "isolated_words": 0.25,   # Sensible para palabras aisladas
            "multiple_categories": 0.05,  # Ultra-sensible para múltiples categorías
            "repetition_penalty": 0.02    # Penalización por repetición
        }
        
        # Técnica de clasificación
        self.classification_technique = "Análisis Ultra-Sensible con Ponderación de Severidad"
        
        # Compilar patrones regex una sola vez
        self._compile_patterns()
        
        logger.info("🚨 Clasificador avanzado ultra-sensible inicializado")
    
    def _compile_patterns(self):
        """Compila patrones regex para búsqueda eficiente"""
        self.category_patterns = {}
        
        for category_name, category_info in self.toxicity_categories.items():
            keywords = category_info["keywords"]
            if keywords:
                # Patrón optimizado con word boundaries y soporte para frases
                keyword_patterns = []
                for keyword in keywords.keys():
                    if " " in keyword:  # Frase completa
                        keyword_patterns.append(re.escape(keyword))
                    else:  # Palabra individual
                        keyword_patterns.append(r'\b' + re.escape(keyword) + r'\b')
                
                pattern = re.compile(
                    '|'.join(keyword_patterns),
                    re.IGNORECASE | re.UNICODE
                )
                self.category_patterns[category_name] = pattern
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis ultra-sensible de toxicidad con ponderación de severidad
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad ultra-sensible
        """
        if not text or not text.strip():
            return self._get_default_response()
        
        try:
            # Preprocesamiento del texto
            cleaned_text = self._clean_text(text)
            words = self._tokenize_words(cleaned_text.lower())
            sentences = self._split_sentences(cleaned_text)
            
            # Análisis ultra-sensible de toxicidad
            toxicity_score, detected_categories, word_count, explanations, severity_breakdown = self._calculate_ultra_sensitive_score(
                cleaned_text, words, sentences
            )
            
            # Determinar categoría y toxicidad con umbrales ultra-sensibles
            is_toxic, category, percentage = self._determine_ultra_sensitive_toxicity(
                toxicity_score, 
                len(detected_categories),
                len(sentences),
                severity_breakdown
            )
            
            # Calcular confianza ultra-sensible
            confidence = self._calculate_ultra_sensitive_confidence(
                toxicity_score, 
                word_count, 
                len(detected_categories),
                severity_breakdown
            )
            
            return {
                "is_toxic": is_toxic,
                "toxicity_percentage": round(percentage, 2),
                "toxicity_level": category,
                "confidence": round(confidence, 3),
                "model_used": "advanced_toxicity_classifier_v1",
                "classification_technique": self.classification_technique,
                "details": {
                    "toxicity_score": round(toxicity_score, 4),
                    "detected_categories": detected_categories,
                    "text_length": len(text),
                    "word_count": word_count,
                    "sentence_count": len(sentences),
                    "severity_breakdown": severity_breakdown,
                    "explanations": explanations,
                    "ultra_sensitive_analysis": True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en análisis ultra-sensible: {e}")
            return self._get_default_response()
    
    def _clean_text(self, text: str) -> str:
        """Limpieza del texto manteniendo estructura"""
        # Remover URLs pero mantener el resto del texto
        text = re.sub(r'https?://\S+|www\.\S+', '', text, flags=re.IGNORECASE)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _tokenize_words(self, text: str) -> List[str]:
        """Tokenización de palabras optimizada"""
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
        return [word for word in words if len(word) > 1]
    
    def _split_sentences(self, text: str) -> List[str]:
        """División en oraciones"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_ultra_sensitive_score(self, cleaned_text: str, words: List[str], sentences: List[str]) -> Tuple[float, List[str], int, Dict[str, str], Dict[str, float]]:
        """Calcula el score de toxicidad ultra-sensible con ponderación de severidad"""
        total_score = 0.0
        detected_categories = []
        explanations = {}
        severity_breakdown = {}
        
        # Análisis por categoría con ponderación de severidad
        for category_name, category_info in self.toxicity_categories.items():
            pattern = self.category_patterns.get(category_name)
            if not pattern:
                continue
                
            matches = pattern.findall(cleaned_text.lower())
            if matches:
                # Calcular score ponderado por severidad de cada palabra
                category_score = 0.0
                word_severities = []
                
                for match in matches:
                    # Buscar la severidad específica de esta palabra
                    word_severity = 0.0
                    for keyword, severity in category_info["keywords"].items():
                        if keyword.lower() in match.lower() or match.lower() in keyword.lower():
                            word_severity = max(word_severity, severity)
                    
                    if word_severity > 0:
                        word_severities.append(word_severity)
                        category_score += word_severity
                
                if word_severities:
                    # Score promedio ponderado por severidad
                    avg_severity = sum(word_severities) / len(word_severities)
                    base_weight = category_info["base_weight"]
                    context_mult = category_info["context_multiplier"]
                    
                    # Cálculo ultra-sensible del score
                    if category_info["requires_context"]:
                        context_factor = min(2.0, len(sentences) / 3)  # Factor de contexto
                        final_score = (avg_severity * base_weight * context_mult * context_factor)
                    else:
                        final_score = (avg_severity * base_weight * context_mult)
                    
                    # Penalización por repetición (más repetición = más tóxico)
                    repetition_factor = min(1.5, len(matches) / 2)
                    final_score *= repetition_factor
                    
                    total_score += final_score
                    detected_categories.append(category_name)
                    
                    # Guardar breakdown de severidad
                    severity_breakdown[category_name] = {
                        "avg_severity": round(avg_severity, 3),
                        "match_count": len(matches),
                        "final_score": round(final_score, 4)
                    }
                    
                    # Generar explicación ultra-detallada
                    explanation = self._generate_ultra_detailed_explanation(
                        category_name, matches, word_severities, final_score
                    )
                    explanations[category_name] = explanation
        
        # Ajustes ultra-sensibles adicionales
        if len(detected_categories) > 1:
            # Multiplicador por múltiples categorías
            total_score *= (1.0 + len(detected_categories) * 0.3)
        
        if len(words) > 0:
            # Factor de densidad de toxicidad
            toxic_density = len([c for c in detected_categories if c != "spam_toxico"]) / len(words)
            total_score *= (1.0 + toxic_density * 2.0)
        
        # Normalización ultra-sensible (evitar valores triviales)
        normalized_score = min(1.0, total_score * 1.5)
        
        return normalized_score, detected_categories, len(words), explanations, severity_breakdown
    
    def _generate_ultra_detailed_explanation(self, category_name: str, matches: List[str], word_severities: List[float], final_score: float) -> str:
        """Genera explicación ultra-detallada de la detección"""
        
        # Mapeo de nombres de categorías a español
        category_names = {
            "insulto_leve": "insulto leve",
            "insulto_moderado": "insulto moderado", 
            "insulto_severo": "insulto severo",
            "acoso_directo": "acoso directo",
            "discriminacion": "discriminación",
            "amenazas": "amenazas",
            "spam_toxico": "spam tóxico"
        }
        
        readable_category = category_names.get(category_name, category_name)
        avg_severity = sum(word_severities) / len(word_severities) if word_severities else 0
        
        # Explicación detallada
        if len(matches) == 1:
            explanation = f"🚨 Detectó {readable_category} por '{matches[0]}' (severidad: {avg_severity:.2f}, score: {final_score:.3f})"
        else:
            shown_matches = matches[:3]
            if len(matches) > 3:
                explanation = f"🚨 Detectó {readable_category} por palabras como '{', '.join(shown_matches)}' y {len(matches) - 3} más (severidad promedio: {avg_severity:.2f}, score: {final_score:.3f})"
            else:
                explanation = f"🚨 Detectó {readable_category} por las palabras '{', '.join(shown_matches)}' (severidad promedio: {avg_severity:.2f}, score: {final_score:.3f})"
        
        # Agregar nivel de severidad
        if avg_severity >= 0.9:
            explanation += " - NIVEL CRÍTICO"
        elif avg_severity >= 0.7:
            explanation += " - NIVEL ALTO"
        elif avg_severity >= 0.5:
            explanation += " - NIVEL MODERADO"
        else:
            explanation += " - NIVEL BAJO"
        
        return explanation
    
    def _determine_ultra_sensitive_toxicity(self, score: float, category_count: int, sentence_count: int, severity_breakdown: Dict) -> Tuple[bool, str, float]:
        """Determina toxicidad con umbrales ultra-sensibles"""
        
        # Umbrales adaptativos ultra-sensibles
        if category_count > 3:
            threshold = self.ultra_sensitive_thresholds["multiple_categories"]
        elif category_count > 1:
            threshold = self.ultra_sensitive_thresholds["high_context"]
        elif sentence_count > 5:
            threshold = self.ultra_sensitive_thresholds["medium_context"]
        else:
            threshold = self.ultra_sensitive_thresholds["low_context"]
        
        # Ajuste por severidad crítica
        critical_severity_count = sum(
            1 for breakdown in severity_breakdown.values() 
            if breakdown.get("avg_severity", 0) >= 0.9
        )
        
        if critical_severity_count > 0:
            threshold *= 0.5  # Doble de sensible para severidad crítica
        
        # Determinar toxicidad
        is_toxic = score >= threshold
        
        # Categorización ultra-sensible
        if score < 0.2:
            category = "safe"
        elif score < 0.5:
            category = "moderate"
        elif score < 0.8:
            category = "high_risk"
        else:
            category = "critical_risk"
        
        # Porcentaje normalizado (evitar valores triviales)
        percentage = min(100.0, score * 120)  # Factor de amplificación
        
        # Asegurar que textos muy tóxicos tengan porcentajes altos
        if score > 0.7:
            percentage = max(percentage, 85.0)
        if score > 0.9:
            percentage = max(percentage, 95.0)
        
        return is_toxic, category, percentage
    
    def _calculate_ultra_sensitive_confidence(self, score: float, word_count: int, category_count: int, severity_breakdown: Dict) -> float:
        """Calcula confianza ultra-sensible del análisis"""
        
        # Factores de confianza
        score_factor = min(1.0, score * 1.5)  # Score más alto = más confianza
        word_factor = min(1.0, word_count / 30)  # Más palabras = más confianza
        category_factor = min(1.0, category_count / 2)  # Más categorías = más confianza
        
        # Factor de severidad
        severity_factor = 0.0
        if severity_breakdown:
            avg_severity = sum(
                breakdown.get("avg_severity", 0) for breakdown in severity_breakdown.values()
            ) / len(severity_breakdown)
            severity_factor = min(1.0, avg_severity * 1.2)
        
        # Promedio ponderado ultra-sensible
        confidence = (
            score_factor * 0.4 + 
            word_factor * 0.25 + 
            category_factor * 0.2 + 
            severity_factor * 0.15
        )
        
        # Asegurar confianza mínima para detecciones claras
        if score > 0.8 and category_count > 0:
            confidence = max(confidence, 0.9)
        
        return min(1.0, confidence)
    
    def _get_default_response(self) -> Dict:
        """Respuesta por defecto para casos de error"""
        return {
            "is_toxic": False,
            "toxicity_percentage": 0.0,
            "toxicity_level": "safe",
            "confidence": 0.0,
            "model_used": "advanced_toxicity_classifier_v1",
            "classification_technique": self.classification_technique,
            "details": {
                "toxicity_score": 0.0,
                "detected_categories": [],
                "text_length": 0,
                "word_count": 0,
                "sentence_count": 0,
                "severity_breakdown": {},
                "explanations": {},
                "ultra_sensitive_analysis": True
            }
        }
    
    def get_classifier_info(self) -> Dict:
        """Obtiene información del clasificador avanzado"""
        return {
            "type": "Advanced Ultra-Sensitive Classifier",
            "technique": self.classification_technique,
            "ultra_sensitive": True,
            "severity_weighting": True,
            "categories": list(self.toxicity_categories.keys()),
            "thresholds": self.ultra_sensitive_thresholds,
            "version": "v1.0"
        }

# Instancia global del clasificador avanzado
advanced_toxicity_classifier = AdvancedToxicityClassifier()
