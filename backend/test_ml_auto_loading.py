#!/usr/bin/env python3
"""
🧪 Test de Carga Automática ML - ToxiGuard
Verifica que los modelos ML se carguen automáticamente
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(os.path.dirname(__file__)))

def test_auto_loading():
    """Test de carga automática de modelos ML"""
    print("🔍 Probando carga automática de modelos ML...")
    
    try:
        from app.ml_models import ml_classifier, hybrid_classifier
        
        print(f"✅ ML Classifier:")
        print(f"   - Tipo: {ml_classifier.model_type}")
        print(f"   - Entrenado: {ml_classifier.is_trained}")
        print(f"   - Modelo: {type(ml_classifier.model).__name__}")
        
        print(f"\n✅ Hybrid Classifier:")
        print(f"   - ML Entrenado: {hybrid_classifier.has_trained_ml_model()}")
        print(f"   - ML Modelo: {type(hybrid_classifier.ml_classifier.model).__name__}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ml_prediction():
    """Test de predicción ML después de la carga automática"""
    print("\n🔍 Probando predicción ML...")
    
    try:
        from app.ml_models import ml_classifier
        
        if ml_classifier.is_trained:
            print("🎯 Modelo ML está entrenado! Probando predicción...")
            
            # Test con diferentes textos
            test_texts = [
                "Hola mundo",
                "Eres un idiota estúpido",
                "La comida está deliciosa",
                "Te voy a matar"
            ]
            
            for text in test_texts:
                try:
                    is_toxic, prob, score = ml_classifier.predict_toxicity(text)
                    print(f"📝 '{text}' → Tóxico: {is_toxic}, Score: {score:.3f}")
                except Exception as e:
                    print(f"❌ Error prediciendo '{text}': {e}")
        else:
            print("⚠️ Modelo ML no está entrenado aún")
            
        return True
    except Exception as e:
        print(f"❌ Error en test ML: {e}")
        return False

def test_hybrid_prediction():
    """Test de predicción híbrida"""
    print("\n🔍 Probando predicción híbrida...")
    
    try:
        from app.ml_models import hybrid_classifier
        
        if hybrid_classifier.has_trained_ml_model():
            print("🎯 Clasificador híbrido con ML entrenado! Probando...")
            
            test_text = "Eres un idiota estúpido"
            result = hybrid_classifier.analyze_text(test_text)
            
            is_toxic, score, labels, text_length, word_count, category, toxicity_percentage = result
            
            print(f"📝 '{test_text}' → Resultado híbrido:")
            print(f"   - Tóxico: {is_toxic}")
            print(f"   - Score: {score:.3f}")
            print(f"   - Porcentaje: {toxicity_percentage}%")
            print(f"   - Categoría: {category}")
            print(f"   - Etiquetas: {labels}")
        else:
            print("⚠️ Clasificador híbrido sin ML entrenado")
            
        return True
    except Exception as e:
        print(f"❌ Error en test híbrido: {e}")
        return False

def test_full_integration():
    """Test de integración completa con services"""
    print("\n🔍 Probando integración completa...")
    
    try:
        from app.services import ToxicityClassifier
        classifier = ToxicityClassifier()
        
        print("✅ ToxicityClassifier creado. Probando análisis...")
        
        # Test con texto tóxico
        test_text = "Eres un idiota estúpido"
        result = classifier.analyze_text(test_text)
        
        is_toxic, score, labels, text_length, word_count, category, toxicity_percentage = result
        
        print(f"📝 '{test_text}' → Análisis completo:")
        print(f"   - Tóxico: {is_toxic}")
        print(f"   - Score: {score:.3f}")
        print(f"   - Porcentaje: {toxicity_percentage}%")
        print(f"   - Categoría: {category}")
        print(f"   - Etiquetas: {labels}")
        
        # Determinar qué clasificador se usó
        if "ml_enhanced" in labels:
            classifier_used = "ML Model"
        elif "hybrid_ml" in labels:
            classifier_used = "Hybrid ML"
        elif "improved" in labels:
            classifier_used = "Improved Classifier"
        else:
            classifier_used = "Legacy Classifier"
            
        print(f"   - 🤖 Clasificador usado: {classifier_used}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 Iniciando test de carga automática ML...\n")
    
    tests = [
        test_auto_loading,
        test_ml_prediction,
        test_hybrid_prediction,
        test_full_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Error ejecutando test: {e}")
    
    print(f"\n📊 Resultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 Todos los tests pasaron! La integración ML completa está funcionando.")
    else:
        print("⚠️ Algunos tests fallaron. Revisar errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
