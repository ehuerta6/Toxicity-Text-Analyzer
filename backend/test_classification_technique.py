"""
🧪 Script de prueba para verificar la técnica de clasificación - ToxiGuard
Prueba que la técnica de clasificación se muestre correctamente en lugar del nombre técnico del modelo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.hybrid_classifier import hybrid_classifier
from app.ml_classifier import ml_classifier
from app.improved_classifier import optimized_classifier

def test_classification_techniques():
    """Prueba que cada clasificador muestre la técnica correcta"""
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die"
    ]
    
    print("🧪 PRUEBA DE TÉCNICAS DE CLASIFICACIÓN - TOXIGUARD")
    print("=" * 70)
    
    # Probar clasificador híbrido
    print("\n🔬 CLASIFICADOR HÍBRIDO:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTexto {i}: {text}")
        result = hybrid_classifier.analyze_text(text)
        print(f"  • Técnica: {result.get('classification_technique', 'N/A')}")
        print(f"  • Modelo usado: {result.get('model_used', 'N/A')}")
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
    
    # Probar clasificador ML
    print("\n🤖 CLASIFICADOR ML:")
    print("-" * 30)
    
    if ml_classifier.is_loaded:
        for i, text in enumerate(test_texts, 1):
            print(f"\nTexto {i}: {text}")
            result = ml_classifier.analyze_text(text)
            print(f"  • Técnica: {result.get('classification_technique', 'N/A')}")
            print(f"  • Modelo usado: {result.get('model_used', 'N/A')}")
            print(f"  • Tóxico: {result['is_toxic']}")
            print(f"  • Porcentaje: {result['toxicity_percentage']}%")
    else:
        print("❌ Clasificador ML no disponible")
    
    # Probar clasificador basado en reglas
    print("\n📋 CLASIFICADOR BASADO EN REGLAS:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTexto {i}: {text}")
        result = optimized_classifier.analyze_text(text)
        print(f"  • Técnica: {result.get('classification_technique', 'N/A')}")
        print(f"  • Modelo usado: {result.get('model_used', 'N/A')}")
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
    
    # Información del clasificador híbrido
    print("\n📊 INFORMACIÓN DEL CLASIFICADOR HÍBRIDO:")
    print("-" * 40)
    
    info = hybrid_classifier.get_classifier_info()
    print(f"Técnica actual: {info['current_technique']}")
    print(f"Clasificador ML disponible: {info['primary_classifier']['is_available']}")
    print(f"Técnica ML: {info['primary_classifier']['technique']}")
    print(f"Técnica de reglas: {info['fallback_classifier']['technique']}")

def test_technique_switching():
    """Prueba el cambio entre técnicas de clasificación"""
    
    print("\n🔄 PRUEBA DE CAMBIO DE TÉCNICAS:")
    print("-" * 40)
    
    # Cambiar a ML
    hybrid_classifier.set_primary_classifier(True)
    print("✅ Cambiado a ML como principal")
    
    result = hybrid_classifier.analyze_text("You are stupid")
    print(f"Técnica usada: {result.get('classification_technique', 'N/A')}")
    
    # Cambiar a reglas
    hybrid_classifier.set_primary_classifier(False)
    print("✅ Cambiado a reglas como principal")
    
    result = hybrid_classifier.analyze_text("You are stupid")
    print(f"Técnica usada: {result.get('classification_technique', 'N/A')}")
    
    # Volver a ML
    hybrid_classifier.set_primary_classifier(True)
    print("✅ Vuelto a ML como principal")

if __name__ == "__main__":
    try:
        test_classification_techniques()
        test_technique_switching()
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
