"""
🧪 Script de prueba para verificar el dashboard compacto - ToxiGuard
Prueba que el nuevo diseño compacto funcione correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.hybrid_classifier import hybrid_classifier

def test_dashboard_compact():
    """Prueba que el dashboard compacto genere respuestas válidas"""
    
    test_texts = [
        "Hello, how are you today?",
        "You are stupid and ugly",
        "I hate you, you should die",
        "This is a normal comment without toxicity"
    ]
    
    print("🧪 PRUEBA DEL DASHBOARD COMPACTO - TOXIGUARD")
    print("=" * 60)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Texto {i}: {text}")
        result = hybrid_classifier.analyze_text(text)
        
        # Verificar que todos los campos necesarios estén presentes
        required_fields = [
            'is_toxic', 'toxicity_percentage', 'toxicity_level', 
            'confidence', 'classification_technique', 'details'
        ]
        
        print(f"  • Tóxico: {result['is_toxic']}")
        print(f"  • Porcentaje: {result['toxicity_percentage']}%")
        print(f"  • Categoría: {result['toxicity_level']}")
        print(f"  • Confianza: {result['confidence']}")
        print(f"  • Técnica: {result['classification_technique']}")
        
        # Verificar campos de details
        details = result.get('details', {})
        if details:
            print(f"  • Categorías detectadas: {details.get('detected_categories', [])}")
            print(f"  • Conteo de palabras: {details.get('word_count', 0)}")
            print(f"  • Explicaciones: {len(details.get('explanations', {}))} disponibles")
        else:
            print("  • Details: No disponibles")
        
        # Verificar que todos los campos requeridos estén presentes
        missing_fields = [field for field in required_fields if field not in result]
        if missing_fields:
            print(f"  ❌ Campos faltantes: {missing_fields}")
        else:
            print("  ✅ Todos los campos requeridos están presentes")
    
    print("\n✅ Prueba del dashboard compacto completada!")

def test_explanations_integration():
    """Prueba que las explicaciones estén integradas correctamente"""
    
    print("\n🔍 PRUEBA DE INTEGRACIÓN DE EXPLICACIONES:")
    print("-" * 40)
    
    test_text = "You are stupid and ugly"
    result = hybrid_classifier.analyze_text(test_text)
    
    print(f"Texto: {test_text}")
    print(f"Resultado: {result['is_toxic']} - {result['toxicity_percentage']}%")
    
    explanations = result.get('details', {}).get('explanations', {})
    if explanations:
        print("Explicaciones generadas:")
        for category, explanation in explanations.items():
            print(f"  • {category}: {explanation}")
    else:
        print("❌ No se generaron explicaciones")
    
    print("\n✅ Prueba de integración de explicaciones completada!")

if __name__ == "__main__":
    try:
        test_dashboard_compact()
        test_explanations_integration()
        print("\n🎉 Todas las pruebas del dashboard compacto completadas!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
