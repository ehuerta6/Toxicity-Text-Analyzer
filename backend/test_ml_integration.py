#!/usr/bin/env python3
"""
🧪 Test de Integración ML - ToxiGuard
Verifica que los modelos ML se integren correctamente
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, str(os.path.dirname(__file__)))

def test_ml_imports():
    """Test de imports de módulos ML"""
    print("🔍 Probando imports de módulos ML...")
    
    try:
        from app.ml_models import ml_classifier, hybrid_classifier
        print("✅ ML models importados correctamente")
        print(f"   - ml_classifier.is_trained: {ml_classifier.is_trained}")
        print(f"   - hybrid_classifier ML trained: {hybrid_classifier.ml_classifier.is_trained}")
    except Exception as e:
        print(f"❌ Error importando ML models: {e}")
        return False
    
    return True

def test_services_integration():
    """Test de integración con services"""
    print("\n🔍 Probando integración con services...")
    
    try:
        from app.services import ToxicityClassifier
        classifier = ToxicityClassifier()
        print("✅ ToxicityClassifier creado correctamente")
        
        # Test de análisis simple
        result = classifier.analyze_text("Hola mundo")
        print(f"✅ Análisis de texto exitoso: {result}")
        
    except Exception as e:
        print(f"❌ Error en services: {e}")
        return False
    
    return True

def test_main_module():
    """Test del módulo principal"""
    print("\n🔍 Probando módulo principal...")
    
    try:
        import app.main
        print("✅ Módulo principal importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en módulo principal: {e}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 Iniciando test de integración ML...\n")
    
    tests = [
        test_ml_imports,
        test_services_integration,
        test_main_module
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
        print("🎉 Todos los tests pasaron! La integración ML está funcionando.")
    else:
        print("⚠️ Algunos tests fallaron. Revisar errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
