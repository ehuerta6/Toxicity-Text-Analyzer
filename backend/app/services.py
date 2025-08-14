import re
from typing import List, Tuple

class ToxicityClassifier:
    """Clasificador naïve de toxicidad basado en palabras clave"""
    
    def __init__(self):
        # Lista de palabras clave tóxicas (ejemplos en español e inglés)
        self.toxic_keywords = {
            # Insultos generales
            "idiota", "estupido", "tonto", "imbecil", "pendejo", "gilipollas",
            "cabron", "hijo de puta", "puta", "perra", "zorra", "bastardo",
            "malparido", "desgraciado", "maldito", "condenado",
            
            # Palabras ofensivas en inglés
            "idiot", "stupid", "fool", "moron", "asshole", "bitch", "whore",
            "bastard", "damn", "hell", "fuck", "shit", "crap", "dumb",
            
            # Acoso y amenazas
            "matar", "morir", "muerte", "odio", "odiar", "destruir",
            "kill", "die", "death", "hate", "destroy", "burn", "quemar",
            
            # Discriminación
            "racista", "xenofobo", "homofobo", "machista", "sexista",
            "racist", "xenophobic", "homophobic", "sexist", "bigot",
            
            # Spam y contenido no deseado
            "spam", "basura", "mierda", "garbage", "trash", "shit"
        }
        
        # Umbral para considerar texto como tóxico
        self.toxicity_threshold = 0.34
        
        # Compilar regex para búsqueda eficiente
        self.keyword_pattern = re.compile(
            r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
            re.IGNORECASE
        )
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str], int, int]:
        """
        Analiza un texto y determina su toxicidad
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tuple con (es_toxico, score, etiquetas, longitud_texto, palabras_encontradas)
        """
        if not text or not text.strip():
            return False, 0.0, [], 0, 0
        
        # Limpiar y normalizar texto
        clean_text = text.lower().strip()
        text_length = len(clean_text)
        
        # Encontrar palabras clave tóxicas
        matches = self.keyword_pattern.findall(clean_text)
        keywords_found = len(matches)
        
        # Calcular score de toxicidad
        if keywords_found == 0:
            score = 0.0
            is_toxic = False
            labels = []
        else:
            # Score proporcional a la cantidad de palabras encontradas
            # Normalizado por la longitud del texto para evitar sesgos
            score = min(1.0, (keywords_found * 0.2) + (keywords_found / max(text_length, 1) * 0.8))
            is_toxic = score >= self.toxicity_threshold
            labels = ["insulto"] if is_toxic else []
        
        return is_toxic, score, labels, text_length, keywords_found
    
    def get_keywords_list(self) -> List[str]:
        """Retorna la lista de palabras clave tóxicas"""
        return sorted(list(self.toxic_keywords))
    
    def add_keyword(self, keyword: str) -> None:
        """Añade una nueva palabra clave tóxica"""
        if keyword and keyword.strip():
            self.toxic_keywords.add(keyword.lower().strip())
            # Recompilar el patrón regex
            self.keyword_pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
                re.IGNORECASE
            )
    
    def remove_keyword(self, keyword: str) -> bool:
        """Remueve una palabra clave tóxica"""
        if keyword.lower() in self.toxic_keywords:
            self.toxic_keywords.remove(keyword.lower())
            # Recompilar el patrón regex
            self.keyword_pattern = re.compile(
                r'\b(' + '|'.join(map(re.escape, self.toxic_keywords)) + r')\b',
                re.IGNORECASE
            )
            return True
        return False

# Instancia global del clasificador
toxicity_classifier = ToxicityClassifier()
