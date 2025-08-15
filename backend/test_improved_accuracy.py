"""
🧪 Script de Prueba para Precisión Mejorada - ToxiGuard
Prueba casos de ejemplo para validar las mejoras en detección de toxicidad
"""

import sys
import os
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.improved_classifier import improved_classifier
from app.advanced_preprocessor import advanced_preprocessor

def test_improved_accuracy():
    """Prueba la precisión mejorada con casos de ejemplo"""
    
    print("🧪 PRUEBAS DE PRECISIÓN MEJORADA - ToxiGuard")
    print("=" * 60)
    
    # Casos de prueba para validar mejoras
    test_cases = [
        # Casos de palabras aisladas (deberían tener toxicidad baja)
        {
            "text": "tonto",
            "expected": "baja toxicidad",
            "description": "Palabra aislada de insulto leve"
        },
        {
            "text": "feo",
            "expected": "baja toxicidad", 
            "description": "Palabra aislada de insulto leve"
        },
        {
            "text": "Eres tonto",
            "expected": "toxicidad moderada",
            "description": "Insulto directo pero simple"
        },
        
        # Casos con contexto que deberían reducir toxicidad
        {
            "text": "Este video es tonto pero divertido",
            "expected": "baja toxicidad",
            "description": "Contexto positivo reduce toxicidad"
        },
        {
            "text": "No eres tonto, eres inteligente",
            "expected": "baja toxicidad",
            "description": "Negación clara reduce toxicidad"
        },
        {
            "text": "Si fuera tonto, no estaría aquí",
            "expected": "toxicidad moderada",
            "description": "Contexto condicional"
        },
        
        # Casos de alta toxicidad que deberían mantenerse
        {
            "text": "Odio a todas las personas como tú",
            "expected": "alta toxicidad",
            "description": "Múltiples indicadores de odio"
        },
        {
            "text": "Eres un idiota estúpido y deberías morir",
            "expected": "alta toxicidad",
            "description": "Múltiples insultos severos + amenaza"
        },
        {
            "text": "Matar a todos los racistas",
            "expected": "alta toxicidad",
            "description": "Violencia + discriminación"
        },
        
        # Casos de contexto mixto
        {
            "text": "Aunque seas tonto, te quiero",
            "expected": "toxicidad moderada",
            "description": "Contexto positivo pero insulto presente"
        },
        {
            "text": "Eres un poco lento pero trabajador",
            "expected": "baja toxicidad",
            "description": "Suavizador + contexto positivo"
        },
        
        # Casos de spam y contenido comercial
        {
            "text": "Comprar ahora, oferta especial",
            "expected": "toxicidad baja-moderada",
            "description": "Spam comercial"
        },
        {
            "text": "Basura de producto, no compres",
            "expected": "toxicidad moderada",
            "description": "Crítica negativa pero no tóxica"
        }
    ]
    
    print(f"📊 Probando {len(test_cases)} casos de ejemplo...\n")
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Caso {i}: {test_case['description']}")
        print(f"   Texto: '{test_case['text']}'")
        print(f"   Esperado: {test_case['expected']}")
        
        try:
            # Análisis con clasificador mejorado
            is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = improved_classifier.analyze_text(test_case['text'])
            
            # Análisis detallado
            detailed_analysis = improved_classifier.get_detailed_analysis(test_case['text'])
            
            print(f"   Resultado: {'🚨 TÓXICO' if is_toxic else '✅ SEGURO'}")
            print(f"   Score: {score:.3f}")
            print(f"   Porcentaje: {toxicity_percentage}%")
            print(f"   Categoría: {category or 'N/A'}")
            print(f"   Palabras encontradas: {keywords_found}")
            print(f"   Score contextual: {detailed_analysis.get('context_score', 0):.3f}")
            print(f"   Umbral adaptativo: {detailed_analysis.get('adaptive_threshold', 0):.3f}")
            
            # Evaluar si el resultado es razonable
            if toxicity_percentage < 30:
                result_quality = "✅ EXCELENTE" if not is_toxic else "❌ FALSO POSITIVO"
            elif toxicity_percentage < 60:
                result_quality = "⚠️ ACEPTABLE"
            else:
                result_quality = "✅ EXCELENTE" if is_toxic else "❌ FALSO NEGATIVO"
            
            print(f"   Calidad: {result_quality}")
            
            results.append({
                "case": i,
                "text": test_case['text'],
                "expected": test_case['expected'],
                "is_toxic": is_toxic,
                "score": score,
                "toxicity_percentage": toxicity_percentage,
                "category": category,
                "quality": result_quality
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "case": i,
                "text": test_case['text'],
                "error": str(e)
            })
        
        print("-" * 50)
    
    # Resumen de resultados
    print("\n📈 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    successful_tests = [r for r in results if 'error' not in r]
    error_tests = [r for r in results if 'error' in r]
    
    print(f"✅ Pruebas exitosas: {len(successful_tests)}/{len(test_cases)}")
    if error_tests:
        print(f"❌ Pruebas con error: {len(error_tests)}")
    
    # Análisis de calidad
    if successful_tests:
        excellent_results = [r for r in successful_tests if "EXCELENTE" in r['quality']]
        acceptable_results = [r for r in successful_tests if "ACEPTABLE" in r['quality']]
        poor_results = [r for r in successful_tests if "FALSO" in r['quality']]
        
        print(f"\n🎯 Calidad de resultados:")
        print(f"   Excelentes: {len(excellent_results)} ({len(excellent_results)/len(successful_tests)*100:.1f}%)")
        print(f"   Aceptables: {len(acceptable_results)} ({len(acceptable_results)/len(successful_tests)*100:.1f}%)")
        print(f"   Pobres: {len(poor_results)} ({len(poor_results)/len(successful_tests)*100:.1f}%)")
        
        # Mostrar casos problemáticos
        if poor_results:
            print(f"\n⚠️ Casos que necesitan atención:")
            for result in poor_results:
                print(f"   - Caso {result['case']}: '{result['text'][:50]}...' -> {result['quality']}")
    
    print("\n🎉 Pruebas completadas!")

def test_preprocessor():
    """Prueba el preprocesador avanzado"""
    print("\n🧠 PRUEBAS DEL PREPROCESADOR AVANZADO")
    print("=" * 60)
    
    test_texts = [
        "Eres tonto pero divertido",
        "No eres tonto, eres inteligente",
        "Si fuera tonto, no estaría aquí",
        "Odio a todas las personas como tú",
        "Este video es tonto pero divertido"
    ]
    
    for text in test_texts:
        print(f"\n📝 Texto: '{text}'")
        
        try:
            preprocessed = advanced_preprocessor.preprocess_text(text)
            context_score = advanced_preprocessor.get_context_score(preprocessed)
            
            print(f"   Palabras: {preprocessed['word_count']}")
            print(f"   Oraciones: {preprocessed['sentence_count']}")
            print(f"   Score contextual: {context_score:.3f}")
            print(f"   Negaciones: {preprocessed['context_analysis']['negation_count']}")
            print(f"   Intensificadores: {preprocessed['context_analysis']['intensifier_count']}")
            print(f"   Suavizadores: {preprocessed['context_analysis']['softener_count']}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    try:
        test_improved_accuracy()
        test_preprocessor()
    except KeyboardInterrupt:
        print("\n\n⏹️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()
