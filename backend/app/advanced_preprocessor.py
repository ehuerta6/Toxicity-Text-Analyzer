"""
🧠 Preprocesador Optimizado - ToxiGuard
Implementa preprocesamiento contextual optimizado para mejor rendimiento
"""

import re
import logging
from typing import List, Dict, Tuple, Set
from collections import Counter

# Configurar logging
logger = logging.getLogger(__name__)

class OptimizedTextPreprocessor:
    """Preprocesador optimizado con análisis contextual simplificado"""
    
    def __init__(self):
        # Stopwords optimizados (solo los más relevantes)
        self.stopwords_es = {
            "el", "la", "de", "que", "y", "a", "en", "un", "es", "se", "no", "te", "lo", "le", 
            "da", "su", "por", "son", "con", "para", "al", "del", "los", "las", "una", "como", 
            "pero", "sus", "me", "hasta", "hay", "donde", "han", "quien", "están", "estado", 
            "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", 
            "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", 
            "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", 
            "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros"
        }
        
        self.stopwords_en = {
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", 
            "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", 
            "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", 
            "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", 
            "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", 
            "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", 
            "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", 
            "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", 
            "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"
        }
        
        # Modificadores contextuales optimizados
        self.context_modifiers = {
            "negation": {"no", "not", "nunca", "jamás", "tampoco", "ni", "nada"},
            "intensifiers": {"muy", "mucho", "extremadamente", "terriblemente", "very", "extremely", "terribly"},
            "softeners": {"un poco", "algo", "bastante", "a bit", "somewhat", "quite"},
            "context_positive": {"pero", "aunque", "sin embargo", "but", "although", "however"}
        }
        
        # Patrones regex compilados para mejor rendimiento
        self._compile_patterns()
        
        logger.info("Preprocesador optimizado inicializado")
    
    def _compile_patterns(self):
        """Compila patrones regex para mejor rendimiento"""
        # Patrón para limpiar texto
        self.clean_pattern = re.compile(r'[^\w\sáéíóúñÁÉÍÓÚÑ]', re.UNICODE)
        
        # Patrón para detectar URLs
        self.url_pattern = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)
        
        # Patrón para detectar números
        self.number_pattern = re.compile(r'\b\d+\b')
        
        # Patrón para detectar emoticons
        self.emoticon_pattern = re.compile(r'[:;=]-?[)(/|\\]')
    
    def preprocess_text(self, text: str) -> Dict[str, any]:
        """
        Preprocesamiento optimizado del texto con análisis contextual
        
        Args:
            text: Texto a procesar
            
        Returns:
            Diccionario con información procesada del texto
        """
        if not text or not text.strip():
            return self._empty_result()
        
        # Limpieza básica optimizada
        clean_text = self._clean_text(text)
        
        # Tokenización simple y eficiente
        sentences = self._split_sentences(clean_text)
        words = self._tokenize_words(clean_text.lower())
        
        # Filtrado de stopwords optimizado
        filtered_words = [word for word in words if word not in self.stopwords_es and word not in self.stopwords_en]
        
        # Análisis contextual optimizado
        context_analysis = self._analyze_context_optimized(sentences, words, filtered_words)
        
        # Cálculo de score contextual
        context_score = self._calculate_context_score(context_analysis)
        
        return {
            "original_text": text,
            "cleaned_text": clean_text,
            "text_length": len(text),
            "word_count": len(filtered_words),
            "sentence_count": len(sentences),
            "sentences": sentences,
            "words": words,
            "filtered_words": filtered_words,
            "context_analysis": context_analysis,
            "context_score": context_score
        }
    
    def _clean_text(self, text: str) -> str:
        """Limpieza de texto optimizada"""
        # Remover URLs
        text = self.url_pattern.sub('', text)
        
        # Remover números
        text = self.number_pattern.sub('', text)
        
        # Remover emoticons
        text = self.emoticon_pattern.sub('', text)
        
        # Limpieza básica de caracteres especiales
        text = self.clean_pattern.sub(' ', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _split_sentences(self, text: str) -> List[str]:
        """División de oraciones optimizada"""
        # Patrón simple para dividir oraciones
        sentence_pattern = re.compile(r'[.!?]+')
        sentences = sentence_pattern.split(text)
        
        # Filtrar oraciones vacías y limpiar
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _tokenize_words(self, text: str) -> List[str]:
        """Tokenización de palabras optimizada"""
        # División simple por espacios y puntuación
        words = re.findall(r'\b\w+\b', text, re.UNICODE)
        
        # Filtrar palabras muy cortas
        words = [word for word in words if len(word) > 1]
        
        return words
    
    def _analyze_context_optimized(self, sentences: List[str], words: List[str], filtered_words: List[str]) -> Dict:
        """Análisis contextual optimizado"""
        context_analysis = {
            "negation_count": 0,
            "intensifier_count": 0,
            "softener_count": 0,
            "context_positive_count": 0,
            "sentence_complexity": 0,
            "word_diversity": 0
        }
        
        # Contar modificadores contextuales
        for word in words:
            if word in self.context_modifiers["negation"]:
                context_analysis["negation_count"] += 1
            elif word in self.context_modifiers["intensifiers"]:
                context_analysis["intensifier_count"] += 1
            elif word in self.context_modifiers["softeners"]:
                context_analysis["softener_count"] += 1
            elif word in self.context_modifiers["context_positive"]:
                context_analysis["context_positive_count"] += 1
        
        # Calcular complejidad de oraciones
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            context_analysis["sentence_complexity"] = min(1.0, avg_sentence_length / 20)
        
        # Calcular diversidad de palabras
        if filtered_words:
            unique_words = len(set(filtered_words))
            context_analysis["word_diversity"] = min(1.0, unique_words / len(filtered_words))
        
        return context_analysis
    
    def _calculate_context_score(self, context_analysis: Dict) -> float:
        """Cálculo optimizado del score contextual"""
        # Factores de contexto
        negation_factor = min(1.0, context_analysis["negation_count"] / 3)
        intensifier_factor = min(1.0, context_analysis["intensifier_count"] / 5)
        softener_factor = min(1.0, context_analysis["softener_count"] / 3)
        positive_factor = min(1.0, context_analysis["context_positive_count"] / 2)
        
        # Score base
        base_score = 0.5
        
        # Ajustes contextuales
        if context_analysis["sentence_complexity"] > 0.6:
            base_score += 0.2  # Textos complejos tienen más contexto
        
        if context_analysis["word_diversity"] > 0.7:
            base_score += 0.1  # Vocabulario diverso indica más contexto
        
        # Ajustes por modificadores
        context_score = base_score
        context_score += negation_factor * 0.1
        context_score += intensifier_factor * 0.1
        context_score -= softener_factor * 0.1
        context_score += positive_factor * 0.05
        
        # Normalizar entre 0 y 1
        return max(0.0, min(1.0, context_score))
    
    def get_context_score(self, preprocessed_data: Dict) -> float:
        """Obtiene el score contextual de los datos preprocesados"""
        return preprocessed_data.get("context_score", 0.5)
    
    def _empty_result(self) -> Dict:
        """Resultado vacío para textos nulos"""
        return {
            "original_text": "",
            "cleaned_text": "",
            "text_length": 0,
            "word_count": 0,
            "sentence_count": 0,
            "sentences": [],
            "words": [],
            "filtered_words": [],
            "context_analysis": {
                "negation_count": 0,
                "intensifier_count": 0,
                "softener_count": 0,
                "context_positive_count": 0,
                "sentence_complexity": 0,
                "word_diversity": 0
            },
            "context_score": 0.5
        }

# Instancia global optimizada
advanced_preprocessor = OptimizedTextPreprocessor()
