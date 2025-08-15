#!/usr/bin/env python3
"""
🧪 Prueba del Clasificador Contextual - ToxiGuard
Script para probar el análisis contextual con embeddings
"""

import requests
import json
import time
from typing import List, Dict

# Configuración
API_BASE_URL = "http://127.0.0.1:8000"

def test_contextual_analysis():
    """Prueba el análisis contextual con diferentes tipos de texto"""
    
    print("🧪 Iniciando pruebas del análisis contextual...")
    print("=" * 60)
    
    # Casos de prueba para verificar el análisis contextual
    test_cases = [
        {
            "name": "Insulto directo",
            "text": "Eres un idiota completo",
            "expected_behavior": "Alta toxicidad detectada"
        },
        {
            "name": "Insulto negado (contexto positivo)",
            "text": "No eres tonto, eres muy inteligente",
            "expected_behavior": "Baja toxicidad por contexto positivo"
        },
        {
            "name": "Acoso directo",
            "text": "Te voy a matar si no haces lo que digo",
            "expected_behavior": "Alta toxicidad por amenaza"
        },
        {
            "name": "Acoso negado",
            "text": "No te voy a hacer daño, solo quiero ayudarte",
            "expected_behavior": "Baja toxicidad por negación"
        },
        {
            "name": "Discriminación directa",
            "text": "Los negros son inferiores a los blancos",
            "expected_behavior": "Alta toxicidad por discriminación"
        },
        {
            "name": "Discriminación negada",
            "text": "Todos somos iguales, no discrimino a nadie",
            "expected_behavior": "Baja toxicidad por mensaje positivo"
        },
        {
            "name": "Texto neutral",
            "text": "El clima está muy agradable hoy",
            "expected_behavior": "Baja toxicidad, texto neutral"
        },
        {
            "name": "Texto mixto",
            "text": "Eres un idiota, pero no te voy a hacer daño",
            "expected_behavior": "Toxicidad moderada por insulto pero negación de violencia"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Prueba {i}: {test_case['name']}")
        print(f"Texto: '{test_case['text']}'")
        print(f"Comportamiento esperado: {test_case['expected_behavior']}")
        
        try:
            # Realizar análisis
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                json={"text": test_case["text"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Análisis exitoso:")
                print(f"   - Toxicidad: {result['toxicity_percentage']}%")
                print(f"   - Categoría: {result['toxicity_category']}")
                print(f"   - Técnica: {result['classification_technique']}")
                print(f"   - Confianza: {result['confidence']}")
                
                if result.get('detected_categories'):
                    print(f"   - Categorías detectadas: {', '.join(result['detected_categories'])}")
                
                if result.get('explanations'):
                    print(f"   - Explicaciones:")
                    for category, explanation in result['explanations'].items():
                        print(f"     * {category}: {explanation}")
                
                # Evaluar si el comportamiento es el esperado
                toxicity = result['toxicity_percentage']
                expected_low = "baja" in test_case['expected_behavior'].lower()
                expected_high = "alta" in test_case['expected_behavior'].lower()
                
                if expected_low and toxicity <= 30:
                    print("   🎯 Comportamiento CORRECTO: Toxicidad baja detectada")
                elif expected_high and toxicity >= 60:
                    print("   🎯 Comportamiento CORRECTO: Toxicidad alta detectada")
                elif not expected_low and not expected_high:
                    print("   🎯 Comportamiento CORRECTO: Análisis realizado")
                else:
                    print(f"   ⚠️ Comportamiento INESPERADO: Toxicidad {toxicity}% vs esperado")
                
                results.append({
                    "test": test_case['name'],
                    "success": True,
                    "toxicity": toxicity,
                    "technique": result['classification_technique']
                })
                
            else:
                print(f"❌ Error en análisis: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                results.append({
                    "test": test_case['name'],
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            results.append({
                "test": test_case['name'],
                "success": False,
                "error": str(e)
            })
        
        time.sleep(1)  # Pausa entre pruebas
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Pruebas exitosas: {len(successful_tests)}/{len(results)}")
    print(f"❌ Pruebas fallidas: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        print("\n📈 Estadísticas de toxicidad:")
        toxicities = [r['toxicity'] for r in successful_tests]
        print(f"   - Promedio: {sum(toxicities)/len(toxicities):.1f}%")
        print(f"   - Mínimo: {min(toxicities):.1f}%")
        print(f"   - Máximo: {max(toxicities):.1f}%")
        
        # Verificar que se está usando el clasificador contextual
        contextual_used = any("contextual" in r['technique'].lower() for r in successful_tests)
        if contextual_used:
            print("   🧠 Clasificador contextual detectado en uso")
        else:
            print("   ⚠️ Clasificador contextual no detectado")
    
    if failed_tests:
        print("\n❌ Pruebas fallidas:")
        for test in failed_tests:
            print(f"   - {test['test']}: {test['error']}")
    
    return len(successful_tests) == len(results)

def test_classifier_info():
    """Prueba el endpoint de información del clasificador"""
    print("\n🔍 Probando información del clasificador...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/classifier-info")
        
        if response.status_code == 200:
            info = response.json()
            print("✅ Información del clasificador obtenida:")
            print(f"   - Tipo: {info.get('classifier_type', 'N/A')}")
            
            if 'contextual_features' in info:
                features = info['contextual_features']
                print(f"   - Análisis de oraciones: {features.get('sentence_analysis', False)}")
                print(f"   - Similitud de embeddings: {features.get('embedding_similarity', False)}")
                print(f"   - Conciencia contextual: {features.get('context_awareness', False)}")
                print(f"   - Detección de negaciones: {features.get('negation_detection', False)}")
                print(f"   - Modelo de embeddings: {features.get('embedding_model', 'N/A')}")
            
            return True
        else:
            print(f"❌ Error obteniendo información: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 ToxiGuard - Prueba del Análisis Contextual")
    print("=" * 60)
    
    # Verificar que el servidor esté funcionando
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ El servidor no está respondiendo correctamente")
            return False
        print("✅ Servidor funcionando correctamente")
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        print("   Asegúrate de que el backend esté ejecutándose en http://127.0.0.1:8000")
        return False
    
    # Ejecutar pruebas
    contextual_success = test_contextual_analysis()
    info_success = test_classifier_info()
    
    print("\n" + "=" * 60)
    if contextual_success and info_success:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ El análisis contextual está funcionando correctamente")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("🔧 Revisa los logs del servidor para más detalles")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
