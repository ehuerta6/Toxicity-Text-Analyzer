"""
🧪 Script de prueba para verificar las explicaciones - ToxiGuard
Prueba que las explicaciones se generen correctamente para cada categoría detectada
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.hybrid_classifier import hybrid_classifier
from app.ml_classifier import ml_classifier
from app.improved_classifier import optimized_classifier

def test_explanations():
    """Prueba que cada clasificador genere explicaciones correctas"""
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die",
        "You are an idiot and I hope you suffer",
        "This is a normal comment without toxicity"
    ]
    
    print("🧪 PRUEBA DE EXPLICACIONES - TOXIGUARD")
    print("=" * 60)
    
    # Probar clasificador híbrido
    print("\n🔬 CLASIFICADOR HÍBRIDO:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        result = hybrid_classifier.analyze_text(text)
        
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
        print(f"  • Categorías: {result['details']['detected_categories']}")
        
        if result['details'].get('explanations'):
            print("  • Explicaciones:")
            for category, explanation in result['details']['explanations'].items():
                print(f"    - {category}: {explanation}")
        else:
            print("  • Explicaciones: No disponibles")
    
    # Probar clasificador ML
    print("\n🤖 CLASIFICADOR ML:")
    print("-" * 30)
    
    if ml_classifier.is_loaded:
        for i, text in enumerate(test_texts, 1):
            print(f"\n📝 Texto {i}: {text}")
            result = ml_classifier.analyze_text(text)
            
            print(f"  • Tóxico: {result['is_toxic']}")
            print(f"  • Porcentaje: {result['toxicity_percentage']}%")
            print(f"  • Categorías: {result['details']['detected_categories']}")
            
            if result['details'].get('explanations'):
                print("  • Explicaciones:")
                for category, explanation in result['details']['explanations'].items():
                    print(f"    - {category}: {explanation}")
            else:
                print("  • Explicaciones: No disponibles")
    else:
        print("❌ Clasificador ML no disponible")
    
    # Probar clasificador basado en reglas
    print("\n📋 CLASIFICADOR BASADO EN REGLAS:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        result = optimized_classifier.analyze_text(text)
        
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
        print(f"  • Categorías: {result['details']['detected_categories']}")
        
        if result['details'].get('explanations'):
            print("  • Explicaciones:")
            for category, explanation in result['details']['explanations'].items():
                print(f"    - {category}: {explanation}")
        else:
            print("  • Explicaciones: No disponibles")

def test_explanation_format():
    """Prueba el formato de las explicaciones"""
    
    print("\n🔍 PRUEBA DE FORMATO DE EXPLICACIONES:")
    print("-" * 40)
    
    test_text = "You are stupid and ugly"
    result = hybrid_classifier.analyze_text(test_text)
    
    print(f"Texto: {test_text}")
    print(f"Resultado: {result['is_toxic']} - {result['toxicity_percentage']}%")
    
    explanations = result['details'].get('explanations', {})
    if explanations:
        print("Explicaciones generadas:")
        for category, explanation in explanations.items():
            print(f"  • {category}: {explanation}")
            
            # Verificar que la explicación tenga el formato correcto
            if "Detectó" in explanation or "Modelo ML detectó" in explanation:
                print(f"    ✅ Formato correcto")
            else:
                print(f"    ❌ Formato incorrecto")
    else:
        print("❌ No se generaron explicaciones")

if __name__ == "__main__":
    try:
        test_explanations()
        test_explanation_format()
        print("\n✅ Todas las pruebas de explicaciones completadas!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
