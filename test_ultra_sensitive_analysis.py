#!/usr/bin/env python3
"""
🧪 Prueba del Sistema Ultra-Sensible de Análisis de Toxicidad - ToxiGuard
Demuestra la capacidad del nuevo clasificador para detectar textos ofensivos con mayor precisión
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'app'))

from advanced_toxicity_classifier import advanced_toxicity_classifier

def test_ultra_sensitive_analysis():
    """Prueba el análisis ultra-sensible con diferentes tipos de textos"""
    
    print("🚨 PRUEBA DEL SISTEMA ULTRA-SENSIBLE DE TOXIGUARD")
    print("=" * 60)
    
    # Textos de prueba con diferentes niveles de toxicidad
    test_texts = [
        # Texto seguro
        "Hola, ¿cómo estás? Espero que tengas un buen día.",
        
        # Texto con insultos leves
        "Eres un poco tonto y aburrido, pero no te preocupes.",
        
        # Texto con insultos moderados
        "Eres un idiota y estupido, no sabes nada de la vida.",
        
        # Texto con insultos severos
        "Eres un pendejo cabron, hijo de puta, eres una basura.",
        
        # Texto con amenazas
        "Te voy a matar, te odio, quiero que mueras miserablemente.",
        
        # Texto con discriminación
        "Los negros son inferiores, las mujeres son débiles, odio a los gays.",
        
        # Texto largo con múltiples insultos
        "Eres un idiota completo, pendejo cabron, hijo de puta. No sabes nada de la vida y eres una basura humana. Te odio y quiero que mueras miserablemente. Eres un racista, xenofobo y homofobo. Eres la peor persona que he conocido.",
        
        # Texto con negaciones (debería ser menos tóxico)
        "No eres tonto, no eres idiota, no te odio, no quiero hacerte daño.",
        
        # Texto mixto (algunas palabras tóxicas, otras no)
        "Hola amigo, eres un poco lento pero no te preocupes. Eres inteligente en otras cosas."
    ]
    
    print("\n📊 RESULTADOS DEL ANÁLISIS ULTRA-SENSIBLE:")
    print("-" * 60)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n🔍 TEXTO {i}:")
        print(f"   '{text[:80]}{'...' if len(text) > 80 else ''}'")
        
        try:
            # Analizar el texto
            result = advanced_toxicity_classifier.analyze_text(text)
            
            # Mostrar resultados
            print(f"   📈 Toxicidad: {result['toxicity_percentage']:.1f}%")
            print(f"   🎯 Confianza: {result['confidence']:.1f}")
            print(f"   🏷️  Categoría: {result['toxicity_level']}")
            print(f"   🚨 Tóxico: {'SÍ' if result['is_toxic'] else 'NO'}")
            
            # Mostrar categorías detectadas
            if result['details']['detected_categories']:
                print(f"   📋 Categorías: {', '.join(result['details']['detected_categories'])}")
            
            # Mostrar breakdown de severidad si está disponible
            if 'severity_breakdown' in result['details'] and result['details']['severity_breakdown']:
                print(f"   🚨 Breakdown de Severidad:")
                for category, breakdown in result['details']['severity_breakdown'].items():
                    print(f"      - {category}: {breakdown['avg_severity']:.2f} ({breakdown['match_count']} coincidencias)")
            
            # Mostrar explicaciones
            if result['details']['explanations']:
                print(f"   💡 Explicaciones:")
                for category, explanation in result['details']['explanations'].items():
                    print(f"      - {category}: {explanation}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n✅ PRUEBA COMPLETADA")
    print("\n🎯 CARACTERÍSTICAS DEL SISTEMA ULTRA-SENSIBLE:")
    print("   • Umbrales ultra-sensibles para evitar valores triviales")
    print("   • Ponderación de severidad por palabra")
    print("   • Análisis de repetición y densidad tóxica")
    print("   • Detección de múltiples categorías simultáneamente")
    print("   • Explicaciones detalladas de cada detección")

if __name__ == "__main__":
    test_ultra_sensitive_analysis()
