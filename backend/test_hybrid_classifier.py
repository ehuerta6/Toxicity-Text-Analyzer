"""
🧪 Script de prueba para el clasificador híbrido - ToxiGuard
Prueba la funcionalidad del clasificador híbrido y compara resultados
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.hybrid_classifier import hybrid_classifier
from app.ml_classifier import ml_classifier
from app.improved_classifier import optimized_classifier

def test_classifiers():
    """Prueba todos los clasificadores con textos de ejemplo"""
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die",
        "This is a normal comment",
        "You are an idiot and I hope you suffer"
    ]
    
    print("🧪 PRUEBA DE CLASIFICADORES - TOXIGUARD")
    print("=" * 60)
    
    # Probar clasificador híbrido
    print("\n🔬 CLASIFICADOR HÍBRIDO:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTexto {i}: {text}")
        result = hybrid_classifier.analyze_text(text)
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
        print(f"  • Nivel: {result['toxicity_level']}")
        print(f"  • Confianza: {result['confidence']}")
        print(f"  • Modelo: {result['model_used']}")
    
    # Probar clasificador ML
    print("\n🤖 CLASIFICADOR ML (Linear SVM):")
    print("-" * 30)
    
    if ml_classifier.is_loaded:
        for i, text in enumerate(test_texts, 1):
            print(f"\nTexto {i}: {text}")
            result = ml_classifier.analyze_text(text)
            print(f"  • Tóxico: {result['is_toxic']}")
            print(f"  • Porcentaje: {result['toxicity_percentage']}%")
            print(f"  • Nivel: {result['toxicity_level']}")
            print(f"  • Confianza: {result['confidence']}")
            print(f"  • Modelo: {result['model_used']}")
    else:
        print("❌ Clasificador ML no disponible")
    
    # Probar clasificador basado en reglas
    print("\n📋 CLASIFICADOR BASADO EN REGLAS:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTexto {i}: {text}")
        result = optimized_classifier.analyze_text(text)
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
        print(f"  • Nivel: {result['toxicity_level']}")
        print(f"  • Confianza: {result['confidence']}")
        print(f"  • Modelo: {result['model_used']}")
    
    # Información del clasificador híbrido
    print("\n📊 INFORMACIÓN DEL CLASIFICADOR HÍBRIDO:")
    print("-" * 40)
    
    info = hybrid_classifier.get_classifier_info()
    print(f"Modo híbrido: {info['hybrid_mode']}")
    print(f"Clasificador ML disponible: {info['primary_classifier']['is_available']}")
    print(f"Clasificador de reglas disponible: {info['fallback_classifier']['is_available']}")
    
    if info['primary_classifier']['is_available']:
        performance = info['primary_classifier']['performance']
        print(f"Rendimiento ML:")
        print(f"  • F1-Score: {performance.get('f1_score', 'N/A')}")
        print(f"  • Precisión: {performance.get('precision', 'N/A')}")
        print(f"  • Recall: {performance.get('recall', 'N/A')}")
        print(f"  • Accuracy: {performance.get('accuracy', 'N/A')}")

def test_classifier_switching():
    """Prueba el cambio entre clasificadores"""
    
    print("\n🔄 PRUEBA DE CAMBIO DE CLASIFICADORES:")
    print("-" * 40)
    
    # Cambiar a ML
    hybrid_classifier.set_primary_classifier(True)
    print("✅ Cambiado a ML como principal")
    
    # Cambiar a reglas
    hybrid_classifier.set_primary_classifier(False)
    print("✅ Cambiado a reglas como principal")
    
    # Volver a ML
    hybrid_classifier.set_primary_classifier(True)
    print("✅ Vuelto a ML como principal")

if __name__ == "__main__":
    try:
        test_classifiers()
        test_classifier_switching()
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
