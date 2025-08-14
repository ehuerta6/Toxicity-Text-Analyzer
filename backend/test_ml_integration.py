#!/usr/bin/env python3
"""
Script para probar la integración del modelo ML en el backend
"""

import sys
from pathlib import Path
import joblib

# Agregar el directorio padre al path
sys.path.append(str(Path(__file__).parent.parent))

def test_model_loading():
    """Prueba la carga del modelo ML"""
    print("🧪 PROBANDO CARGA DEL MODELO ML")
    print("=" * 50)
    
    try:
        # Verificar que los archivos existan
        models_dir = Path(__file__).parent.parent / "models"
        model_path = models_dir / "toxic_model.pkl"
        vectorizer_path = models_dir / "vectorizer.pkl"
        
        print(f"📁 Directorio de modelos: {models_dir}")
        print(f"   Modelo: {model_path} - {'✅ Existe' if model_path.exists() else '❌ No existe'}")
        print(f"   Vectorizador: {vectorizer_path} - {'✅ Existe' if vectorizer_path.exists() else '❌ No existe'}")
        
        if not model_path.exists() or not vectorizer_path.exists():
            print("❌ Archivos del modelo no encontrados")
            return False
        
        # Cargar modelo
        print("\n📥 Cargando modelo...")
        model = joblib.load(model_path)
        print(f"   ✅ Modelo cargado: {type(model).__name__}")
        
        # Cargar vectorizador
        print("📥 Cargando vectorizador...")
        vectorizer = joblib.load(vectorizer_path)
        print(f"   ✅ Vectorizador cargado: {type(vectorizer).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return False

def test_preprocessing():
    """Prueba el preprocesamiento de texto"""
    print("\n🔧 PROBANDO PREPROCESAMIENTO")
    print("=" * 50)
    
    try:
        from ml.preprocess import preprocess_text
        
        test_texts = [
            "Hello world! This is a nice comment.",
            "You are an idiot and I hate you!",
            "This is a neutral comment about the weather.",
            "Go to hell you stupid person!"
        ]
        
        for i, text in enumerate(test_texts, 1):
            processed = preprocess_text(text)
            print(f"   {i}. Original: {text[:50]}{'...' if len(text) > 50 else ''}")
            print(f"      Procesado: {processed[:50]}{'...' if len(processed) > 50 else ''}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en preprocesamiento: {e}")
        return False

def test_prediction():
    """Prueba la predicción con el modelo"""
    print("\n🤖 PROBANDO PREDICCIÓN")
    print("=" * 50)
    
    try:
        # Cargar modelo
        models_dir = Path(__file__).parent.parent / "models"
        model = joblib.load(models_dir / "toxic_model.pkl")
        
        # Importar preprocesamiento
        from ml.preprocess import preprocess_text
        
        test_texts = [
            "Hello world! This is a nice comment.",
            "You are an idiot and I hate you!",
            "This is a neutral comment about the weather.",
            "Go to hell you stupid person!"
        ]
        
        for i, text in enumerate(test_texts, 1):
            # Preprocesar
            processed = preprocess_text(text)
            
            # Predecir
            prediction = model.predict([processed])[0]
            probability = model.predict_proba([processed])[0]
            
            print(f"   {i}. Texto: {text[:50]}{'...' if len(text) > 50 else ''}")
            print(f"      Procesado: {processed[:50]}{'...' if len(processed) > 50 else ''}")
            print(f"      Predicción: {'Tóxico' if prediction else 'No Tóxico'}")
            print(f"      Probabilidad: {float(probability[int(prediction)]):.3f}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en predicción: {e}")
        return False

def test_backend_integration():
    """Prueba la integración con el backend"""
    print("\n🔗 PROBANDO INTEGRACIÓN CON BACKEND")
    print("=" * 50)
    
    try:
        # Importar módulo del backend
        from app.main import load_ml_model, ml_model, ml_vectorizer, model_loaded
        
        print("📥 Cargando modelo desde backend...")
        success = load_ml_model()
        
        if success:
            print(f"   ✅ Modelo cargado: {ml_model is not None}")
            print(f"   ✅ Vectorizador cargado: {ml_vectorizer is not None}")
            print(f"   ✅ Estado: {model_loaded}")
            
            # Probar predicción
            if ml_model is not None:
                from ml.preprocess import preprocess_text
                
                test_text = "You are an idiot!"
                processed = preprocess_text(test_text)
                prediction = ml_model.predict([processed])[0]
                probability = ml_model.predict_proba([processed])[0]
                
                print(f"\n   🧪 Prueba de predicción:")
                print(f"      Texto: {test_text}")
                print(f"      Predicción: {'Tóxico' if prediction else 'No Tóxico'}")
                print(f"      Probabilidad: {float(probability[int(prediction)]):.3f}")
            
            return True
        else:
            print("   ❌ Error cargando modelo desde backend")
            return False
            
    except Exception as e:
        print(f"❌ Error en integración con backend: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 PRUEBA DE INTEGRACIÓN DEL MODELO ML - ToxiGuard")
    print("=" * 70)
    
    tests = [
        ("Carga del Modelo", test_model_loading),
        ("Preprocesamiento", test_preprocessing),
        ("Predicción", test_prediction),
        ("Integración Backend", test_backend_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen de resultados
    print(f"\n{'='*70}")
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El modelo ML está integrado correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
