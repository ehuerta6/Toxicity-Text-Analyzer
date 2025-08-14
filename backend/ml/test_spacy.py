#!/usr/bin/env python3
"""
Script de prueba para verificar la instalación de spaCy
"""

import spacy
import sys

def test_spacy_installation():
    """Prueba que spaCy esté instalado y funcionando"""
    print("🧪 Probando instalación de spaCy...")
    
    try:
        # Cargar el modelo en inglés
        print("   📥 Cargando modelo en_core_web_sm...")
        nlp = spacy.load("en_core_web_sm")
        print("   ✅ Modelo cargado exitosamente")
        
        # Probar procesamiento de texto
        print("   🔍 Probando procesamiento de texto...")
        text = "Hello world! This is a test sentence for spaCy."
        doc = nlp(text)
        
        print(f"   📝 Texto procesado: {text}")
        print(f"   🔤 Tokens: {[token.text for token in doc]}")
        print(f"   🏷️  POS tags: {[(token.text, token.pos_) for token in doc]}")
        print(f"   🧠 Entidades: {[(ent.text, ent.label_) for ent in doc.ents]}")
        
        # Probar lematización
        print("   📚 Probando lematización...")
        lemmas = [token.lemma_ for token in doc]
        print(f"   📖 Lemas: {lemmas}")
        
        # Probar stop words
        print("   🛑 Probando stop words...")
        stop_words = [token.text for token in doc if token.is_stop]
        print(f"   🚫 Stop words: {stop_words}")
        
        print("   ✅ spaCy funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_ml_dependencies():
    """Prueba que las dependencias de ML estén instaladas"""
    print("\n🔧 Probando dependencias de ML...")
    
    dependencies = {
        'scikit-learn': 'sklearn',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'spacy': 'spacy'
    }
    
    all_ok = True
    
    for package_name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"   ✅ {package_name} instalado")
        except ImportError:
            print(f"   ❌ {package_name} no encontrado")
            all_ok = False
    
    return all_ok

def main():
    """Función principal de pruebas"""
    print("🚀 VERIFICACIÓN DE ENTORNO ML - ToxiGuard")
    print("=" * 50)
    
    # Probar spaCy
    spacy_ok = test_spacy_installation()
    
    # Probar dependencias
    deps_ok = test_ml_dependencies()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    print(f"spaCy funcionando: {'✅' if spacy_ok else '❌'}")
    print(f"Dependencias ML: {'✅' if deps_ok else '❌'}")
    
    if spacy_ok and deps_ok:
        print("\n🎉 ¡Entorno ML configurado correctamente!")
        print("   Listo para implementar modelos avanzados")
    else:
        print("\n⚠️  Algunos componentes requieren atención")
        print("   Revisa los errores arriba")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
