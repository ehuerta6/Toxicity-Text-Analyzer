"""
🧪 Script de prueba para verificar explicaciones siempre activas - ToxiGuard
Prueba que las explicaciones se generen siempre y sean claras y completas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.hybrid_classifier import hybrid_classifier
from app.ml_classifier import ml_classifier
from app.improved_classifier import optimized_classifier

def test_explanations_always_present():
    """Prueba que las explicaciones siempre estén presentes y sean claras"""
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die",
        "You are an idiot and I hope you suffer",
        "This is a normal comment without toxicity",
        "Bad word",
        "Terrible",
        "Awful comment here"
    ]
    
    print("🧪 PRUEBA DE EXPLICACIONES SIEMPRE ACTIVAS - TOXIGUARD")
    print("=" * 70)
    
    # Probar clasificador híbrido
    print("\n🔬 CLASIFICADOR HÍBRIDO:")
    print("-" * 30)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        result = hybrid_classifier.analyze_text(text)
        
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
        print(f"  • Categorías: {result['details']['detected_categories']}")
        
        explanations = result['details'].get('explanations', {})
        if explanations:
            print("  • Explicaciones:")
            for category, explanation in explanations.items():
                word_count = len(explanation.split())
                print(f"    - {category}: {explanation}")
                print(f"      Palabras: {word_count} {'✅' if word_count >= 4 else '⚠️'}")
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
            
            explanations = result['details'].get('explanations', {})
            if explanations:
                print("  • Explicaciones:")
                for category, explanation in explanations.items():
                    word_count = len(explanation.split())
                    print(f"    - {category}: {explanation}")
                    print(f"      Palabras: {word_count} {'✅' if word_count >= 4 else '⚠️'}")
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
        
        explanations = result['details'].get('explanations', {})
        if explanations:
            print("  • Explicaciones:")
            for category, explanation in explanations.items():
                word_count = len(explanation.split())
                print(f"    - {category}: {explanation}")
                print(f"      Palabras: {word_count} {'✅' if word_count >= 4 else '⚠️'}")
        else:
            print("  • Explicaciones: No disponibles")

def test_explanation_quality():
    """Prueba la calidad de las explicaciones generadas"""
    
    print("\n🔍 PRUEBA DE CALIDAD DE EXPLICACIONES:")
    print("-" * 40)
    
    test_text = "You are stupid and ugly"
    result = hybrid_classifier.analyze_text(test_text)
    
    print(f"Texto: {test_text}")
    print(f"Resultado: {result['is_toxic']} - {result['toxicity_percentage']}%")
    
    explanations = result['details'].get('explanations', {})
    if explanations:
        print("Explicaciones generadas:")
        for category, explanation in explanations.items():
            word_count = len(explanation.split())
            clarity = "✅ Clara" if word_count >= 4 else "⚠️ Muy corta"
            context = "✅ Con contexto" if any(word in explanation.lower() for word in ["contexto", "análisis", "texto"]) else "⚠️ Sin contexto"
            
            print(f"  • {category}: {explanation}")
            print(f"    - Palabras: {word_count} - {clarity}")
            print(f"    - Contexto: {context}")
    else:
        print("❌ No se generaron explicaciones")

if __name__ == "__main__":
    try:
        test_explanations_always_present()
        test_explanation_quality()
        print("\n✅ Todas las pruebas de explicaciones siempre activas completadas!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
