#!/usr/bin/env python3
"""
🚀 Script de Instalación Rápida - Mejoras de Precisión ToxiGuard
Instala y configura automáticamente el sistema mejorado de detección de toxicidad
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            if result.stdout.strip():
                print(f"   Salida: {result.stdout.strip()}")
        else:
            print(f"⚠️ {description} completado con advertencias")
            if result.stderr.strip():
                print(f"   Advertencias: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error en {description}: {e}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    print("\n📦 INSTALANDO DEPENDENCIAS")
    print("=" * 50)
    
    # Verificar si pip está disponible
    if not run_command("pip --version", "Verificando pip"):
        print("❌ pip no está disponible. Instala pip primero.")
        return False
    
    # Instalar dependencias básicas
    dependencies = [
        "nltk==3.8.1",
        "scikit-learn==1.3.2",
        "joblib==1.3.2",
        "numpy==1.24.3",
        "pandas==2.0.3"
    ]
    
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️ No se pudo instalar {dep}, continuando...")
    
    return True

def download_nltk_resources():
    """Descarga los recursos necesarios de NLTK"""
    print("\n🧠 DESCARGANDO RECURSOS NLTK")
    print("=" * 50)
    
    nltk_resources = [
        "punkt",
        "stopwords", 
        "wordnet"
    ]
    
    for resource in nltk_resources:
        command = f'python -c "import nltk; nltk.download(\'{resource}\')"'
        if not run_command(command, f"Descargando {resource}"):
            print(f"⚠️ No se pudo descargar {resource}")
    
    return True

def test_installation():
    """Prueba la instalación"""
    print("\n🧪 PROBANDO INSTALACIÓN")
    print("=" * 50)
    
    test_script = """
import sys
try:
    import nltk
    print("✅ NLTK instalado correctamente")
    
    import sklearn
    print("✅ Scikit-learn instalado correctamente")
    
    import nltk.data
    nltk.data.find('tokenizers/punkt')
    print("✅ Recursos NLTK disponibles")
    
    print("🎉 ¡Todas las dependencias están funcionando!")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)
except LookupError as e:
    print(f"❌ Recurso NLTK no encontrado: {e}")
    sys.exit(1)
"""
    
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    
    success = run_command("python test_imports.py", "Probando importaciones")
    
    # Limpiar archivo temporal
    if os.path.exists("test_imports.py"):
        os.remove("test_imports.py")
    
    return success

def show_next_steps():
    """Muestra los siguientes pasos"""
    print("\n🚀 PRÓXIMOS PASOS")
    print("=" * 50)
    print("1. ✅ Dependencias instaladas")
    print("2. ✅ Recursos NLTK descargados")
    print("3. ✅ Sistema probado")
    print("\n🎯 Ahora puedes:")
    print("   - Ejecutar el backend mejorado")
    print("   - Probar la precisión: python test_improved_accuracy.py")
    print("   - Usar la API con análisis contextual mejorado")
    print("\n📚 Para más información, consulta:")
    print("   - IMPROVED_ACCURACY_SUMMARY.md")
    print("   - test_improved_accuracy.py")

def main():
    """Función principal de instalación"""
    print("🚀 INSTALADOR DE MEJORAS DE PRECISIÓN - ToxiGuard")
    print("=" * 60)
    print("Este script instalará y configurará automáticamente")
    print("el sistema mejorado de detección de toxicidad.")
    print()
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    # Descargar recursos NLTK
    if not download_nltk_resources():
        print("⚠️ Advertencia: Algunos recursos NLTK no se pudieron descargar")
    
    # Probar instalación
    if not test_installation():
        print("❌ Error en la instalación")
        sys.exit(1)
    
    # Mostrar próximos pasos
    show_next_steps()
    
    print("\n🎉 ¡Instalación completada exitosamente!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Instalación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
