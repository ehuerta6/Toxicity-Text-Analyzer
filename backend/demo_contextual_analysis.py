#!/usr/bin/env python3
"""
🎯 Demostración del Análisis Contextual - ToxiGuard
Muestra las mejoras implementadas en el análisis de toxicidad
"""

from app.contextual_classifier import contextual_classifier
import time

def demo_contextual_analysis():
    """Demuestra el análisis contextual con ejemplos específicos"""
    
    print("🎯 ToxiGuard - Demostración del Análisis Contextual")
    print("=" * 70)
    print("✅ Mejoras implementadas:")
    print("   • Análisis contextual con embeddings")
    print("   • Detección de negaciones y contexto")
    print("   • Análisis por oraciones")
    print("   • Similitud semántica")
    print("   • Modelo ligero: all-MiniLM-L6-v2")
    print("=" * 70)
    
    # Casos de demostración
    demo_cases = [
        {
            "title": "🔴 Insulto Directo",
            "text": "Eres un idiota completo",
            "expected": "Alta toxicidad (insulto directo)"
        },
        {
            "title": "🟢 Insulto Negado (Contexto Positivo)",
            "text": "No eres tonto, eres muy inteligente",
            "expected": "Baja toxicidad (negación + contexto positivo)"
        },
        {
            "title": "🔴 Acoso Directo",
            "text": "Te voy a matar si no haces lo que digo",
            "expected": "Alta toxicidad (amenaza directa)"
        },
        {
            "title": "🟢 Acoso Negado",
            "text": "No te voy a hacer daño, solo quiero ayudarte",
            "expected": "Baja toxicidad (negación de violencia)"
        },
        {
            "title": "🔴 Discriminación Directa",
            "text": "Los negros son inferiores a los blancos",
            "expected": "Alta toxicidad (discriminación)"
        },
        {
            "title": "🟢 Discriminación Negada",
            "text": "Todos somos iguales, no discrimino a nadie",
            "expected": "Baja toxicidad (mensaje positivo)"
        },
        {
            "title": "🟡 Texto Neutral",
            "text": "El clima está muy agradable hoy",
            "expected": "Baja toxicidad (texto neutral)"
        },
        {
            "title": "🟡 Texto Mixto",
            "text": "Eres un idiota, pero no te voy a hacer daño",
            "expected": "Toxicidad moderada (insulto + negación)"
        }
    ]
    
    results = []
    
    for i, case in enumerate(demo_cases, 1):
        print(f"\n📝 {i}. {case['title']}")
        print(f"Texto: '{case['text']}'")
        print(f"Esperado: {case['expected']}")
        
        start_time = time.time()
        result = contextual_classifier.analyze_text(case['text'])
        analysis_time = (time.time() - start_time) * 1000
        
        toxicity = result['toxicity_percentage']
        category = result['toxicity_level']
        technique = result['classification_technique']
        
        # Determinar si el resultado es correcto
        if "baja" in case['expected'].lower() and toxicity <= 30:
            status = "✅ CORRECTO"
        elif "alta" in case['expected'].lower() and toxicity >= 60:
            status = "✅ CORRECTO"
        elif "moderada" in case['expected'].lower() and 30 < toxicity < 60:
            status = "✅ CORRECTO"
        else:
            status = "⚠️ INESPERADO"
        
        print(f"Resultado: {toxicity:.1f}% tóxico ({category})")
        print(f"Técnica: {technique}")
        print(f"Tiempo: {analysis_time:.1f}ms")
        print(f"Estado: {status}")
        
        # Mostrar explicaciones si están disponibles
        if result.get('details', {}).get('explanations'):
            print("Explicaciones:")
            for cat, explanation in result['details']['explanations'].items():
                print(f"  • {cat}: {explanation}")
        
        results.append({
            "case": case['title'],
            "toxicity": toxicity,
            "expected": case['expected'],
            "status": status
        })
        
        print("-" * 50)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE LA DEMOSTRACIÓN")
    print("=" * 70)
    
    correct_results = [r for r in results if "CORRECTO" in r['status']]
    unexpected_results = [r for r in results if "INESPERADO" in r['status']]
    
    print(f"✅ Resultados correctos: {len(correct_results)}/{len(results)}")
    print(f"⚠️ Resultados inesperados: {len(unexpected_results)}/{len(results)}")
    
    if correct_results:
        avg_toxicity = sum(r['toxicity'] for r in correct_results) / len(correct_results)
        print(f"📈 Toxicidad promedio: {avg_toxicity:.1f}%")
    
    print("\n🎯 Beneficios del Análisis Contextual:")
    print("   • Detecta negaciones y contexto positivo")
    print("   • Evita falsos positivos en frases como 'no eres tonto'")
    print("   • Análisis semántico en lugar de solo palabras clave")
    print("   • Mayor precisión en la clasificación de toxicidad")
    print("   • Explicaciones detalladas del análisis")
    
    print("\n" + "=" * 70)
    print("🎉 ¡Análisis contextual implementado exitosamente!")
    print("=" * 70)

if __name__ == "__main__":
    demo_contextual_analysis()
