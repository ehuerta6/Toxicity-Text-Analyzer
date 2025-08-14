import re
from typing import List, Tuple, Dict
from datetime import datetime

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
        
        # Umbral para considerar texto como tóxico
        self.toxicity_threshold = 0.3
        
        # Pesos por categoría para scoring más preciso
        self.category_weights = {
            "insulto": 1.0,
            "acoso": 1.5,
            "discriminacion": 1.3,
            "spam": 0.7
        }
        
        # Compilar regex para búsqueda eficiente
        self.keyword_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
            re.IGNORECASE
        )
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str], int, int, str, float]:
        """
        Analiza un texto y determina su toxicidad con categorización
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tuple con (es_toxico, score, etiquetas, longitud_texto, palabras_encontradas, categoria, porcentaje)
        """
        if not text or not text.strip():
            return False, 0.0, [], 0, 0, None, 0.0
        
        # Limpiar y normalizar texto
        clean_text = text.lower().strip()
        text_length = len(clean_text)
        
        # Encontrar palabras clave tóxicas por categoría
        category_matches = {}
        total_matches = 0
        
        for category, keywords in self.toxicity_categories.items():
            category_pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b',
                re.IGNORECASE
            )
            matches = category_pattern.findall(clean_text)
            category_matches[category] = len(matches)
            total_matches += len(matches)
        
        # Determinar la categoría principal
        if total_matches == 0:
            score = 0.0
            is_toxic = False
            labels = []
            category = None
            toxicity_percentage = 0.0
        else:
            # Calcular score ponderado por categoría
            weighted_score = sum(
                count * self.category_weights[cat] 
                for cat, count in category_matches.items() 
                if count > 0
            )
            
            # Fórmula mejorada: más sensible a palabras tóxicas
            # Base score por palabras encontradas + factor de densidad
            base_score = min(1.0, weighted_score * 0.25)  # Cada palabra tóxica agrega al score
            density_score = min(0.5, total_matches / max(text_length / 20, 1))  # Densidad de toxicidad
            score = min(1.0, base_score + density_score)
            
            # Si hay palabras tóxicas, score mínimo de 0.4
            if total_matches > 0:
                score = max(score, 0.4)
            
            # Determinar si es tóxico
            is_toxic = score >= self.toxicity_threshold
            
            # Determinar categoría principal
            if total_matches > 0:
                category = max(category_matches.items(), key=lambda x: x[1] * self.category_weights[x[0]])[0]
                labels = [category, "detected"]
            else:
                category = None
                labels = []
            
            # Calcular porcentaje de toxicidad
            toxicity_percentage = round(score * 100, 1)
        
        return is_toxic, score, labels, text_length, total_matches, category, toxicity_percentage
    
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
            self.toxicity_categories[category].add(keyword.lower().strip())
            self.toxic_keywords.add(keyword.lower().strip())
            # Recompilar el patrón regex
            self.keyword_pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
                re.IGNORECASE
            )
    
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
            self.keyword_pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
                re.IGNORECASE
            )
        
        return removed

# Instancia global del clasificador
toxicity_classifier = ToxicityClassifier()
