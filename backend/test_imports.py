#!/usr/bin/env python3
"""
🧪 Script de Prueba de Importaciones - ToxiGuard
Verifica que todos los módulos se puedan importar correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 Probando importaciones...")

try:
    print("1. Importando advanced_preprocessor...")
    from app.advanced_preprocessor import advanced_preprocessor
    print("   ✅ advanced_preprocessor importado correctamente")
except Exception as e:
    print(f"   ❌ Error importando advanced_preprocessor: {e}")
    import traceback
    traceback.print_exc()

try:
    print("2. Importando improved_classifier...")
    from app.improved_classifier import improved_classifier
    print("   ✅ improved_classifier importado correctamente")
except Exception as e:
    print(f"   ❌ Error importando improved_classifier: {e}")
    import traceback
    traceback.print_exc()

try:
    print("3. Importando services...")
    from app.services import toxicity_classifier, IMPROVED_CLASSIFIER_AVAILABLE
    print(f"   ✅ services importado correctamente")
    print(f"   📊 IMPROVED_CLASSIFIER_AVAILABLE: {IMPROVED_CLASSIFIER_AVAILABLE}")
except Exception as e:
    print(f"   ❌ Error importando services: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Prueba de importaciones completada!")
