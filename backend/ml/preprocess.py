#!/usr/bin/env python3
"""
Funciones de preprocesamiento de texto para ToxiGuard
"""

import re
import spacy
import pandas as pd
from typing import List, Tuple
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar config
sys.path.append(str(Path(__file__).parent.parent))
from ml.config import SPACY_MODEL, SPACY_DISABLE

def clean_text(text: str) -> str:
    """
    Limpia el texto eliminando caracteres especiales y normalizando
    
    Args:
        text: Texto a limpiar
        
    Returns:
        Texto limpio y normalizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convertir a minúsculas
    text = text.lower()
    
    # Eliminar URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Eliminar emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    # Eliminar caracteres especiales y números (mantener solo letras y espacios)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Eliminar múltiples espacios y espacios al inicio/final
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize_and_lemmatize(text: str, nlp: spacy.language.Language = None) -> List[str]:
    """
    Tokeniza y lematiza el texto usando spaCy
    
    Args:
        text: Texto a procesar
        nlp: Modelo de spaCy (opcional, se crea si no se proporciona)
        
    Returns:
        Lista de tokens lematizados sin stopwords ni puntuación
    """
    if not text:
        return []
    
    # Crear modelo de spaCy si no se proporciona
    if nlp is None:
        try:
            nlp = spacy.load(SPACY_MODEL, disable=SPACY_DISABLE)
        except Exception as e:
            print(f"❌ Error cargando modelo spaCy: {e}")
            return []
    
    # Procesar texto con spaCy
    doc = nlp(text)
    
    # Extraer tokens lematizados, filtrando stopwords y puntuación
    tokens = []
    for token in doc:
        # Filtrar stopwords
        if token.is_stop:
            continue
            
        # Filtrar puntuación
        if token.is_punct:
            continue
            
        # Filtrar espacios
        if token.is_space:
            continue
            
        # Filtrar tokens muy cortos
        if len(token.text) < 2:
            continue
        
        # Obtener lema y agregar si no está vacío
        lemma = token.lemma_.strip()
        if lemma:
            tokens.append(lemma)
    
    return tokens

def preprocess_text(text: str, nlp: spacy.language.Language = None) -> str:
    """
    Preprocesa texto completo: limpia, tokeniza y lematiza
    
    Args:
        text: Texto a preprocesar
        nlp: Modelo de spaCy (opcional)
        
    Returns:
        Texto preprocesado como string
    """
    # Limpiar texto
    clean_text_result = clean_text(text)
    
    # Tokenizar y lematizar
    tokens = tokenize_and_lemmatize(clean_text_result, nlp)
    
    # Unir tokens en string
    return " ".join(tokens)

def preprocess_batch(texts: List[str], nlp: spacy.language.Language = None) -> List[str]:
    """
    Preprocesa una lista de textos en lote
    
    Args:
        texts: Lista de textos a preprocesar
        nlp: Modelo de spaCy (opcional)
        
    Returns:
        Lista de textos preprocesados
    """
    if not texts:
        return []
    
    print(f"🔄 Preprocesando lote de {len(texts)} textos...")
    
    # Crear modelo de spaCy una sola vez si no se proporciona
    if nlp is None:
        try:
            nlp = spacy.load(SPACY_MODEL, disable=SPACY_DISABLE)
            print(f"   📥 Modelo spaCy cargado: {SPACY_MODEL}")
        except Exception as e:
            print(f"   ❌ Error cargando modelo spaCy: {e}")
            return []
    
    processed_texts = []
    for i, text in enumerate(texts):
        if i % 100 == 0:
            print(f"   📝 Procesando texto {i+1}/{len(texts)}")
        
        processed = preprocess_text(text, nlp)
        processed_texts.append(processed)
    
    print(f"   ✅ Lote preprocesado exitosamente")
    return processed_texts

def analyze_preprocessing_results(original_texts: List[str], processed_texts: List[str]) -> None:
    """
    Analiza y muestra los resultados del preprocesamiento
    
    Args:
        original_texts: Lista de textos originales
        processed_texts: Lista de textos procesados
    """
    if len(original_texts) != len(processed_texts):
        print("❌ Las listas de textos originales y procesados deben tener la misma longitud")
        return
    
    print(f"\n📊 ANÁLISIS DE RESULTADOS DE PREPROCESAMIENTO")
    print("=" * 70)
    
    # Estadísticas generales
    total_original = sum(len(text) for text in original_texts)
    total_processed = sum(len(text) for text in processed_texts)
    reduction = ((total_original - total_processed) / total_original) * 100 if total_original > 0 else 0
    
    print(f"   📏 Caracteres totales:")
    print(f"      Original: {total_original:,}")
    print(f"      Procesado: {total_processed:,}")
    print(f"      Reducción: {reduction:.1f}%")
    
    # Mostrar ejemplos
    print(f"\n👀 EJEMPLOS DE PREPROCESAMIENTO:")
    print("-" * 70)
    
    for i in range(min(5, len(original_texts))):
        original = original_texts[i]
        processed = processed_texts[i]
        
        print(f"\n📝 Texto {i+1}:")
        print(f"   Original: {original[:100]}{'...' if len(original) > 100 else ''}")
        print(f"   Procesado: {processed[:100]}{'...' if len(processed) > 100 else ''}")
        print(f"   Longitud: {len(original)} → {len(processed)} caracteres")
        print(f"   Reducción: {((len(original) - len(processed)) / len(original) * 100):.1f}%")

def test_preprocessing_functions():
    """
    Prueba las funciones de preprocesamiento con ejemplos del dataset
    """
    print("🧪 PRUEBA DE FUNCIONES DE PREPROCESAMIENTO")
    print("=" * 70)
    
    # Ejemplos de texto del dataset
    test_texts = [
        "Hello world! This is a test sentence.",
        "Check out this link: https://example.com and email me@test.com",
        "I can't believe this is happening!!!",
        "The quick brown fox jumps over the lazy dog 123.",
        "Law enforcement is not trained to shoot to apprehend. They are trained to shoot to kill."
    ]
    
    print(f"📝 Textos de prueba ({len(test_texts)}):")
    for i, text in enumerate(test_texts, 1):
        print(f"   {i}. {text}")
    
    # Probar función clean_text
    print(f"\n🔧 PROBANDO FUNCIÓN clean_text():")
    print("-" * 50)
    
    for i, text in enumerate(test_texts, 1):
        cleaned = clean_text(text)
        print(f"   {i}. Original: {text}")
        print(f"      Limpio: {cleaned}")
        print(f"      Reducción: {((len(text) - len(cleaned)) / len(text) * 100):.1f}%")
        print()
    
    # Probar función tokenize_and_lemmatize
    print(f"🔤 PROBANDO FUNCIÓN tokenize_and_lemmatize():")
    print("-" * 50)
    
    try:
        nlp = spacy.load(SPACY_MODEL, disable=SPACY_DISABLE)
        print(f"   ✅ Modelo spaCy cargado: {SPACY_MODEL}")
        
        for i, text in enumerate(test_texts, 1):
            tokens = tokenize_and_lemmatize(text, nlp)
            print(f"   {i}. Original: {text}")
            print(f"      Tokens: {tokens}")
            print(f"      Cantidad: {len(tokens)} tokens")
            print()
            
    except Exception as e:
        print(f"   ❌ Error cargando spaCy: {e}")
    
    # Probar función preprocess_text
    print(f"🚀 PROBANDO FUNCIÓN preprocess_text():")
    print("-" * 50)
    
    try:
        nlp = spacy.load(SPACY_MODEL, disable=SPACY_DISABLE)
        
        for i, text in enumerate(test_texts, 1):
            processed = preprocess_text(text, nlp)
            print(f"   {i}. Original: {text}")
            print(f"      Procesado: {processed}")
            print(f"      Reducción: {((len(text) - len(processed)) / len(text) * 100):.1f}%")
            print()
            
    except Exception as e:
        print(f"   ❌ Error en preprocesamiento: {e}")
    
    # Probar función preprocess_batch
    print(f"📦 PROBANDO FUNCIÓN preprocess_batch():")
    print("-" * 50)
    
    try:
        processed_batch = preprocess_batch(test_texts)
        print(f"   ✅ Batch procesado exitosamente")
        
        # Analizar resultados
        analyze_preprocessing_results(test_texts, processed_batch)
        
    except Exception as e:
        print(f"   ❌ Error en batch processing: {e}")
    
    print(f"\n✅ Prueba de funciones completada")

def main():
    """Función principal"""
    print("🚀 FUNCIONES DE PREPROCESAMIENTO DE TEXTO - ToxiGuard")
    print("=" * 70)
    
    try:
        # Probar todas las funciones
        test_preprocessing_functions()
        
        print(f"\n🎉 Funciones de preprocesamiento probadas exitosamente!")
        print(f"   Listas para usar en el pipeline de ML")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
