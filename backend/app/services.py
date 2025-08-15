"""
🔍 Servicios de Clasificación - ToxiGuard
Clasificador mejorado de toxicidad con categorización avanzada
"""

import re
import logging
from typing import List, Tuple, Dict

# Configurar logging
logger = logging.getLogger(__name__)

# Importar clasificador mejorado
try:
    from .improved_classifier import improved_classifier
    IMPROVED_CLASSIFIER_AVAILABLE = True
    logger.info("✅ Clasificador mejorado disponible")
except ImportError as e:
    IMPROVED_CLASSIFIER_AVAILABLE = False
    logger.warning(f"⚠️ Clasificador mejorado no disponible: {e}")

class ToxicityClassifier:
    """Clasificador mejorado de toxicidad con categorización avanzada"""
    
    def __init__(self):
        # Categorías de toxicidad con palabras clave específicas
        self.toxicity_categories = {
            "insulto": {
                "idiota", "estupido", "tonto", "imbecil", "pendejo", "gilipollas",
                "cabron", "hijo de puta", "puta", "perra", "zorra", "bastardo",
                "malparido", "desgraciado", "maldito", "condenado",
                "idiot", "stupid", "fool", "moron", "asshole", "bitch", "whore",
                "bastard", "damn", "hell", "fuck", "shit", "crap", "dumb"
            },
            "acoso": {
                "matar", "morir", "muerte", "odio", "odiar", "destruir",
                "kill", "die", "death", "hate", "destroy", "burn", "quemar",
                "amenaza", "amenazar", "threat", "threaten", "violence", "violent"
            },
            "discriminacion": {
                "racista", "xenofobo", "homofobo", "machista", "sexista",
                "racist", "xenophobic", "homophobic", "sexist", "bigot",
                "nazi", "fascista", "fascist", "supremacist"
            },
            "spam": {
                "spam", "basura", "mierda", "garbage", "trash", "shit",
                "comprar", "vender", "buy", "sell", "oferta", "offer"
            }
        }
        
        # Combinar todas las palabras clave para búsqueda general
        self.toxic_keywords = set()
        for category_words in self.toxicity_categories.values():
            self.toxic_keywords.update(category_words)
        
        # Umbral dinámico basado en la intensidad del contenido
        self.base_threshold = 0.25
        
        # Pesos por categoría para scoring más preciso
        self.category_weights = {
            "insulto": 1.0,
            "acoso": 1.5,
            "discriminacion": 1.3,
            "spam": 0.7
        }
        
        # Compilar regex para búsqueda eficiente
        self._compile_patterns()
        
        logger.info(f"Clasificador inicializado con {len(self.toxic_keywords)} palabras clave")
    
    def _compile_patterns(self):
        """Compila los patrones regex para búsqueda eficiente"""
        self.keyword_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
            re.IGNORECASE
        )
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str], int, int, str, float]:
        """
        Analiza un texto y determina su toxicidad con categorización mejorada
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tuple con (es_toxico, score, etiquetas, longitud_texto, palabras_encontradas, categoria, porcentaje)
        """
        if not text or not text.strip():
            return False, 0.0, [], 0, 0, None, 0.0
        
        # Intentar usar el clasificador mejorado si está disponible
        if IMPROVED_CLASSIFIER_AVAILABLE:
            try:
                logger.debug("Usando clasificador mejorado")
                return improved_classifier.analyze_text(text)
            except Exception as e:
                logger.warning(f"Error en clasificador mejorado, usando fallback: {e}")
        
        # Fallback al clasificador original
        logger.debug("Usando clasificador original (fallback)")
        return self._analyze_text_legacy(text)
    
    def _analyze_text_legacy(self, text: str) -> Tuple[bool, float, List[str], int, int, str, float]:
        """Método legacy del clasificador original"""
        # Limpiar y normalizar texto
        clean_text = self._normalize_text(text)
        text_length = len(clean_text)
        
        # Encontrar palabras clave tóxicas por categoría
        category_matches = self._find_category_matches(clean_text)
        total_matches = sum(category_matches.values())
        
        # Calcular score dinámico
        score, is_toxic, category, labels = self._calculate_dynamic_score(
            clean_text, category_matches, total_matches, text_length
        )
        
        # Calcular porcentaje de toxicidad
        toxicity_percentage = round(score * 100, 1)
        
        # Logs para debugging
        logger.debug(f"Texto: '{text[:50]}...' -> Score: {score:.3f}, Tóxico: {is_toxic}")
        
        return is_toxic, score, labels, text_length, total_matches, category, toxicity_percentage
    
    def _normalize_text(self, text: str) -> str:
        """Normalización mejorada del texto"""
        # Convertir a minúsculas y remover espacios extra
        text = text.lower().strip()
        
        # Remover caracteres especiales pero mantener estructura
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _find_category_matches(self, clean_text: str) -> Dict[str, int]:
        """Encuentra coincidencias por categoría de manera eficiente"""
        category_matches = {}
        
        for category, keywords in self.toxicity_categories.items():
            # Crear patrón específico para la categoría
            category_pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b',
                re.IGNORECASE
            )
            matches = category_pattern.findall(clean_text)
            category_matches[category] = len(matches)
        
        return category_matches
    
    def _calculate_dynamic_score(self, clean_text: str, category_matches: Dict[str, int], 
                                total_matches: int, text_length: int) -> Tuple[float, bool, str, List[str]]:
        """Calcula score dinámico basado en múltiples factores"""
        
        if total_matches == 0:
            return 0.0, False, None, []
        
        # Score base por palabras encontradas
        weighted_score = sum(
            count * self.category_weights[cat] 
            for cat, count in category_matches.items() 
            if count > 0
        )
        
        # Factor de densidad (palabras tóxicas por longitud)
        density_factor = min(0.6, total_matches / max(text_length / 15, 1))
        
        # Factor de intensidad (múltiples palabras de la misma categoría)
        intensity_factor = min(0.4, sum(count ** 0.5 for count in category_matches.values() if count > 0) / 10)
        
        # Score combinado
        base_score = min(0.8, weighted_score * 0.2)
        combined_score = min(1.0, base_score + density_factor + intensity_factor)
        
        # Ajuste por categoría dominante
        if total_matches > 0:
            dominant_category = max(category_matches.items(), key=lambda x: x[1] * self.category_weights[x[0]])
            category_weight = self.category_weights[dominant_category[0]]
            combined_score = min(1.0, combined_score * (1 + category_weight * 0.1))
        
        # Umbral dinámico basado en la intensidad
        dynamic_threshold = self.base_threshold
        if total_matches > 2:
            dynamic_threshold *= 0.8  # Más sensible para múltiples palabras
        if text_length < 20 and total_matches > 0:
            dynamic_threshold *= 0.7  # Más sensible para textos cortos
        
        # Determinar si es tóxico
        is_toxic = combined_score >= dynamic_threshold
        
        # Determinar categoría principal
        if total_matches > 0:
            category = max(category_matches.items(), key=lambda x: x[1] * self.category_weights[x[0]])[0]
            labels = [category, "detected"]
        else:
            category = None
            labels = []
        
        return combined_score, is_toxic, category, labels
    
    def get_keywords_list(self) -> List[str]:
        """Retorna la lista de palabras clave tóxicas"""
        return sorted(list(self.toxic_keywords))
    
    def get_categories_info(self) -> Dict[str, Dict]:
        """Retorna información detallada de las categorías"""
        return {
            category: {
                "keywords": sorted(list(keywords)),
                "count": len(keywords),
                "weight": weight
            }
            for category, keywords in self.toxicity_categories.items()
        }
    
    def add_keyword(self, keyword: str, category: str = "insulto") -> None:
        """Añade una nueva palabra clave tóxica a una categoría específica"""
        if keyword and keyword.strip() and category in self.toxicity_categories:
            keyword_lower = keyword.lower().strip()
            self.toxicity_categories[category].add(keyword_lower)
            self.toxic_keywords.add(keyword_lower)
            
            # Recompilar el patrón regex
            self._compile_patterns()
            logger.info(f"Palabra clave '{keyword}' añadida a categoría '{category}'")
    
    def remove_keyword(self, keyword: str) -> bool:
        """Remueve una palabra clave tóxica de todas las categorías"""
        keyword_lower = keyword.lower()
        removed = False
        
        for category in self.toxicity_categories:
            if keyword_lower in self.toxicity_categories[category]:
                self.toxicity_categories[category].remove(keyword_lower)
                removed = True
        
        if keyword_lower in self.toxic_keywords:
            self.toxic_keywords.remove(keyword_lower)
            removed = True
        
        if removed:
            # Recompilar el patrón regex
            self._compile_patterns()
            logger.info(f"Palabra clave '{keyword}' removida")
        
        return removed
    
    def get_toxicity_threshold(self) -> float:
        """Retorna el umbral actual de toxicidad"""
        return self.base_threshold
    
    def set_toxicity_threshold(self, threshold: float) -> None:
        """Establece un nuevo umbral de toxicidad"""
        if 0.0 <= threshold <= 1.0:
            self.base_threshold = threshold
            logger.info(f"Umbral de toxicidad actualizado a {threshold}")
        else:
            raise ValueError("El umbral debe estar entre 0.0 y 1.0")

# Instancia global del clasificador
toxicity_classifier = ToxicityClassifier()
