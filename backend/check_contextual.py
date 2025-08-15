#!/usr/bin/env python3
"""
🔍 Verificación del Clasificador Contextual
"""

from app.contextual_classifier import contextual_classifier

print("🔍 Verificación del Clasificador Contextual")
print("=" * 50)

print(f"Modelo de embeddings: {contextual_classifier.embedding_model}")
print(f"Nombre del modelo: {contextual_classifier.model_name}")
print(f"Técnica de clasificación: {contextual_classifier.classification_technique}")

# Probar análisis simple
test_text = "No eres tonto, eres muy inteligente"
print(f"\n📝 Probando texto: '{test_text}'")

try:
    result = contextual_classifier.analyze_text(test_text)
    print(f"✅ Análisis exitoso:")
    print(f"   - Toxicidad: {result['toxicity_percentage']}%")
    print(f"   - Categoría: {result['toxicity_level']}")
    print(f"   - Técnica: {result['classification_technique']}")
    print(f"   - Modelo usado: {result['model_used']}")
    
    if result.get('details', {}).get('explanations'):
        print(f"   - Explicaciones: {result['details']['explanations']}")
    
except Exception as e:
    print(f"❌ Error en análisis: {e}")

print("\n" + "=" * 50)
