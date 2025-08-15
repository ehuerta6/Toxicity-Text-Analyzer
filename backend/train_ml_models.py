#!/usr/bin/env python3
"""
🚀 Script de Entrenamiento de Modelos ML - ToxiGuard
Entrena y evalúa diferentes modelos de Machine Learning para clasificación de toxicidad
"""

import sys
import os
import logging
import argparse
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(Path(__file__).parent))

from app.model_trainer import model_trainer
from app.weight_optimizer import weight_optimizer
from app.ml_models import MLToxicityClassifier

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_data():
    """
    Crea datos de ejemplo para entrenamiento si no existen
    
    Returns:
        Lista de tuplas (texto, etiqueta, categoría)
    """
    sample_data = [
        # Textos tóxicos
        ("Eres un idiota estúpido", 1, "insulto_severo"),
        ("Odio a todas las personas como tú", 1, "acoso"),
        ("Los negros son inferiores", 1, "discriminacion"),
        ("Compra esto ahora, oferta limitada", 1, "spam"),
        ("Eres feo y aburrido", 1, "insulto_leve"),
        ("Vete a la mierda", 1, "insulto_moderado"),
        ("Te voy a matar", 1, "acoso"),
        ("Los gays son enfermos", 1, "discriminacion"),
        ("Este producto es basura", 1, "spam"),
        ("Eres lento y tonto", 1, "insulto_leve"),
        
        # Textos no tóxicos
        ("Hola, ¿cómo estás?", 0, "normal"),
        ("El clima está muy agradable hoy", 0, "normal"),
        ("Me gusta la música clásica", 0, "normal"),
        ("La comida está deliciosa", 0, "normal"),
        ("Vamos al parque a pasear", 0, "normal"),
        ("El libro es muy interesante", 0, "normal"),
        ("La película fue entretenida", 0, "normal"),
        ("El café tiene un aroma agradable", 0, "normal"),
        ("La ciudad es muy bonita", 0, "normal"),
        ("El deporte es saludable", 0, "normal"),
        
        # Casos límite
        ("Este video es tonto pero divertido", 0, "contexto_positivo"),
        ("La película es aburrida pero tiene buenos efectos", 0, "contexto_positivo"),
        ("El personaje es malo pero la historia es buena", 0, "contexto_positivo"),
        ("Odio cuando llueve", 0, "expresion_legitima"),
        ("Me molesta el ruido", 0, "expresion_legitima"),
        ("No me gusta la comida picante", 0, "expresion_legitima"),
    ]
    
    return sample_data

def train_models_with_sample_data():
    """
    Entrena modelos usando datos de ejemplo
    
    Returns:
        Diccionario con resultados del entrenamiento
    """
    logger.info("🎯 Entrenando modelos con datos de ejemplo...")
    
    # Crear datos de ejemplo
    sample_data = create_sample_data()
    
    # Separar textos y etiquetas
    texts = [item[0] for item in sample_data]
    labels = [item[1] for item in sample_data]
    
    logger.info(f"📊 Datos preparados: {len(texts)} muestras")
    logger.info(f"📈 Distribución: {sum(labels)} tóxicos, {len(labels) - sum(labels)} no tóxicos")
    
    # Entrenar todos los modelos
    logger.info("🚀 Iniciando entrenamiento de modelos...")
    
    try:
        results = model_trainer.train_all_models(texts, labels, use_grid_search=True)
        
        if results:
            logger.info("✅ Entrenamiento completado exitosamente")
            
            # Comparar modelos
            comparison = model_trainer.compare_models(results)
            
            # Generar reporte
            report = model_trainer.generate_model_report(comparison)
            print("\n" + "="*60)
            print("📊 REPORTE DE ENTRENAMIENTO")
            print("="*60)
            print(report)
            
            # Guardar resultados
            results_file = model_trainer.save_training_results({
                "training_results": results,
                "comparison": comparison,
                "sample_data_info": {
                    "total_samples": len(texts),
                    "toxic_samples": sum(labels),
                    "non_toxic_samples": len(labels) - sum(labels)
                }
            })
            
            logger.info(f"💾 Resultados guardados en: {results_file}")
            
            return results
            
        else:
            logger.error("❌ No se pudieron entrenar los modelos")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error durante el entrenamiento: {e}")
        return None

