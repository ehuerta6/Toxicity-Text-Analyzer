"""
🧠 Preprocesador Avanzado - ToxiGuard
Implementa preprocesamiento contextual y análisis de n-grams para mejorar la precisión
"""

import re
import logging
from typing import List, Dict, Tuple, Set
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams

# Configurar logging
logger = logging.getLogger(__name__)

class AdvancedTextPreprocessor:
    """Preprocesador avanzado con análisis contextual y n-grams"""
    
    def __init__(self):
        self.stopwords_es = set()
        self.stopwords_en = set()
        self.lemmatizer = None
        self.context_modifiers = {
            "negation": {"no", "not", "nunca", "jamás", "tampoco", "ni", "nada"},
            "intensifiers": {"muy", "mucho", "extremadamente", "terriblemente", "very", "extremely", "terribly"},
            "softeners": {"un poco", "algo", "bastante", "a bit", "somewhat", "quite"},
            "context_positive": {"pero", "aunque", "sin embargo", "but", "although", "however"}
        }
        
        self._initialize_nltk()
        logger.info("Preprocesador avanzado inicializado")
    
    def _initialize_nltk(self):
        """Inicializa recursos de NLTK"""
        try:
            # Descargar recursos necesarios si no están disponibles
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
            
            try:
                nltk.data.find('corpora/stopwords')
            except LookupError:
                nltk.download('stopwords')
            
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                nltk.download('wordnet')
            
            # Cargar stopwords
            self.stopwords_es = set(stopwords.words('spanish'))
            self.stopwords_en = set(stopwords.words('english'))
            
            # Inicializar lemmatizador
            self.lemmatizer = WordNetLemmatizer()
            
        except Exception as e:
            logger.warning(f"No se pudieron cargar recursos NLTK: {e}")
            # Fallback a stopwords básicos
            self.stopwords_es = {"el", "la", "de", "que", "y", "a", "en", "un", "es", "se", "no", "te", "lo", "le", "da", "su", "por", "son", "con", "para", "al", "del", "los", "las", "una", "como", "pero", "sus", "me", "hasta", "hay", "donde", "han", "quien", "están", "estado", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros"}
            self.stopwords_en = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"}
    
    def preprocess_text(self, text: str) -> Dict[str, any]:
        """
        Preprocesamiento avanzado del texto con análisis contextual
        
        Args:
            text: Texto a procesar
            
        Returns:
            Diccionario con información procesada del texto
        """
        if not text or not text.strip():
            return self._empty_result()
        
        # Limpieza básica
        clean_text = self._clean_text(text)
        
        # Tokenización
        sentences = sent_tokenize(clean_text)
        words = word_tokenize(clean_text.lower())
        
        # Análisis de n-grams
        bigrams = list(ngrams(words, 2))
        trigrams = list(ngrams(words, 3))
        
        # Filtrado de stopwords
        filtered_words = [word for word in words if word not in self.stopwords_es and word not in self.stopwords_en]
        
        # Lematización
        lemmatized_words = [self.lemmatizer.lemmatize(word) if self.lemmatizer else word for word in filtered_words]
        
        # Análisis contextual
        context_analysis = self._analyze_context(sentences, words, bigrams, trigrams)
        
        # Análisis de sentimiento contextual
        sentiment_context = self._analyze_sentiment_context(sentences, words)
        
        return {
            "original_text": text,
            "clean_text": clean_text,
            "sentences": sentences,
            "words": words,
            "filtered_words": filtered_words,
            "lemmatized_words": lemmatized_words,
            "bigrams": bigrams,
            "trigrams": trigrams,
            "context_analysis": context_analysis,
            "sentiment_context": sentiment_context,
            "text_length": len(clean_text),
            "word_count": len(words),
            "sentence_count": len(sentences)
        }
    
    def _clean_text(self, text: str) -> str:
        """Limpieza avanzada del texto"""
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
        
        # Remover emails
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Remover números pero mantener estructura
        text = re.sub(r'\b\d+\b', ' ', text)
        
        # Remover caracteres especiales pero mantener puntuación importante
        text = re.sub(r'[^\w\s\.\,\!\?\;\:]', ' ', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _analyze_context(self, sentences: List[str], words: List[str], 
                         bigrams: List[Tuple], trigrams: List[Tuple]) -> Dict[str, any]:
        """Análisis contextual del texto"""
        context_info = {
            "negation_count": 0,
            "intensifier_count": 0,
            "softener_count": 0,
            "context_positive_count": 0,
            "question_count": 0,
            "exclamation_count": 0,
            "conditional_phrases": 0
        }
        
        # Contar modificadores contextuales
        for word in words:
            if word in self.context_modifiers["negation"]:
                context_info["negation_count"] += 1
            elif word in self.context_modifiers["intensifiers"]:
                context_info["intensifier_count"] += 1
            elif word in self.context_modifiers["softeners"]:
                context_info["softener_count"] += 1
            elif word in self.context_modifiers["context_positive"]:
                context_info["context_positive_count"] += 1
        
        # Análisis de puntuación
        for sentence in sentences:
            if sentence.strip().endswith('?'):
                context_info["question_count"] += 1
            elif sentence.strip().endswith('!'):
                context_info["exclamation_count"] += 1
        
        # Detectar frases condicionales
        conditional_indicators = {"si", "if", "cuando", "when", "aunque", "although"}
        for word in words:
            if word in conditional_indicators:
                context_info["conditional_phrases"] += 1
        
        return context_info
    
    def _analyze_sentiment_context(self, sentences: List[str], words: List[str]) -> Dict[str, any]:
        """Análisis del contexto de sentimiento"""
        sentiment_info = {
            "positive_indicators": 0,
            "negative_indicators": 0,
            "neutral_indicators": 0,
            "mixed_sentiment": False
        }
        
        # Palabras indicadoras de sentimiento (simplificadas)
        positive_words = {"bueno", "excelente", "genial", "fantástico", "maravilloso", "good", "excellent", "great", "fantastic", "wonderful"}
        negative_words = {"malo", "terrible", "horrible", "pésimo", "awful", "bad", "terrible", "horrible", "awful", "terrible"}
        
        for word in words:
            if word in positive_words:
                sentiment_info["positive_indicators"] += 1
            elif word in negative_words:
                sentiment_info["negative_indicators"] += 1
            else:
                sentiment_info["neutral_indicators"] += 1
        
        # Detectar sentimiento mixto
        if sentiment_info["positive_indicators"] > 0 and sentiment_info["negative_indicators"] > 0:
            sentiment_info["mixed_sentiment"] = True
        
        return sentiment_info
    
    def _empty_result(self) -> Dict[str, any]:
        """Resultado vacío para textos nulos"""
        return {
            "original_text": "",
            "clean_text": "",
            "sentences": [],
            "words": [],
            "filtered_words": [],
            "lemmatized_words": [],
            "bigrams": [],
            "trigrams": [],
            "context_analysis": {},
            "sentiment_context": {},
            "text_length": 0,
            "word_count": 0,
            "sentence_count": 0
        }
    
    def get_context_score(self, preprocessed_data: Dict[str, any]) -> float:
        """
        Calcula un score contextual basado en el análisis del texto
        
        Args:
            preprocessed_data: Datos preprocesados del texto
            
        Returns:
            Score contextual entre 0.0 y 1.0
        """
        if not preprocessed_data or preprocessed_data["word_count"] == 0:
            return 0.0
        
        context_analysis = preprocessed_data["context_analysis"]
        sentiment_context = preprocessed_data["sentiment_context"]
        
        # Score base por modificadores contextuales
        context_score = 0.0
        
        # Negaciones reducen la toxicidad percibida
        if context_analysis["negation_count"] > 0:
            context_score -= 0.2 * min(context_analysis["negation_count"], 3)
        
        # Intensificadores aumentan la toxicidad
        if context_analysis["intensifier_count"] > 0:
            context_score += 0.15 * min(context_analysis["intensifier_count"], 3)
        
        # Suavizadores reducen la toxicidad
        if context_analysis["softener_count"] > 0:
            context_score -= 0.1 * min(context_analysis["softener_count"], 3)
        
        # Contexto positivo puede reducir toxicidad
        if context_analysis["context_positive_count"] > 0:
            context_score -= 0.1 * min(context_analysis["context_positive_count"], 2)
        
        # Preguntas pueden indicar menor toxicidad
        if context_analysis["question_count"] > 0:
            context_score -= 0.05 * min(context_analysis["question_count"], 2)
        
        # Exclamaciones pueden indicar mayor toxicidad
        if context_analysis["exclamation_count"] > 0:
            context_score += 0.1 * min(context_analysis["exclamation_count"], 3)
        
        # Sentimiento mixto puede indicar menor toxicidad
        if sentiment_context["mixed_sentiment"]:
            context_score -= 0.1
        
        # Normalizar entre 0.0 y 1.0
        context_score = max(-0.5, min(0.5, context_score))
        context_score = (context_score + 0.5) / 2  # Convertir a rango 0-1
        
        return context_score

# Instancia global del preprocesador
advanced_preprocessor = AdvancedTextPreprocessor()
