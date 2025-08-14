#!/usr/bin/env python3
"""
Script para probar la mejora en la detección de toxicidad
"""

import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000"

def test_toxicity_detection():
    """Prueba detección de toxicidad con textos específicos"""
    print("🧪 Probando detección mejorada de toxicidad...")
    
    test_cases = [
        {
            "text": "Hola, ¡qué bonito día!",
            "expected": False,
            "description": "Texto completamente seguro"
        },
        {
            "text": "Eres un idiota estúpido",
            "expected": True,
            "description": "Insulto directo - debería ser tóxico"
        },
        {
            "text": "Vete al diablo, imbécil",
            "expected": True,
            "description": "Múltiples insultos - debería ser tóxico"
        },
        {
            "text": "Me encanta esta nueva tecnología",
            "expected": False,
            "description": "Comentario positivo"
        },
        {
            "text": "Fuck you, asshole!",
            "expected": True,
            "description": "Insultos en inglés - debería ser tóxico"
        },
        {
            "text": "Este producto es una mierda",
            "expected": True,
            "description": "Palabra tóxica - debería ser tóxico"
        }
    ]
    
    results = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}: {case['description']}")
        print(f"   Texto: '{case['text']}'")
        print(f"   Esperado: {'Tóxico' if case['expected'] else 'Seguro'}")
        
        try:
            response = requests.post(f"{BASE_URL}/analyze", json={"text": case['text']})
            
            if response.status_code == 200:
                result = response.json()
                actual_toxic = result.get('toxic', False)
                percentage = result.get('toxicity_percentage', 0)
                category = result.get('category', 'N/A')
                keywords_found = result.get('keywords_found', 0)
                
                print(f"   ✅ Resultado: {'Tóxico' if actual_toxic else 'Seguro'} ({percentage:.1f}%)")
                print(f"   📊 Categoría: {category}")
                print(f"   🔍 Palabras encontradas: {keywords_found}")
                
                # Verificar si coincide con lo esperado
                if actual_toxic == case['expected']:
                    print("   ✅ CORRECTO - Detección esperada")
                    results.append(True)
                else:
                    print("   ❌ INCORRECTO - Detección inesperada")
                    results.append(False)
                    
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append(False)
    
    # Resumen
    correct = sum(results)
    total = len(results)
    accuracy = (correct / total) * 100
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    print(f"✅ Casos correctos: {correct}/{total}")
    print(f"📈 Precisión: {accuracy:.1f}%")
    
    if accuracy >= 80:
        print("🎉 ¡Excelente! La detección está funcionando bien")
    elif accuracy >= 60:
        print("⚠️ La detección necesita mejoras")
    else:
        print("❌ La detección tiene problemas serios")

def main():
    """Función principal"""
    print("=" * 60)
    print("🔍 PRUEBA DE DETECCIÓN DE TOXICIDAD MEJORADA")
    print("=" * 60)
    
    try:
        # Verificar conexión
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Servidor no disponible")
            return
            
        test_toxicity_detection()
        
    except requests.exceptions.RequestException:
        print("❌ No se pudo conectar al servidor")
        print("Asegúrate de que el backend esté ejecutándose en http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