def optimize_weights_with_sample_data():
    """
    Optimiza pesos usando datos de ejemplo
    
    Returns:
        Diccionario con pesos optimizados
    """
    logger.info("⚖️ Optimizando pesos con datos de ejemplo...")
    
    # Crear datos de ejemplo
    sample_data = create_sample_data()
    
    try:
        # Optimización con Grid Search
        logger.info("🔍 Aplicando optimización con Grid Search...")
        grid_results = weight_optimizer.optimize_weights_grid_search(
            sample_data, metric="f1"
        )
        
        # Optimización con algoritmo genético
        logger.info("🧬 Aplicando optimización con algoritmo genético...")
        genetic_results = weight_optimizer.optimize_weights_genetic(
            sample_data, population_size=30, generations=50, metric="f1"
        )
        
        # Comparar resultados
        print("\n" + "="*60)
        print("⚖️ COMPARACIÓN DE OPTIMIZACIÓN DE PESOS")
        print("="*60)
        
        print(f"\n🔍 Grid Search:")
        print(f"  Mejor Score: {grid_results['best_score']:.3f}")
        print(f"  Pesos: {grid_results['optimized_weights']}")
        
        print(f"\n🧬 Algoritmo Genético:")
        print(f"  Mejor Score: {genetic_results['best_score']:.3f}")
        print(f"  Pesos: {genetic_results['optimized_weights']}")
        
        # Usar el mejor resultado
        if grid_results['best_score'] >= genetic_results['best_score']:
            best_results = grid_results
            method = "Grid Search"
        else:
            best_results = genetic_results
            method = "Algoritmo Genético"
        
        print(f"\n🏆 Mejor método: {method}")
        print(f"  Score: {best_results['best_score']:.3f}")
        print(f"  Pesos optimizados: {best_results['optimized_weights']}")
        
        # Guardar pesos optimizados
        weights_file = "models/optimized_weights.json"
        weight_optimizer.save_optimized_weights(
            best_results['optimized_weights'], 
            weights_file
        )
        
        logger.info(f"💾 Pesos optimizados guardados en: {weights_file}")
        
        return best_results
        
    except Exception as e:
        logger.error(f"❌ Error durante la optimización de pesos: {e}")
        return None

def test_models():
    """
    Prueba los modelos entrenados con ejemplos
    
    Returns:
        True si las pruebas son exitosas
    """
    logger.info("🧪 Probando modelos entrenados...")
    
    # Textos de prueba
    test_texts = [
        "Eres un idiota",  # Debería ser tóxico
        "Hola, ¿cómo estás?",  # Debería ser no tóxico
        "Este video es tonto pero divertido",  # Caso límite
        "Odio a todas las personas",  # Debería ser tóxico
        "El clima está muy agradable",  # Debería ser no tóxico
    ]
    
    try:
        # Probar modelo ML si está disponible
        if hasattr(model_trainer, 'ml_classifier') and model_trainer.ml_classifier.is_trained:
            logger.info("🤖 Probando modelo ML...")
            
            for text in test_texts:
                is_toxic, prob, score = model_trainer.ml_classifier.predict_toxicity(text)
                print(f"📝 '{text}' -> Tóxico: {is_toxic}, Score: {score:.3f}, Prob: {prob:.3f}")
        
        # Probar clasificador híbrido si está disponible
        if hasattr(model_trainer, 'hybrid_classifier'):
            logger.info("🔀 Probando clasificador híbrido...")
            
            for text in test_texts:
                result = model_trainer.hybrid_classifier.analyze_text(text)
                print(f"📝 '{text}' -> {result}")
        
        logger.info("✅ Pruebas completadas exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante las pruebas: {e}")
        return False

def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(
        description="Entrenador de Modelos ML para ToxiGuard"
    )
    
    parser.add_argument(
        "--train", 
        action="store_true", 
        help="Entrenar modelos ML"
    )
    
    parser.add_argument(
        "--optimize-weights", 
        action="store_true", 
        help="Optimizar pesos de categorías"
    )
    
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Probar modelos entrenados"
    )
    
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Ejecutar todas las operaciones"
    )
    
    args = parser.parse_args()
    
    if not any([args.train, args.optimize_weights, args.test, args.all]):
        parser.print_help()
        return
    
    logger.info("🚀 Iniciando script de entrenamiento de modelos ML...")
    
    try:
        if args.all or args.train:
            logger.info("🎯 MODO: Entrenamiento de modelos")
            train_models_with_sample_data()
        
        if args.all or args.optimize_weights:
            logger.info("⚖️ MODO: Optimización de pesos")
            optimize_weights_with_sample_data()
        
        if args.all or args.test:
            logger.info("🧪 MODO: Pruebas de modelos")
            test_models()
        
        logger.info("🎉 Script completado exitosamente")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Script interrumpido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
