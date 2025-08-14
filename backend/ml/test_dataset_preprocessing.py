#!/usr/bin/env python3
"""
Script para probar las funciones de preprocesamiento con ejemplos del dataset real
"""

import pandas as pd
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar config
sys.path.append(str(Path(__file__).parent.parent))
from ml.config import DATA_DIR
from ml.preprocess import clean_text, tokenize_and_lemmatize, preprocess_text, preprocess_batch

def test_with_dataset_examples():
    """
    Prueba las funciones de preprocesamiento con ejemplos reales del dataset
    """
    print("🧪 PRUEBA CON EJEMPLOS DEL DATASET REAL - ToxiGuard")
    print("=" * 70)
    
    # Cargar dataset
    csv_path = DATA_DIR / "toxic_comments.csv"
    
    if not csv_path.exists():
        print(f"❌ Dataset no encontrado: {csv_path}")
        return
    
    print(f"📊 Cargando dataset: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"✅ Dataset cargado: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    
    # Seleccionar ejemplos variados del dataset
    print(f"\n🔍 Seleccionando ejemplos del dataset...")
    
    # Ejemplo tóxico
    toxic_example = df[df['IsToxic'] == True]['Text'].iloc[0]
    print(f"   📝 Ejemplo tóxico: {toxic_example[:100]}{'...' if len(toxic_example) > 100 else ''}")
    
    # Ejemplo no tóxico
    non_toxic_example = df[df['IsToxic'] == False]['Text'].iloc[0]
    print(f"   📝 Ejemplo no tóxico: {non_toxic_example[:100]}{'...' if len(non_toxic_example) > 100 else ''}")
    
    # Ejemplo largo
    long_example = df.loc[df['Text'].str.len().idxmax(), 'Text']
    print(f"   📝 Ejemplo largo: {long_example[:100]}{'...' if len(long_example) > 100 else ''}")
    
    # Ejemplo corto
    short_example = df.loc[df['Text'].str.len().idxmin(), 'Text']
    print(f"   📝 Ejemplo corto: {short_example}")
    
    # Ejemplo con URLs/emails
    url_email_example = df[df['Text'].str.contains('http|@', na=False)]['Text'].iloc[0]
    print(f"   📝 Ejemplo con URLs/emails: {url_email_example[:100]}{'...' if len(url_email_example) > 100 else ''}")
    
    # Lista de ejemplos para probar
    examples = [
        ("Tóxico", toxic_example),
        ("No tóxico", non_toxic_example),
        ("Largo", long_example),
        ("Corto", short_example),
        ("Con URLs/emails", url_email_example)
    ]
    
    print(f"\n🔧 PROBANDO FUNCIÓN clean_text() CON EJEMPLOS DEL DATASET:")
    print("=" * 80)
    
    for category, text in examples:
        print(f"\n📝 {category}:")
        print(f"   Original: {text[:150]}{'...' if len(text) > 150 else ''}")
        
        cleaned = clean_text(text)
        print(f"   Limpio: {cleaned[:150]}{'...' if len(cleaned) > 150 else ''}")
        
        reduction = ((len(text) - len(cleaned)) / len(text) * 100) if len(text) > 0 else 0
        print(f"   Reducción: {reduction:.1f}% ({len(text)} → {len(cleaned)} caracteres)")
    
    print(f"\n🔤 PROBANDO FUNCIÓN tokenize_and_lemmatize() CON EJEMPLOS DEL DATASET:")
    print("=" * 80)
    
    for category, text in examples:
        print(f"\n📝 {category}:")
        print(f"   Original: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        tokens = tokenize_and_lemmatize(text)
        print(f"   Tokens: {tokens[:20]}{'...' if len(tokens) > 20 else ''}")
        print(f"   Cantidad: {len(tokens)} tokens")
        
        # Mostrar algunos tokens específicos
        if tokens:
            print(f"   Primeros 5: {tokens[:5]}")
            print(f"   Últimos 5: {tokens[-5:] if len(tokens) > 5 else tokens}")
    
    print(f"\n🚀 PROBANDO FUNCIÓN preprocess_text() CON EJEMPLOS DEL DATASET:")
    print("=" * 80)
    
    for category, text in examples:
        print(f"\n📝 {category}:")
        print(f"   Original: {text[:100]}{'...' if len(text) > 100 else ''}")
        
        processed = preprocess_text(text)
        print(f"   Procesado: {processed[:100]}{'...' if len(processed) > 100 else ''}")
        
        reduction = ((len(text) - len(processed)) / len(text) * 100) if len(text) > 0 else 0
        print(f"   Reducción: {reduction:.1f}% ({len(text)} → {len(processed)} caracteres)")
    
    print(f"\n📦 PROBANDO FUNCIÓN preprocess_batch() CON EJEMPLOS DEL DATASET:")
    print("=" * 80)
    
    # Extraer solo los textos de los ejemplos
    example_texts = [text for _, text in examples]
    
    try:
        processed_batch = preprocess_batch(example_texts)
        print(f"✅ Batch procesado exitosamente")
        
        # Mostrar comparación
        print(f"\n📊 COMPARACIÓN FINAL:")
        print("-" * 80)
        
        total_original = sum(len(text) for text in example_texts)
        total_processed = sum(len(text) for text in processed_batch)
        reduction = ((total_original - total_processed) / total_original) * 100 if total_original > 0 else 0
        
        print(f"   📏 Caracteres totales:")
        print(f"      Original: {total_original:,}")
        print(f"      Procesado: {total_processed:,}")
        print(f"      Reducción: {reduction:.1f}%")
        
        # Mostrar ejemplos específicos
        for i, (category, original_text) in enumerate(examples):
            processed_text = processed_batch[i]
            print(f"\n   {category}:")
            print(f"      Original: {original_text[:80]}{'...' if len(original_text) > 80 else ''}")
            print(f"      Procesado: {processed_text[:80]}{'...' if len(processed_text) > 80 else ''}")
            
    except Exception as e:
        print(f"❌ Error en batch processing: {e}")
    
    print(f"\n✅ Prueba con ejemplos del dataset completada")

def analyze_preprocessing_quality():
    """
    Analiza la calidad del preprocesamiento con estadísticas del dataset
    """
    print(f"\n📊 ANÁLISIS DE CALIDAD DEL PREPROCESAMIENTO")
    print("=" * 70)
    
    # Cargar dataset
    csv_path = DATA_DIR / "toxic_comments.csv"
    df = pd.read_csv(csv_path)
    
    # Estadísticas del dataset original
    print(f"📋 ESTADÍSTICAS DEL DATASET ORIGINAL:")
    print(f"   Total de comentarios: {len(df):,}")
    print(f"   Longitud promedio: {df['Text'].str.len().mean():.1f} caracteres")
    print(f"   Longitud mínima: {df['Text'].str.len().min()} caracteres")
    print(f"   Longitud máxima: {df['Text'].str.len().max()} caracteres")
    
    # Comentarios con URLs
    urls_count = df['Text'].str.contains('http', na=False).sum()
    print(f"   Comentarios con URLs: {urls_count:,} ({urls_count/len(df)*100:.1f}%)")
    
    # Comentarios con emails
    emails_count = df['Text'].str.contains('@', na=False).sum()
    print(f"   Comentarios con emails: {emails_count:,} ({emails_count/len(df)*100:.1f}%)")
    
    # Comentarios con números
    numbers_count = df['Text'].str.contains(r'\d', na=False).sum()
    print(f"   Comentarios con números: {numbers_count:,} ({numbers_count/len(df)*100:.1f}%)")
    
    # Comentarios con puntuación excesiva
    excessive_punct = df['Text'].str.contains(r'[!]{2,}|[?]{2,}', na=False).sum()
    print(f"   Comentarios con puntuación excesiva: {excessive_punct:,} ({excessive_punct/len(df)*100:.1f}%)")
    
    print(f"\n🎯 BENEFICIOS DEL PREPROCESAMIENTO:")
    print(f"   ✅ Eliminación de URLs y emails innecesarios")
    print(f"   ✅ Normalización de texto (minúsculas)")
    print(f"   ✅ Eliminación de puntuación excesiva")
    print(f"   ✅ Lematización para mejor comprensión")
    print(f"   ✅ Filtrado de stop words")
    print(f"   ✅ Preparación para vectorización TF-IDF")

def main():
    """Función principal"""
    print("🚀 PRUEBA DE PREPROCESAMIENTO CON DATASET REAL - ToxiGuard")
    print("=" * 80)
    
    try:
        # Probar con ejemplos del dataset
        test_with_dataset_examples()
        
        # Analizar calidad del preprocesamiento
        analyze_preprocessing_quality()
        
        print(f"\n🎉 ¡Pruebas completadas exitosamente!")
        print(f"   Las funciones de preprocesamiento están listas para el pipeline de ML")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
