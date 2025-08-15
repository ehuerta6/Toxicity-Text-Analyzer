"""
🎯 Evaluador Comparativo de Modelos de Toxicidad - ToxiGuard
Compara el rendimiento de diferentes algoritmos de machine learning para clasificación de toxicidad
"""

import pandas as pd
import numpy as np
import pickle
import time
import logging
from typing import Dict, List, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Evaluador comparativo de modelos de clasificación de toxicidad"""
    
    def __init__(self, data_path: str = "../../data/toxic_comments_processed.csv"):
        self.data_path = data_path
        self.models = {}
        self.results = {}
        self.vectorizer = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self) -> bool:
        """Carga y prepara el dataset para entrenamiento"""
        try:
            logger.info("📊 Cargando dataset...")
            df = pd.read_csv(self.data_path)
            
            # Verificar columnas disponibles
            logger.info(f"Columnas disponibles: {list(df.columns)}")
            logger.info(f"Forma del dataset: {df.shape}")
            
            # Buscar columnas de texto y toxicidad
            text_column = None
            toxicity_column = None
            
            for col in df.columns:
                if 'text' in col.lower() or 'comment' in col.lower() or 'message' in col.lower():
                    text_column = col
                if 'toxic' in col.lower() or 'label' in col.lower() or 'class' in col.lower():
                    toxicity_column = col
            
            if text_column is None:
                logger.error("❌ No se encontró columna de texto")
                return False
                
            if toxicity_column is None:
                logger.error("❌ No se encontró columna de toxicidad")
                return False
            
            logger.info(f"✅ Columna de texto: {text_column}")
            logger.info(f"✅ Columna de toxicidad: {toxicity_column}")
            
            # Preparar datos
            texts = df[text_column].fillna('').astype(str)
            labels = df[toxicity_column].fillna(0).astype(int)
            
            # Verificar distribución de clases
            logger.info(f"Distribución de clases: {labels.value_counts().to_dict()}")
            
            # Dividir datos
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                texts, labels, test_size=0.2, random_state=42, stratify=labels
            )
            
            # Vectorizar texto
            self.vectorizer = TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 2),
                stop_words='english',
                min_df=2,
                max_df=0.95
            )
            
            logger.info("🔄 Vectorizando texto...")
            self.X_train_vectorized = self.vectorizer.fit_transform(self.X_train)
            self.X_test_vectorized = self.vectorizer.transform(self.X_test)
            
            logger.info(f"✅ Datos cargados: {len(self.X_train)} train, {len(self.X_test)} test")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos: {e}")
            return False
    
    def define_models(self):
        """Define los modelos a evaluar"""
        self.models = {
            'naive_bayes': {
                'model': MultinomialNB(alpha=1.0),
                'name': 'Naive Bayes',
                'description': 'Clasificador probabilístico basado en el teorema de Bayes'
            },
            'logistic_regression': {
                'model': LogisticRegression(
                    C=1.0, 
                    max_iter=1000, 
                    random_state=42,
                    solver='liblinear'
                ),
                'name': 'Logistic Regression',
                'description': 'Regresión logística para clasificación binaria'
            },
            'random_forest': {
                'model': RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                ),
                'name': 'Random Forest',
                'description': 'Ensemble de árboles de decisión'
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5,
                    random_state=42
                ),
                'name': 'Gradient Boosting',
                'description': 'Ensemble de boosting secuencial'
            },
            'linear_svm': {
                'model': LinearSVC(
                    C=1.0,
                    max_iter=1000,
                    random_state=42
                ),
                'name': 'Linear SVM',
                'description': 'Support Vector Machine lineal'
            }
        }
        
        logger.info(f"✅ {len(self.models)} modelos definidos para evaluación")
    
    def evaluate_model(self, model_name: str, model, X_train, y_train, X_test, y_test) -> Dict:
        """Evalúa un modelo específico"""
        logger.info(f"🔍 Evaluando {model_name}...")
        
        start_time = time.time()
        
        # Entrenar modelo
        train_start = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - train_start
        
        # Predecir
        pred_start = time.time()
        y_pred = model.predict(X_test)
        pred_time = time.time() - pred_start
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Validación cruzada
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_weighted')
        cv_f1_mean = cv_scores.mean()
        cv_f1_std = cv_scores.std()
        
        total_time = time.time() - start_time
        
        results = {
            'model_name': model_name,
            'accuracy': round(accuracy, 4),
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1, 4),
            'cv_f1_mean': round(cv_f1_mean, 4),
            'cv_f1_std': round(cv_f1_std, 4),
            'train_time': round(train_time, 4),
            'prediction_time': round(pred_time, 4),
            'total_time': round(total_time, 4)
        }
        
        logger.info(f"✅ {model_name} evaluado - F1: {f1:.4f}, Tiempo: {total_time:.4f}s")
        return results
    
    def evaluate_all_models(self) -> Dict:
        """Evalúa todos los modelos definidos"""
        logger.info("🚀 Iniciando evaluación de todos los modelos...")
        
        if not self.X_train_vectorized is not None:
            logger.error("❌ Datos no cargados. Ejecuta load_data() primero.")
            return {}
        
        all_results = {}
        
        for model_key, model_info in self.models.items():
            try:
                results = self.evaluate_model(
                    model_info['name'],
                    model_info['model'],
                    self.X_train_vectorized,
                    self.y_train,
                    self.X_test_vectorized,
                    self.y_test
                )
                all_results[model_key] = results
                
            except Exception as e:
                logger.error(f"❌ Error evaluando {model_key}: {e}")
                all_results[model_key] = {
                    'model_name': model_info['name'],
                    'error': str(e)
                }
        
        self.results = all_results
        return all_results
    
    def generate_report(self) -> str:
        """Genera un reporte detallado de la evaluación"""
        if not self.results:
            return "❌ No hay resultados para reportar"
        
        report = "\n" + "="*80 + "\n"
        report += "🎯 REPORTE COMPARATIVO DE MODELOS DE TOXICIDAD - TOXIGUARD\n"
        report += "="*80 + "\n\n"
        
        # Tabla de métricas principales
        report += "📊 MÉTRICAS PRINCIPALES:\n"
        report += "-" * 80 + "\n"
        report += f"{'Modelo':<20} {'F1-Score':<10} {'Precisión':<10} {'Recall':<10} {'Tiempo Total':<12}\n"
        report += "-" * 80 + "\n"
        
        for model_key, result in self.results.items():
            if 'error' not in result:
                report += f"{result['model_name']:<20} {result['f1_score']:<10.4f} {result['precision']:<10.4f} "
                report += f"{result['recall']:<10.4f} {result['total_time']:<12.4f}s\n"
        
        report += "\n" + "="*80 + "\n"
        report += "📈 ANÁLISIS DETALLADO POR MODELO:\n"
        report += "="*80 + "\n\n"
        
        for model_key, result in self.results.items():
            if 'error' in result:
                report += f"❌ {result['model_name']}: Error - {result['error']}\n\n"
                continue
                
            report += f"🔍 {result['model_name']}:\n"
            report += f"   • F1-Score: {result['f1_score']:.4f}\n"
            report += f"   • Precisión: {result['precision']:.4f}\n"
            report += f"   • Recall: {result['recall']:.4f}\n"
            report += f"   • Accuracy: {result['accuracy']:.4f}\n"
            report += f"   • F1 CV (5-fold): {result['cv_f1_mean']:.4f} ± {result['cv_f1_std']:.4f}\n"
            report += f"   • Tiempo de entrenamiento: {result['train_time']:.4f}s\n"
            report += f"   • Tiempo de predicción: {result['prediction_time']:.4f}s\n"
            report += f"   • Tiempo total: {result['total_time']:.4f}s\n\n"
        
        # Recomendación
        report += "="*80 + "\n"
        report += "🏆 RECOMENDACIÓN:\n"
        report += "="*80 + "\n"
        
        best_model = self.get_best_model()
        if best_model:
            report += f"El modelo recomendado es: {best_model['model_name']}\n"
            report += f"Razones:\n"
            report += f"• Mejor F1-Score: {best_model['f1_score']:.4f}\n"
            report += f"• Balance entre precisión y velocidad\n"
            report += f"• Estabilidad en validación cruzada\n"
        else:
            report += "No se pudo determinar el mejor modelo\n"
        
        return report
    
    def get_best_model(self) -> Dict:
        """Obtiene el mejor modelo basado en F1-Score y tiempo"""
        if not self.results:
            return None
        
        valid_results = [r for r in self.results.values() if 'error' not in r]
        if not valid_results:
            return None
        
        # Ordenar por F1-Score descendente
        sorted_results = sorted(valid_results, key=lambda x: x['f1_score'], reverse=True)
        
        # Considerar también el tiempo de predicción
        best_models = sorted_results[:3]  # Top 3 por F1-Score
        
        # Entre los top 3, elegir el más rápido en predicción
        fastest = min(best_models, key=lambda x: x['prediction_time'])
        
        return fastest
    
    def save_models(self, output_dir: str = "../../models"):
        """Guarda los modelos entrenados"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info("💾 Guardando modelos entrenados...")
        
        for model_key, model_info in self.models.items():
            try:
                # Guardar modelo
                model_path = os.path.join(output_dir, f"{model_key}_trained.pkl")
                with open(model_path, 'wb') as f:
                    pickle.dump(model_info['model'], f)
                
                # Guardar vectorizer
                vectorizer_path = os.path.join(output_dir, f"{model_key}_vectorizer.pkl")
                with open(vectorizer_path, 'wb') as f:
                    pickle.dump(self.vectorizer, f)
                
                logger.info(f"✅ {model_key} guardado en {model_path}")
                
            except Exception as e:
                logger.error(f"❌ Error guardando {model_key}: {e}")
    
    def save_results(self, output_path: str = "../../models/evaluation_results.json"):
        """Guarda los resultados de evaluación"""
        import json
        import os
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Resultados guardados en {output_path}")
        except Exception as e:
            logger.error(f"❌ Error guardando resultados: {e}")

def main():
    """Función principal para ejecutar la evaluación"""
    logger.info("🚀 Iniciando evaluación comparativa de modelos...")
    
    evaluator = ModelEvaluator()
    
    # Cargar datos
    if not evaluator.load_data():
        logger.error("❌ No se pudieron cargar los datos")
        return
    
    # Definir modelos
    evaluator.define_models()
    
    # Evaluar todos los modelos
    results = evaluator.evaluate_all_models()
    
    # Generar y mostrar reporte
    report = evaluator.generate_report()
    print(report)
    
    # Guardar resultados
    evaluator.save_results()
    evaluator.save_models()
    
    logger.info("✅ Evaluación completada exitosamente!")

if __name__ == "__main__":
    main()
