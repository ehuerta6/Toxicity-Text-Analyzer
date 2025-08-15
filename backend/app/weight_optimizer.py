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
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
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
                    score = self._calculate_metric(y_val, y_pred, metric)
                else:
                    y_pred = model.predict(weighted_X)
                    score = self._calculate_metric(y_train, y_pred, metric)
                
                # Actualizar mejores pesos si es necesario
                if score > best_score:
                    best_score = score
                    best_weights = weights.copy()
                    
                    # Calcular métricas completas
                    if validation_data:
                        best_metrics = self._calculate_all_metrics(y_val, y_pred)
                    else:
                        best_metrics = self._calculate_all_metrics(y_train, y_pred)
                    
                    logger.info(f"Nuevos mejores pesos encontrados. Score: {score:.3f}")
                    
            except Exception as e:
                logger.warning(f"Error evaluando pesos {weights}: {e}")
                continue
        
        # Resultados de optimización
        results = {
            "optimized_weights": best_weights,
            "best_score": best_score,
            "best_metrics": best_metrics,
            "optimization_metric": metric,
            "timestamp": datetime.now().isoformat(),
            "method": "grid_search"
        }
        
        logger.info(f"Optimización completada. Mejor score: {best_score:.3f}")
        return results
    
    def optimize_weights_genetic(self, training_data: List[Tuple[str, int, str]], 
                               population_size: int = 50, generations: int = 100,
                               metric: str = "f1") -> Dict[str, Any]:
        """
        Optimiza pesos usando algoritmo genético
        
        Args:
            training_data: Lista de tuplas (texto, etiqueta, categoría)
            population_size: Tamaño de la población
            generations: Número de generaciones
            metric: Métrica a optimizar
            
        Returns:
            Diccionario con pesos optimizados y métricas
        """
        if metric not in self.optimization_metrics:
            raise ValueError(f"Métrica no válida: {metric}")
        
        logger.info(f"Optimizando pesos usando algoritmo genético con métrica: {metric}")
        
        # Preparar datos
        X_train, y_train, category_weights = self._prepare_data_for_optimization(training_data)
        
        # Inicializar población
        population = self._initialize_population(population_size)
        
        best_weights = None
        best_score = 0
        best_metrics = {}
        
        for generation in range(generations):
            # Evaluar fitness de la población
            fitness_scores = []
            for weights in population:
                try:
                    score = self._evaluate_weights(weights, X_train, y_train, metric)
                    fitness_scores.append((score, weights))
                except Exception as e:
                    logger.warning(f"Error evaluando pesos: {e}")
                    fitness_scores.append((0, weights))
            
            # Ordenar por fitness
            fitness_scores.sort(reverse=True)
            
            # Actualizar mejor solución
            if fitness_scores[0][0] > best_score:
                best_score = fitness_scores[0][0]
                best_weights = fitness_scores[0][1].copy()
                
                # Calcular métricas completas
                y_pred = self._predict_with_weights(best_weights, X_train, y_train)
                best_metrics = self._calculate_all_metrics(y_train, y_pred)
                
                logger.info(f"Generación {generation}: Nuevo mejor score: {best_score:.3f}")
            
            # Selección y reproducción
            elite_size = max(1, population_size // 10)
            elite = [weights for _, weights in fitness_scores[:elite_size]]
            
            # Generar nueva población
            new_population = elite.copy()
            
            while len(new_population) < population_size:
                # Selección por torneo
                parent1 = self._tournament_selection(fitness_scores)
                parent2 = self._tournament_selection(fitness_scores)
                
                # Crossover
                child = self._crossover(parent1, parent2)
                
                # Mutación
                if np.random.random() < 0.1:
                    child = self._mutate(child)
                
                new_population.append(child)
            
            population = new_population
        
        # Resultados
        results = {
            "optimized_weights": best_weights,
            "best_score": best_score,
            "best_metrics": best_metrics,
            "optimization_metric": metric,
            "timestamp": datetime.now().isoformat(),
            "method": "genetic_algorithm",
            "generations": generations,
            "population_size": population_size
        }
        
        logger.info(f"Optimización genética completada. Mejor score: {best_score:.3f}")
        return results
    
    def _prepare_data_for_optimization(self, data: List[Tuple[str, int, str]]) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Prepara datos para optimización de pesos
        
        Args:
            data: Lista de tuplas (texto, etiqueta, categoría)
            
        Returns:
            Tuple con (características, etiquetas, categorías)
        """
        # Extraer características básicas del texto
        features = []
        labels = []
        categories = []
        
        for text, label, category in data:
            # Características del texto
            text_features = [
                len(text),  # Longitud del texto
                len(text.split()),  # Número de palabras
                sum(1 for c in text if c.isupper()),  # Mayúsculas
                sum(1 for c in text if c in '!?.'),  # Signos de puntuación
                sum(1 for word in text.lower().split() if len(word) > 6),  # Palabras largas
            ]
            
            features.append(text_features)
            labels.append(label)
            categories.append(category)
        
        return np.array(features), np.array(labels), categories
    
    def _generate_weight_grid(self) -> List[Dict[str, float]]:
        """
        Genera grid de pesos para Grid Search
        
        Returns:
            Lista de combinaciones de pesos
        """
        weight_combinations = []
        
        # Generar combinaciones de pesos
        for insulto_leve in np.arange(0.1, 0.6, 0.1):
            for insulto_moderado in np.arange(0.4, 0.9, 0.1):
                for insulto_severo in np.arange(0.7, 1.1, 0.1):
                    for acoso in np.arange(0.6, 1.1, 0.1):
                        for discriminacion in np.arange(0.7, 1.1, 0.1):
                            for spam in np.arange(0.2, 0.7, 0.1):
                                weights = {
                                    "insulto_leve": round(insulto_leve, 1),
                                    "insulto_moderado": round(insulto_moderado, 1),
                                    "insulto_severo": round(insulto_severo, 1),
                                    "acoso": round(acoso, 1),
                                    "discriminacion": round(discriminacion, 1),
                                    "spam": round(spam, 1)
                                }
                                weight_combinations.append(weights)
        
        return weight_combinations
    
    def _apply_weights_to_features(self, features: np.ndarray, weights: Dict[str, float]) -> np.ndarray:
        """
        Aplica pesos a las características
        
        Args:
            features: Características del texto
            weights: Pesos a aplicar
            
        Returns:
            Características ponderadas
        """
        # Por ahora, aplicar pesos de manera simple
        # En una implementación más avanzada, se podrían mapear características específicas a categorías
        weighted_features = features.copy()
        
        # Aplicar factor de peso general basado en la suma de pesos
        weight_factor = sum(weights.values()) / len(weights)
        weighted_features *= weight_factor
        
        return weighted_features
    
    def _calculate_metric(self, y_true: np.ndarray, y_pred: np.ndarray, metric: str) -> float:
        """
        Calcula una métrica específica
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Etiquetas predichas
            metric: Métrica a calcular
            
        Returns:
            Valor de la métrica
        """
        if metric == "f1":
            return f1_score(y_true, y_pred, average='weighted')
        elif metric == "precision":
            return precision_score(y_true, y_pred, average='weighted', zero_division=0)
        elif metric == "recall":
            return recall_score(y_true, y_pred, average='weighted', zero_division=0)
        elif metric == "balanced_accuracy":
            from sklearn.metrics import balanced_accuracy_score
            return balanced_accuracy_score(y_true, y_pred)
        else:
            raise ValueError(f"Métrica no soportada: {metric}")
    
    def _calculate_all_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calcula todas las métricas disponibles
        
        Args:
            y_true: Etiquetas verdaderas
            y_pred: Etiquetas predichas
            
        Returns:
            Diccionario con todas las métricas
        """
        return {
            "f1": f1_score(y_true, y_pred, average='weighted'),
            "precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
            "recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
            "accuracy": (y_true == y_pred).mean()
        }
    
    def _initialize_population(self, size: int) -> List[Dict[str, float]]:
        """
        Inicializa población para algoritmo genético
        
        Args:
            size: Tamaño de la población
            
        Returns:
            Lista de individuos (pesos)
        """
        population = []
        
        for _ in range(size):
            individual = {}
            for category, (min_weight, max_weight) in self.weight_ranges.items():
                individual[category] = round(np.random.uniform(min_weight, max_weight), 2)
            population.append(individual)
        
        return population
    
    def _evaluate_weights(self, weights: Dict[str, float], X: np.ndarray, 
                         y: np.ndarray, metric: str) -> float:
        """
        Evalúa un conjunto de pesos
        
        Args:
            weights: Pesos a evaluar
            X: Características
            y: Etiquetas
            metric: Métrica de evaluación
            
        Returns:
            Score de fitness
        """
        try:
            weighted_X = self._apply_weights_to_features(X, weights)
            y_pred = self._predict_with_weights(weights, X, y)
            return self._calculate_metric(y, y_pred, metric)
        except Exception:
            return 0.0
    
    def _predict_with_weights(self, weights: Dict[str, float], X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Hace predicciones usando pesos específicos
        
        Args:
            weights: Pesos a usar
            X: Características
            y: Etiquetas
            
        Returns:
            Predicciones
        """
        weighted_X = self._apply_weights_to_features(X, weights)
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(weighted_X, y)
        return model.predict(weighted_X)
    
    def _tournament_selection(self, fitness_scores: List[Tuple[float, Dict[str, float]]], 
                            tournament_size: int = 3) -> Dict[str, float]:
        """
        Selección por torneo para algoritmo genético
        
        Args:
            fitness_scores: Lista de (fitness, pesos)
            tournament_size: Tamaño del torneo
            
        Returns:
            Individuo seleccionado
        """
        tournament = np.random.choice(len(fitness_scores), tournament_size, replace=False)
        tournament_fitness = [fitness_scores[i] for i in tournament]
        return max(tournament_fitness, key=lambda x: x[0])[1]
    
    def _crossover(self, parent1: Dict[str, float], parent2: Dict[str, float]) -> Dict[str, float]:
        """
        Operador de crossover para algoritmo genético
        
        Args:
            parent1: Primer padre
            parent2: Segundo padre
            
        Returns:
            Hijo resultante
        """
        child = {}
        for category in parent1.keys():
            if np.random.random() < 0.5:
                child[category] = parent1[category]
            else:
                child[category] = parent2[category]
        return child
    
    def _mutate(self, individual: Dict[str, float], mutation_rate: float = 0.1) -> Dict[str, float]:
        """
        Operador de mutación para algoritmo genético
        
        Args:
            individual: Individuo a mutar
            mutation_rate: Tasa de mutación
            
        Returns:
            Individuo mutado
        """
        mutated = individual.copy()
        
        for category in mutated.keys():
            if np.random.random() < mutation_rate:
                min_weight, max_weight = self.weight_ranges[category]
                mutated[category] = round(np.random.uniform(min_weight, max_weight), 2)
        
        return mutated
    
    def save_optimized_weights(self, weights: Dict[str, float], filepath: str) -> bool:
        """
        Guarda pesos optimizados
        
        Args:
            weights: Pesos a guardar
            filepath: Ruta del archivo
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(weights, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Pesos optimizados guardados en: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando pesos: {e}")
            return False
    
    def load_optimized_weights(self, filepath: str) -> Optional[Dict[str, float]]:
        """
        Carga pesos optimizados guardados
        
        Args:
            filepath: Ruta del archivo
            
        Returns:
            Pesos cargados o None si hay error
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                weights = json.load(f)
            
            logger.info(f"Pesos optimizados cargados desde: {filepath}")
            return weights
            
        except Exception as e:
            logger.error(f"Error cargando pesos: {e}")
            return None

# Instancia global del optimizador
weight_optimizer = WeightOptimizer()
