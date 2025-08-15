"""
🧠 Clasificador Contextual de Toxicidad - ToxiGuard
Implementa análisis contextual usando embeddings de sentence-transformers
para detectar toxicidad considerando el contexto completo de las frases
"""

import re
import logging
from typing import List, Dict, Tuple, Set
from collections import Counter
import numpy as np

# Configurar logging
logger = logging.getLogger(__name__)

# Importar sentence-transformers de manera opcional
try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    logger.info("✅ Sentence Transformers disponible")
except ImportError as e:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning(f"⚠️ Sentence Transformers no disponible: {e}")

class ContextualToxicityClassifier:
    """Clasificador contextual que analiza toxicidad considerando el contexto completo"""
    
    def __init__(self):
        # Modelo de embeddings para análisis contextual
        self.embedding_model = None
        self.model_name = "all-MiniLM-L6-v2"  # Modelo ligero y eficiente
        
        # Categorías de toxicidad con ejemplos contextuales
        self.toxicity_categories = {
            "insulto_directo": {
                "examples": [
                    "eres un idiota",
                    "you are stupid",
                    "soy un tonto",
                    "i am a fool"
                ],
                "base_weight": 0.8,
                "context_threshold": 0.7
            },
            "insulto_negado": {
                "examples": [
                    "no eres tonto",
                    "you are not stupid",
                    "no soy idiota",
                    "i am not a fool"
                ],
                "base_weight": 0.1,
                "context_threshold": 0.3
            },
            "acoso_directo": {
                "examples": [
                    "te voy a matar",
                    "i will kill you",
                    "odio a todos",
                    "i hate everyone"
                ],
                "base_weight": 0.9,
                "context_threshold": 0.8
            },
            "acoso_negado": {
                "examples": [
                    "no te voy a hacer daño",
                    "i won't hurt you",
                    "no odio a nadie",
                    "i don't hate anyone"
                ],
                "base_weight": 0.05,
                "context_threshold": 0.2
            },
            "discriminacion": {
                "examples": [
                    "los negros son inferiores",
                    "black people are inferior",
                    "las mujeres son débiles",
                    "women are weak"
                ],
                "base_weight": 0.95,
                "context_threshold": 0.85
            },
            "discriminacion_negada": {
                "examples": [
                    "todos somos iguales",
                    "we are all equal",
                    "no discrimino a nadie",
                    "i don't discriminate"
                ],
                "base_weight": 0.05,
                "context_threshold": 0.2
            }
        }
        
        # Palabras clave para detección inicial (solo para identificar candidatos)
        self.toxic_keywords = {
            "idiota", "estupido", "tonto", "imbecil", "pendejo", "cabron",
            "hijo de puta", "puta", "perra", "zorra", "bastardo", "malparido",
            "idiot", "stupid", "fool", "moron", "asshole", "bitch", "whore",
            "bastard", "damn", "hell", "fuck", "shit", "crap", "dumb",
            "matar", "morir", "odio", "destruir", "kill", "die", "hate",
            "racista", "xenofobo", "homofobo", "racist", "xenophobic", "homophobic"
        }
        
        # Inicializar modelo de embeddings si está disponible
        self._initialize_embedding_model()
        
        # Técnica de clasificación
        self.classification_technique = "Análisis Contextual con Embeddings"
        
        logger.info("Clasificador contextual inicializado")
    
    def _initialize_embedding_model(self):
        """Inicializa el modelo de embeddings de manera segura"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            logger.warning("⚠️ Sentence Transformers no disponible, usando fallback")
            return
        
        try:
            logger.info(f"🔄 Cargando modelo de embeddings: {self.model_name}")
            self.embedding_model = SentenceTransformer(self.model_name)
            logger.info("✅ Modelo de embeddings cargado exitosamente")
        except Exception as e:
            logger.error(f"❌ Error cargando modelo de embeddings: {e}")
            self.embedding_model = None
    
    def analyze_text(self, text: str) -> Dict:
        """
        Análisis contextual de toxicidad usando embeddings
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con el análisis completo de toxicidad contextual
        """
        if not text or not text.strip():
            return self._get_default_response()
        
        try:
            # Dividir texto en oraciones para análisis contextual
            sentences = self._split_into_sentences(text)
            
            if not sentences:
                return self._get_default_response()
            
            # Análisis contextual por oración
            sentence_analyses = []
            total_toxicity_score = 0.0
            detected_categories = set()
            explanations = {}
            
            for sentence in sentences:
                sentence_analysis = self._analyze_sentence_context(sentence)
                sentence_analyses.append(sentence_analysis)
                
                total_toxicity_score += sentence_analysis["toxicity_score"]
                detected_categories.update(sentence_analysis["categories"])
                
                # Agregar explicaciones
                for category, explanation in sentence_analysis["explanations"].items():
                    if category not in explanations:
                        explanations[category] = []
                    explanations[category].append(explanation)
            
            # Calcular score promedio y normalizar
            avg_toxicity_score = total_toxicity_score / len(sentences) if sentences else 0.0
            normalized_score = min(1.0, avg_toxicity_score * 1.2)  # Ajuste para mantener escala 0-100
            
            # Determinar toxicidad y categoría
            is_toxic, category, percentage = self._determine_toxicity_level(normalized_score, len(detected_categories))
            
            # Calcular confianza basada en la consistencia del análisis
            confidence = self._calculate_confidence(sentence_analyses, len(sentences))
            
            # Consolidar explicaciones
            consolidated_explanations = self._consolidate_explanations(explanations)
            
            return {
                "is_toxic": is_toxic,
                "toxicity_percentage": round(percentage, 2),
                "toxicity_level": category,
                "confidence": round(confidence, 3),
                "model_used": "contextual_classifier_v1",
                "classification_technique": self.classification_technique,
                "details": {
                    "toxicity_score": round(normalized_score, 4),
                    "detected_categories": list(detected_categories),
                    "text_length": len(text),
                    "word_count": len(text.split()),
                    "context_score": round(avg_toxicity_score, 3),
                    "sentence_count": len(sentences),
                    "explanations": consolidated_explanations,
                    "sentence_analyses": sentence_analyses
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error en análisis contextual: {e}")
            return self._get_default_response()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Divide el texto en oraciones para análisis contextual"""
        # Patrón mejorado para dividir oraciones
        sentence_pattern = re.compile(r'[.!?]+[\s\n]*')
        sentences = sentence_pattern.split(text)
        
        # Filtrar y limpiar oraciones
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 2:  # Ignorar oraciones muy cortas
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _analyze_sentence_context(self, sentence: str) -> Dict:
        """Analiza el contexto de una oración específica"""
        if not self.embedding_model:
            # Fallback sin embeddings
            return self._analyze_sentence_fallback(sentence)
        
        try:
            # Verificar si la oración contiene palabras tóxicas
            sentence_lower = sentence.lower()
            toxic_words_found = [word for word in self.toxic_keywords if word in sentence_lower]
            
            if not toxic_words_found:
                return {
                    "toxicity_score": 0.0,
                    "categories": [],
                    "explanations": {},
                    "context_similarity": 0.0
                }
            
            # Calcular embeddings para la oración
            sentence_embedding = self.embedding_model.encode([sentence])[0]
            
            # Comparar con ejemplos de cada categoría
            max_similarity = 0.0
            best_category = None
            category_scores = {}
            
            for category_name, category_info in self.toxicity_categories.items():
                category_similarities = []
                
                for example in category_info["examples"]:
                    example_embedding = self.embedding_model.encode([example])[0]
                    similarity = util.pytorch_cos_sim(sentence_embedding, example_embedding).item()
                    category_similarities.append(similarity)
                
                # Usar la similitud máxima para esta categoría
                max_category_similarity = max(category_similarities) if category_similarities else 0.0
                category_scores[category_name] = max_category_similarity
                
                if max_category_similarity > max_similarity:
                    max_similarity = max_category_similarity
                    best_category = category_name
            
            # Calcular score de toxicidad basado en similitud y peso de categoría
            toxicity_score = 0.0
            detected_categories = []
            explanations = {}
            
            for category_name, similarity in category_scores.items():
                if similarity > self.toxicity_categories[category_name]["context_threshold"]:
                    category_weight = self.toxicity_categories[category_name]["base_weight"]
                    category_score = similarity * category_weight
                    toxicity_score = max(toxicity_score, category_score)
                    detected_categories.append(category_name)
                    
                    # Generar explicación contextual
                    explanation = self._generate_contextual_explanation(
                        category_name, similarity, sentence, toxic_words_found
                    )
                    explanations[category_name] = explanation
            
            return {
                "toxicity_score": toxicity_score,
                "categories": detected_categories,
                "explanations": explanations,
                "context_similarity": max_similarity
            }
            
        except Exception as e:
            logger.error(f"❌ Error analizando oración: {e}")
            return self._analyze_sentence_fallback(sentence)
    
    def _analyze_sentence_fallback(self, sentence: str) -> Dict:
        """Análisis de fallback sin embeddings"""
        sentence_lower = sentence.lower()
        toxic_words_found = [word for word in self.toxic_keywords if word in sentence_lower]
        
        if not toxic_words_found:
            return {
                "toxicity_score": 0.0,
                "categories": [],
                "explanations": {},
                "context_similarity": 0.0
            }
        
        # Análisis simple basado en palabras clave
        toxicity_score = min(0.5, len(toxic_words_found) * 0.2)
        categories = ["insulto_directo"] if toxic_words_found else []
        
        explanations = {}
        if toxic_words_found:
            explanations["insulto_directo"] = f"Detectó palabras tóxicas: {', '.join(toxic_words_found[:3])}"
        
        return {
            "toxicity_score": toxicity_score,
            "categories": categories,
            "explanations": explanations,
            "context_similarity": 0.3  # Similitud baja para fallback
        }
    
    def _generate_contextual_explanation(self, category: str, similarity: float, 
                                       sentence: str, toxic_words: List[str]) -> str:
        """Genera explicación contextual detallada"""
        
        # Mapeo de categorías a español
        category_names = {
            "insulto_directo": "insulto directo",
            "insulto_negado": "insulto negado (contexto positivo)",
            "acoso_directo": "acoso directo",
            "acoso_negado": "acoso negado (contexto positivo)",
            "discriminacion": "discriminación",
            "discriminacion_negada": "discriminación negada (contexto positivo)"
        }
        
        readable_category = category_names.get(category, category)
        similarity_percent = round(similarity * 100, 1)
        
        if "negado" in category or "negada" in category:
            explanation = f"Detectó {readable_category} (similitud: {similarity_percent}%) - El contexto indica que se está negando la toxicidad"
        else:
            explanation = f"Detectó {readable_category} (similitud: {similarity_percent}%) - Palabras clave: {', '.join(toxic_words[:3])}"
        
        return explanation
    
    def _determine_toxicity_level(self, score: float, category_count: int) -> Tuple[bool, str, float]:
        """Determina el nivel de toxicidad basado en el score contextual"""
        
        # Umbrales adaptativos basados en contexto
        if category_count > 2:
            threshold = 0.3  # Más sensible para múltiples categorías
        elif category_count > 0:
            threshold = 0.4  # Umbral estándar
        else:
            threshold = 0.6  # Menos sensible para categorías únicas
        
        # Determinar toxicidad
        is_toxic = score >= threshold
        
        # Categorización
        if score < 0.3:
            category = "safe"
        elif score < 0.6:
            category = "moderate"
        else:
            category = "high_risk"
        
        # Porcentaje normalizado
        percentage = min(100.0, score * 100)
        
        return is_toxic, category, percentage
    
    def _calculate_confidence(self, sentence_analyses: List[Dict], sentence_count: int) -> float:
        """Calcula la confianza del análisis contextual"""
        if not sentence_analyses:
            return 0.0
        
        # Factores de confianza
        avg_similarity = sum(analysis["context_similarity"] for analysis in sentence_analyses) / len(sentence_analyses)
        consistency_factor = min(1.0, sentence_count / 5)  # Más oraciones = más confianza
        
        # Confianza basada en similitud y consistencia
        confidence = (avg_similarity * 0.7 + consistency_factor * 0.3)
        return min(1.0, confidence)
    
    def _consolidate_explanations(self, explanations: Dict[str, List[str]]) -> Dict[str, str]:
        """Consolida múltiples explicaciones en una sola por categoría"""
        consolidated = {}
        
        for category, explanation_list in explanations.items():
            if explanation_list:
                # Tomar la explicación más detallada
                best_explanation = max(explanation_list, key=len)
                consolidated[category] = best_explanation
        
        return consolidated
    
    def _get_default_response(self) -> Dict:
        """Respuesta por defecto para casos de error"""
        return {
            "is_toxic": False,
            "toxicity_percentage": 0.0,
            "toxicity_level": "safe",
            "confidence": 0.0,
            "model_used": "contextual_classifier_v1",
            "classification_technique": self.classification_technique,
            "details": {
                "toxicity_score": 0.0,
                "detected_categories": [],
                "text_length": 0,
                "word_count": 0,
                "context_score": 0.0,
                "sentence_count": 0,
                "explanations": {},
                "sentence_analyses": []
            }
        }
    
    def get_classifier_info(self) -> Dict:
        """Obtiene información del clasificador contextual"""
        return {
            "type": "Contextual Classifier",
            "technique": self.classification_technique,
            "embedding_model": self.model_name if self.embedding_model else "Not available",
            "embedding_available": self.embedding_model is not None,
            "categories": list(self.toxicity_categories.keys()),
            "context_analysis": True,
            "fallback_mode": self.embedding_model is None
        }

# Instancia global del clasificador contextual
contextual_classifier = ContextualToxicityClassifier()
