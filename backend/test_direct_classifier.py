#!/usr/bin/env python3
"""
🧪 Prueba Directa del Clasificador Mejorado - ToxiGuard
Prueba directamente el clasificador mejorado para verificar su funcionamiento
"""

import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.improved_classifier import improved_classifier

def test_direct_classifier():
    """Prueba directamente el clasificador mejorado"""
    
    print("🧪 PRUEBA DIRECTA DEL CLASIFICADOR MEJORADO")
    print("=" * 60)
    
    test_cases = [
        "tonto",
        "Este video es tonto pero divertido",
        "No eres tonto, eres inteligente",
        "Odio a todas las personas como tú"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n🔍 Caso {i}: '{text}'")
        
        try:
            # Análisis directo con clasificador mejorado
            is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = improved_classifier.analyze_text(text)
            
            print(f"   Resultado: {'🚨 TÓXICO' if is_toxic else '✅ SEGURO'}")
            print(f"   Score: {score:.3f}")
            print(f"   Porcentaje: {toxicity_percentage}%")
            print(f"   Categoría: {category or 'N/A'}")
            print(f"   Palabras encontradas: {keywords_found}")
            
            # Análisis detallado
            detailed = improved_classifier.get_detailed_analysis(text)
            print(f"   Score contextual: {detailed.get('context_score', 0):.3f}")
            print(f"   Umbral adaptativo: {detailed.get('adaptive_threshold', 0):.3f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎉 Prueba directa completada!")

if __name__ == "__main__":
    test_direct_classifier()
