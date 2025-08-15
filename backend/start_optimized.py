#!/usr/bin/env python3
"""
🚀 Script de inicio optimizado para ToxiGuard Backend
Inicia el servidor con configuraciones optimizadas para desarrollo y producción
"""

import os
import sys
import argparse
import uvicorn
from pathlib import Path

def setup_environment(env_type: str = "development"):
    """Configura el entorno según el tipo especificado"""
    
    if env_type == "development":
        # Configuración para desarrollo
        env_file = Path(__file__).parent / ".env.development"
        if env_file.exists():
            # Copiar configuración de desarrollo
            import shutil
            shutil.copy2(env_file, Path(__file__).parent / ".env")
            print("✅ Configuración de desarrollo aplicada")
        
        # Variables de entorno para desarrollo
        os.environ.setdefault("DEBUG", "true")
        os.environ.setdefault("RELOAD", "true")
        os.environ.setdefault("LOG_LEVEL", "INFO")
        
    elif env_type == "production":
        # Configuración para producción
        os.environ.setdefault("DEBUG", "false")
        os.environ.setdefault("RELOAD", "false")
        os.environ.setdefault("LOG_LEVEL", "WARNING")
        
    print(f"🌍 Entorno configurado: {env_type}")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "joblib",
        "pandas",
        "numpy",
        "scikit-learn"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Paquetes faltantes: {', '.join(missing_packages)}")
        print("🔧 Instale las dependencias con:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def check_model_files():
    """Verifica que los archivos del modelo estén disponibles"""
    print("🤖 Verificando archivos del modelo...")
    
    models_dir = Path(__file__).parent.parent / "models"
    required_files = [
        "toxic_model.pkl",
        "vectorizer.pkl"
    ]
    
    missing_files = []
    
    for file_name in required_files:
        file_path = models_dir / file_name
        if file_path.exists():
            size_mb = file_path.stat().st_size / 1024 / 1024
            print(f"   ✅ {file_name} ({size_mb:.1f} MB)")
        else:
            print(f"   ❌ {file_name}")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n⚠️  Archivos del modelo faltantes: {', '.join(missing_files)}")
        print("🔧 Entrene el modelo primero con:")
        print("   cd ml && python train_model.py")
        print("\n💡 El backend funcionará con el clasificador mejorado como fallback")
        return False
    
    print("✅ Todos los archivos del modelo están disponibles")
    return True

def start_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = True):
    """Inicia el servidor FastAPI"""
    print(f"\n🚀 Iniciando ToxiGuard Backend...")
    print(f"   🌐 Host: {host}")
    print(f"   🔌 Puerto: {port}")
    print(f"   🔄 Reload: {'Sí' if reload else 'No'}")
    print(f"   📁 Directorio: {Path(__file__).parent}")
    print()
    
    # Configuración del servidor
    config = {
        "app": "app.main:app",
        "host": host,
        "port": port,
        "reload": reload,
        "log_level": os.getenv("LOG_LEVEL", "info").lower(),
        "access_log": True,
        "use_colors": True
    }
    
    if reload:
        print("🔄 Modo desarrollo activado - El servidor se recargará automáticamente")
        print("   Para detener: Ctrl+C")
        print()
    
    try:
        uvicorn.run(**config)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Inicio optimizado de ToxiGuard Backend")
    parser.add_argument("--env", choices=["development", "production"], default="development",
                       help="Tipo de entorno (default: development)")
    parser.add_argument("--host", default="127.0.0.1", help="Host del servidor (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor (default: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="Deshabilitar auto-reload")
    parser.add_argument("--check-only", action="store_true", help="Solo verificar dependencias y archivos")
    
    args = parser.parse_args()
    
    print("🚀 TOXIGUARD BACKEND - INICIO OPTIMIZADO")
    print("=" * 50)
    print(f"⏰ Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌍 Entorno: {args.env}")
    print()
    
    # Configurar entorno
    setup_environment(args.env)
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar archivos del modelo
    check_model_files()
    
    if args.check_only:
        print("\n✅ Verificación completada")
        return
    
    # Iniciar servidor
    reload_enabled = not args.no_reload and args.env == "development"
    start_server(args.host, args.port, reload_enabled)

if __name__ == "__main__":
    main()
