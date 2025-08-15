"""
🎯 Clasificador Mejorado de Toxicidad - ToxiGuard
Implementa análisis contextual y scoring adaptativo para mayor precisión
"""

import re
import logging
from typing import List, Tuple, Dict, Set
from collections import Counter
from .advanced_preprocessor import advanced_preprocessor

# Configurar logging
logger = logging.getLogger(__name__)

class ImprovedToxicityClassifier:
    """Clasificador mejorado con análisis contextual y scoring adaptativo"""
    
    def __init__(self):
        # Categorías de toxicidad con palabras clave específicas y pesos contextuales
        self.toxicity_categories = {
            "insulto_leve": {
                "keywords": {"tonto", "feo", "lento", "aburrido", "stupid", "ugly", "slow", "boring"},
                "base_weight": 0.2,  # Reducido de 0.3 a 0.2
                "context_multiplier": 0.6,  # Reducido de 0.8 a 0.6
                "requires_context": True
            },
            "insulto_moderado": {
                "keywords": {"idiota", "estupido", "imbecil", "idiot", "stupid", "moron", "fool"},
                "base_weight": 0.5,  # Reducido de 0.6 a 0.5
                "context_multiplier": 1.0,
                "requires_context": False
            },
            "insulto_severo": {
                "keywords": {"pendejo", "cabron", "hijo de puta", "asshole", "bitch", "bastard"},
                "base_weight": 0.9,
                "context_multiplier": 1.2,
                "requires_context": False
            },
            "acoso": {
                "keywords": {"matar", "morir", "odio", "destruir", "kill", "die", "hate", "destroy"},
                "base_weight": 0.8,
                "context_multiplier": 1.1,
                "requires_context": True
            },
            "discriminacion": {
                "keywords": {"racista", "xenofobo", "homofobo", "racist", "xenophobic", "homophobic"},
                "base_weight": 0.9,
                "context_multiplier": 1.3,
                "requires_context": True
            },
            "spam": {
                "keywords": {"spam", "basura", "mierda", "garbage", "trash", "comprar", "vender"},
                "base_weight": 0.3,  # Reducido de 0.4 a 0.3
                "context_multiplier": 0.8,  # Reducido de 0.9 a 0.8
                "requires_context": False
            }
        }
        
        # Umbrales adaptativos ajustados para ser menos sensibles
        self.adaptive_thresholds = {
            "low_context": 0.45,     # Reducido de 0.5 a 0.45
            "medium_context": 0.35,  # Reducido de 0.4 a 0.35
            "high_context": 0.30,    # Reducido de 0.35 a 0.30
            "isolated_words": 0.65   # Reducido de 0.7 a 0.65
        }
        
        # Compilar patrones regex
        self._compile_patterns()
        
        logger.info("Clasificador mejorado inicializado con umbrales ajustados")
    
    def _compile_patterns(self):
        """Compila patrones regex para búsqueda eficiente"""
        self.category_patterns = {}
        
        for category_name, category_info in self.toxicity_categories.items():
            keywords = category_info["keywords"]
            if keywords:
                pattern = re.compile(
                    r'\b(' + '|'.join(map(re.escape, keywords)) + r')\b',
                    re.IGNORECASE
                )
                self.category_patterns[category_name] = pattern
    
    def analyze_text(self, text: str) -> Tuple[bool, float, List[str], int, int, str, float]:
        """
        Análisis mejorado de toxicidad con contexto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Tuple con (es_toxico, score, etiquetas, longitud_texto, palabras_encontradas, categoria, porcentaje)
        """
        if not text or not text.strip():
            return False, 0.0, [], 0, 0, None, 0.0
        
        # Preprocesamiento avanzado
        preprocessed_data = advanced_preprocessor.preprocess_text(text)
        
        # Análisis de toxicidad por categoría
        category_analysis = self._analyze_categories(preprocessed_data)
        
        # Scoring contextual
        context_score = advanced_preprocessor.get_context_score(preprocessed_data)
        
        # Score final combinado
        final_score, is_toxic, category, labels = self._calculate_contextual_score(
            preprocessed_data, category_analysis, context_score
        )
        
        # Calcular porcentaje
        toxicity_percentage = round(final_score * 100, 1)
        
        # Logs para debugging
        logger.debug(f"Texto: '{text[:50]}...' -> Score: {final_score:.3f}, Tóxico: {is_toxic}, Contexto: {context_score:.3f}")
        
        return is_toxic, final_score, labels, preprocessed_data["text_length"], sum(category_analysis.values()), category, toxicity_percentage
    
    def _analyze_categories(self, preprocessed_data: Dict) -> Dict[str, int]:
        """Analiza coincidencias por categoría"""
        category_matches = {}
        clean_text = preprocessed_data["clean_text"]
        
        for category_name, category_info in self.toxicity_categories.items():
            if category_name in self.category_patterns:
                pattern = self.category_patterns[category_name]
                matches = pattern.findall(clean_text)
                category_matches[category_name] = len(matches)
            else:
                category_matches[category_name] = 0
        
        return category_matches
    
    def _calculate_contextual_score(self, preprocessed_data: Dict, category_analysis: Dict[str, int], 
                                   context_score: float) -> Tuple[float, bool, str, List[str]]:
        """Calcula score contextual considerando múltiples factores"""
        
        total_matches = sum(category_analysis.values())
        if total_matches == 0:
            return 0.0, False, None, []
        
        # Score base por categorías
        category_score = 0.0
        category_weights = {}
        
        for category_name, match_count in category_analysis.items():
            if match_count > 0:
                category_info = self.toxicity_categories[category_name]
                base_weight = category_info["base_weight"]
                context_multiplier = category_info["context_multiplier"]
                
                # Ajustar peso por contexto
                adjusted_weight = base_weight * context_multiplier
                
                # Si requiere contexto y hay poco contexto, reducir peso significativamente
                if category_info["requires_context"] and preprocessed_data["word_count"] < 15:
                    adjusted_weight *= 0.5  # Reducido de 0.7 a 0.5
                
                # Aumentar peso para categorías severas
                if category_name in ["acoso", "discriminacion", "insulto_severo"]:
                    adjusted_weight *= 1.3  # Multiplicador adicional para contenido severo
                
                category_score += match_count * adjusted_weight
                category_weights[category_name] = adjusted_weight
        
        # Factor de densidad contextual
        word_count = preprocessed_data["word_count"]
        sentence_count = preprocessed_data["sentence_count"]
        
        # Textos con más contexto tienen menor densidad crítica
        if sentence_count > 2:
            density_threshold = word_count / 30  # Aumentado de 25 a 30
        elif sentence_count > 1:
            density_threshold = word_count / 25  # Aumentado de 20 a 25
        else:
            density_threshold = word_count / 20  # Aumentado de 15 a 20
        
        density_factor = min(0.4, total_matches / max(density_threshold, 1))  # Reducido de 0.5 a 0.4
        
        # Factor de intensidad por categoría
        intensity_factor = 0.0
        for category_name, match_count in category_analysis.items():
            if match_count > 0:
                # Múltiples palabras de la misma categoría aumentan intensidad
                intensity_factor += min(0.25, (match_count ** 0.7) / 12)  # Reducido de 0.3 a 0.25
        
        # Score combinado
        base_score = min(0.7, category_score * 0.25)  # Reducido de 0.8 a 0.7 y de 0.3 a 0.25
        combined_score = min(1.0, base_score + density_factor + intensity_factor)
        
        # Ajuste por contexto más agresivo
        context_adjustment = (context_score - 0.5) * 0.3  # Aumentado de 0.2 a 0.3
        combined_score = max(0.0, min(1.0, combined_score + context_adjustment))
        
        # Ajuste adicional para contenido severo
        if any(category_analysis.get(severity_cat, 0) > 0 for severity_cat in ["acoso", "discriminacion", "insulto_severo"]):
            combined_score = min(1.0, combined_score * 1.2)  # Aumentar score para contenido severo
        
        # Umbral adaptativo
        threshold = self._get_adaptive_threshold(preprocessed_data, total_matches)
        
        # Determinar si es tóxico
        is_toxic = combined_score >= threshold
        
        # Determinar categoría principal
        if total_matches > 0:
            # Priorizar categorías más severas
            severity_order = ["discriminacion", "acoso", "insulto_severo", "insulto_moderado", "insulto_leve", "spam"]
            
            for severity_cat in severity_order:
                if category_analysis.get(severity_cat, 0) > 0:
                    category = severity_cat
                    break
            else:
                # Si no hay categoría severa, usar la más frecuente
                category = max(category_analysis.items(), key=lambda x: x[1])[0]
            
            labels = [category, "context_aware", "improved"]
        else:
            category = None
            labels = []
        
        return combined_score, is_toxic, category, labels
    
    def _get_adaptive_threshold(self, preprocessed_data: Dict, total_matches: int) -> float:
        """Determina umbral adaptativo basado en el contexto"""
        word_count = preprocessed_data["word_count"]
        sentence_count = preprocessed_data["sentence_count"]
        
        # Palabras aisladas requieren umbral más alto
        if word_count <= 5 and total_matches > 0:  # Aumentado de 3 a 5
            return self.adaptive_thresholds["isolated_words"]
        
        # Determinar nivel de contexto
        if sentence_count >= 3 and word_count >= 40:  # Aumentado de 30 a 40
            context_level = "high_context"
        elif sentence_count >= 2 and word_count >= 20:  # Aumentado de 15 a 20
            context_level = "medium_context"
        else:
            context_level = "low_context"
        
        base_threshold = self.adaptive_thresholds[context_level]
        
        # Ajustar por número de coincidencias
        if total_matches > 3:
            base_threshold *= 0.8  # Más sensible para múltiples palabras
        elif total_matches == 1:
            base_threshold *= 1.3  # Menos sensible para palabras únicas (aumentado de 1.2 a 1.3)
        
        return max(0.15, min(0.85, base_threshold))  # Ajustado rango de 0.1-0.8 a 0.15-0.85
    
    def get_detailed_analysis(self, text: str) -> Dict:
        """Retorna análisis detallado del texto"""
        if not text or not text.strip():
            return {}
        
        preprocessed_data = advanced_preprocessor.preprocess_text(text)
        category_analysis = self._analyze_categories(preprocessed_data)
        context_score = advanced_preprocessor.get_context_score(preprocessed_data)
        
        return {
            "preprocessing": preprocessed_data,
            "category_analysis": category_analysis,
            "context_score": context_score,
            "context_analysis": preprocessed_data["context_analysis"],
            "sentiment_context": preprocessed_data["sentiment_context"],
            "adaptive_threshold": self._get_adaptive_threshold(preprocessed_data, sum(category_analysis.values()))
        }
    
    def get_categories_info(self) -> Dict[str, Dict]:
        """Retorna información detallada de las categorías"""
        return {
            category_name: {
                "keywords": sorted(list(category_info["keywords"])),
                "count": len(category_info["keywords"]),
                "base_weight": category_info["base_weight"],
                "context_multiplier": category_info["context_multiplier"],
                "requires_context": category_info["requires_context"]
            }
            for category_name, category_info in self.toxicity_categories.items()
        }
    
    def add_keyword(self, keyword: str, category: str = "insulto_leve") -> None:
        """Añade nueva palabra clave"""
        if keyword and keyword.strip() and category in self.toxicity_categories:
            keyword_lower = keyword.lower().strip()
            self.toxicity_categories[category]["keywords"].add(keyword_lower)
            self._compile_patterns()
            logger.info(f"Palabra clave '{keyword}' añadida a categoría '{category}'")
    
    def remove_keyword(self, keyword: str) -> bool:
        """Remueve palabra clave"""
        keyword_lower = keyword.lower()
        removed = False
        
        for category_info in self.toxicity_categories.values():
            if keyword_lower in category_info["keywords"]:
                category_info["keywords"].remove(keyword_lower)
                removed = True
        
        if removed:
            self._compile_patterns()
            logger.info(f"Palabra clave '{keyword}' removida")
        
        return removed

# Instancia global del clasificador mejorado
improved_classifier = ImprovedToxicityClassifier()
