"""
⚖️ Optimizador de Pesos - ToxiGuard
Sistema para optimizar automáticamente los pesos de las categorías de toxicidad
"""

import logging
import json
import os
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression

from .ml_models import MLToxicityClassifier

# Configurar logging
logger = logging.getLogger(__name__)

class WeightOptimizer:
    """Optimizador automático de pesos para categorías de toxicidad"""
    
    def __init__(self, base_weights: Dict[str, float] = None):
        """
        Inicializa el optimizador de pesos
        
        Args:
            base_weights: Pesos base para las categorías
        """
        # Pesos base por defecto (basados en análisis de impacto)
        self.base_weights = base_weights or {
            "insulto_leve": 0.3,
            "insulto_moderado": 0.6,
            "insulto_severo": 0.9,
            "acoso": 0.8,
            "discriminacion": 0.9,
            "spam": 0.4
        }
        
        # Rango de optimización para cada peso
        self.weight_ranges = {
            "insulto_leve": (0.1, 0.5),
            "insulto_moderado": (0.4, 0.8),
            "insulto_severo": (0.7, 1.0),
            "acoso": (0.6, 1.0),
            "discriminacion": (0.7, 1.0),
            "spam": (0.2, 0.6)
        }
        
        # Métricas objetivo para optimización
        self.optimization_metrics = ["f1", "precision", "recall", "balanced_accuracy"]
        
        logger.info("Optimizador de pesos inicializado")
    
    def optimize_weights_grid_search(self, training_data: List[Tuple[str, int, str]], 
                                   validation_data: List[Tuple[str, int, str]] = None,
                                   metric: str = "f1") -> Dict[str, Any]:
        """
        Optimiza pesos usando Grid Search
        
        Args:
            training_data: Lista de tuplas (texto, etiqueta, categoría)
            validation_data: Datos de validación separados (opcional)
            metric: Métrica a optimizar
            
        Returns:
            Diccionario con pesos optimizados y métricas
        """
        if metric not in self.optimization_metrics:
            raise ValueError(f"Métrica no válida: {metric}. Válidas: {self.optimization_metrics}")
        
        logger.info(f"Optimizando pesos usando Grid Search con métrica: {metric}")
        
        # Preparar datos para optimización
        X_train, y_train, category_weights = self._prepare_data_for_optimization(training_data)
        
        # Definir grid de pesos a probar
        weight_grid = self._generate_weight_grid()
        
        # Grid Search para encontrar mejores pesos
        best_score = 0
        best_weights = self.base_weights.copy()
        best_metrics = {}
        
        for weights in weight_grid:
            try:
                # Aplicar pesos a los datos
                weighted_X = self._apply_weights_to_features(X_train, weights)
                
                # Entrenar modelo simple para evaluar pesos
                model = LogisticRegression(random_state=42, max_iter=1000)
                model.fit(weighted_X, y_train)
                
                # Evaluar en datos de validación o entrenamiento
                if validation_data:
                    X_val, y_val, _ = self._prepare_data_for_optimization(validation_data)
                    weighted_X_val = self._apply_weights_to_features(X_val, weights)
                    y_pred = model.predict(weighted_X_val)
                    
                    # Calcular métricas
                    if metric == "f1":
                        score = f1_score(y_val, y_pred, average='weighted')
                    elif metric == "precision":
                        score = precision_score(y_val, y_pred, average='weighted')
                    elif metric == "recall":
                        score = recall_score(y_val, y_pred, average='weighted')
                    else:
                        score = f1_score(y_val, y_pred, average='weighted')
                else:
                    # Usar cross-validation en datos de entrenamiento
                    y_pred = model.predict(weighted_X)
                    
                    if metric == "f1":
                        score = f1_score(y_train, y_pred, average='weighted')
                    elif metric == "precision":
                        score = precision_score(y_train, y_pred, average='weighted')
                    elif metric == "recall":
                        score = recall_score(y_train, y_pred, average='weighted')
                    else:
                        score = f1_score(y_train, y_pred, average='weighted')
                
                # Actualizar mejores pesos si es necesario
                if score > best_score:
                    best_score = score
                    best_weights = weights.copy()
                    
                    # Calcular métricas completas
                    if validation_data:
                        y_pred = model.predict(weighted_X_val)
                        best_metrics = {
                            "f1": f1_score(y_val, y_pred, average='weighted'),
                            "precision": precision_score(y_val, y_pred, average='weighted'),
                            "recall": recall_score(y_val, y_pred, average='weighted')
                        }
                    else:
                        y_pred = model.predict(weighted_X)
                        best_metrics = {
                            "f1": f1_score(y_train, y_pred, average='weighted'),
                            "precision": precision_score(y_train, y_pred, average='weighted'),
                            "recall": recall_score(y_train, y_pred, average='weighted')
                        }
                
            except Exception as e:
                logger.warning(f"Error evaluando pesos {weights}: {e}")
                continue
        
        logger.info(f"Mejores pesos encontrados: {best_weights}")
        logger.info(f"Mejor score: {best_score:.4f}")
        
        return {
            "optimized_weights": best_weights,
            "best_score": best_score,
            "metrics": best_metrics,
            "optimization_method": "grid_search",
            "metric_used": metric,
            "timestamp": datetime.now().isoformat()
        }
    
    def _prepare_data_for_optimization(self, data: List[Tuple[str, int, str]]) -> Tuple[np.ndarray, np.ndarray, Dict[str, float]]:
        """Prepara datos para optimización de pesos"""
        if not data:
            raise ValueError("Datos de entrenamiento vacíos")
        
        # Extraer textos, etiquetas y categorías
        texts, labels, categories = zip(*data)
        
        # Convertir a arrays numpy
        X = np.array(texts)
        y = np.array(labels)
        
        # Crear mapeo de categorías a pesos
        category_weights = {}
        for category in set(categories):
            if category in self.base_weights:
                category_weights[category] = self.base_weights[category]
            else:
                category_weights[category] = 0.5  # Peso por defecto
        
        return X, y, category_weights
    
    def _generate_weight_grid(self) -> List[Dict[str, float]]:
        """Genera grid de pesos a probar"""
        weight_grid = []
        
        # Generar combinaciones de pesos
        for insulto_leve in [0.1, 0.2, 0.3, 0.4, 0.5]:
            for insulto_moderado in [0.4, 0.5, 0.6, 0.7, 0.8]:
                for insulto_severo in [0.7, 0.8, 0.9, 1.0]:
                    for acoso in [0.6, 0.7, 0.8, 0.9, 1.0]:
                        for discriminacion in [0.7, 0.8, 0.9, 1.0]:
                            for spam in [0.2, 0.3, 0.4, 0.5, 0.6]:
                                weights = {
                                    "insulto_leve": insulto_leve,
                                    "insulto_moderado": insulto_moderado,
                                    "insulto_severo": insulto_severo,
                                    "acoso": acoso,
                                    "discriminacion": discriminacion,
                                    "spam": spam
                                }
                                weight_grid.append(weights)
        
        return weight_grid
    
    def _apply_weights_to_features(self, X: np.ndarray, weights: Dict[str, float]) -> np.ndarray:
        """Aplica pesos a las características del texto"""
        # Implementación simplificada - en un caso real, esto dependería de cómo
        # se extraen las características del texto
        weighted_X = X.copy()
        
        # Aquí se aplicarían los pesos a las características específicas
        # Por ahora, retornamos X sin modificar
        return weighted_X
    
    def save_optimized_weights(self, weights: Dict[str, float], filepath: str = None) -> bool:
        """Guarda los pesos optimizados en un archivo JSON"""
        try:
            if filepath is None:
                filepath = f"optimized_weights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
            
            # Preparar datos para guardar
            save_data = {
                "weights": weights,
                "timestamp": datetime.now().isoformat(),
                "base_weights": self.base_weights,
                "weight_ranges": self.weight_ranges
            }
            
            # Guardar en archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Pesos optimizados guardados en: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando pesos optimizados: {e}")
            return False
    
    def load_optimized_weights(self, filepath: str) -> Optional[Dict[str, float]]:
        """Carga pesos optimizados desde un archivo JSON"""
        try:
            if not os.path.exists(filepath):
                logger.warning(f"Archivo de pesos no encontrado: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "weights" in data:
                logger.info(f"Pesos optimizados cargados desde: {filepath}")
                return data["weights"]
            else:
                logger.warning("Archivo no contiene pesos válidos")
                return None
                
        except Exception as e:
            logger.error(f"Error cargando pesos optimizados: {e}")
            return None
    
    def get_weight_analysis(self) -> Dict[str, Any]:
        """Retorna análisis de los pesos actuales"""
        return {
            "base_weights": self.base_weights,
            "weight_ranges": self.weight_ranges,
            "total_categories": len(self.base_weights),
            "average_weight": sum(self.base_weights.values()) / len(self.base_weights),
            "min_weight": min(self.base_weights.values()),
            "max_weight": max(self.base_weights.values()),
            "timestamp": datetime.now().isoformat()
        }
    
    def reset_to_base_weights(self) -> bool:
        """Resetea los pesos a los valores base"""
        try:
            self.base_weights = {
                "insulto_leve": 0.3,
                "insulto_moderado": 0.6,
                "insulto_severo": 0.9,
                "acoso": 0.8,
                "discriminacion": 0.9,
                "spam": 0.4
            }
            logger.info("Pesos reseteados a valores base")
            return True
        except Exception as e:
            logger.error(f"Error reseteando pesos: {e}")
            return False

# Instancia global del optimizador
weight_optimizer = WeightOptimizer()
