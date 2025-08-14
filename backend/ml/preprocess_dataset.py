#!/usr/bin/env python3
"""
Script para preprocesar el dataset completo de comentarios tóxicos
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import time

# Agregar el directorio padre al path para importar config
sys.path.append(str(Path(__file__).parent.parent))
from ml.config import DATA_DIR
from ml.preprocessor import TextPreprocessor

def load_and_preprocess_dataset():
    """Carga y preprocesa el dataset completo"""
    print("🚀 CARGA Y PREPROCESAMIENTO DEL DATASET - ToxiGuard")
    print("=" * 70)
    
    # 1. Cargar dataset
    print("\n📊 PASO 1: Cargando dataset...")
    csv_path = DATA_DIR / "toxic_comments.csv"
    
    if not csv_path.exists():
        print(f"   ❌ Archivo no encontrado: {csv_path}")
        return None
    
    print(f"   📁 Archivo encontrado: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"   ✅ Dataset cargado: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    
    # 2. Inicializar preprocesador
    print("\n🔧 PASO 2: Inicializando preprocesador...")
    try:
        preprocessor = TextPreprocessor()
        print(f"   ✅ Preprocesador inicializado")
    except Exception as e:
        print(f"   ❌ Error inicializando preprocesador: {e}")
        return None
    
    # 3. Preprocesar dataset
    print("\n🔄 PASO 3: Preprocesando textos...")
    start_time = time.time()
    
    try:
        # Preprocesar la columna de texto
        df_processed = preprocessor.preprocess_dataframe(
            df, 
            text_column="Text", 
            new_column="ProcessedText"
        )
        
        processing_time = time.time() - start_time
        print(f"   ✅ Preprocesamiento completado en {processing_time:.2f} segundos")
        
    except Exception as e:
        print(f"   ❌ Error durante preprocesamiento: {e}")
        return None
    
    # 4. Mostrar resultados
    print("\n📋 PASO 4: Analizando resultados...")
    
    # Comparar textos originales vs procesados
    print(f"\n👀 COMPARACIÓN DE TEXTO ORIGINAL VS PROCESADO:")
    print("-" * 80)
    
    for i in range(min(5, len(df_processed))):
        original_text = df_processed.iloc[i]["Text"]
        processed_text = df_processed.iloc[i]["ProcessedText"]
        
        print(f"\n📝 Comentario {i+1}:")
        print(f"   Original: {original_text[:100]}{'...' if len(original_text) > 100 else ''}")
        print(f"   Procesado: {processed_text[:100]}{'...' if len(processed_text) > 100 else ''}")
        
        # Estadísticas del texto
        stats = preprocessor.get_text_statistics(original_text)
        print(f"   📊 Longitud: {stats['original_length']} → {stats['processed_length']} caracteres")
        print(f"   🔤 Tokens: {stats['token_count']} → {len(processed_text.split())} palabras")
    
    # 5. Estadísticas del dataset procesado
    print(f"\n📊 ESTADÍSTICAS DEL DATASET PROCESADO:")
    print("-" * 80)
    
    # Longitudes de texto
    original_lengths = df_processed["Text"].str.len()
    processed_lengths = df_processed["ProcessedText"].str.len()
    
    print(f"   📏 Longitud de texto original:")
    print(f"      Promedio: {original_lengths.mean():.1f} caracteres")
    print(f"      Mínima: {original_lengths.min()} caracteres")
    print(f"      Máxima: {original_lengths.max()} caracteres")
    
    print(f"\n   📏 Longitud de texto procesado:")
    print(f"      Promedio: {processed_lengths.mean():.1f} caracteres")
    print(f"      Mínima: {processed_lengths.min()} caracteres")
    print(f"      Máxima: {processed_lengths.max()} caracteres")
    
    # Reducción de longitud
    reduction = ((original_lengths.mean() - processed_lengths.mean()) / original_lengths.mean()) * 100
    print(f"\n   📉 Reducción promedio: {reduction:.1f}%")
    
    # 6. Guardar dataset procesado
    print(f"\n💾 PASO 5: Guardando dataset procesado...")
    
    output_path = DATA_DIR / "toxic_comments_processed.csv"
    try:
        df_processed.to_csv(output_path, index=False)
        print(f"   ✅ Dataset guardado en: {output_path}")
        print(f"   📏 Tamaño del archivo: {output_path.stat().st_size / 1024:.1f} KB")
    except Exception as e:
        print(f"   ❌ Error guardando archivo: {e}")
    
    # 7. Resumen final
    print(f"\n🎉 RESUMEN FINAL:")
    print("-" * 80)
    print(f"   📊 Dataset original: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    print(f"   📊 Dataset procesado: {df_processed.shape[0]:,} filas × {df_processed.shape[1]} columnas")
    print(f"   ⏱️  Tiempo de procesamiento: {processing_time:.2f} segundos")
    print(f"   📉 Reducción de texto: {reduction:.1f}%")
    print(f"   💾 Archivo guardado: {output_path.name}")
    
    return df_processed

def analyze_toxicity_distribution(df):
    """Analiza la distribución de toxicidad en el dataset"""
    if df is None:
        return
    
    print(f"\n🔍 ANÁLISIS DE DISTRIBUCIÓN DE TOXICIDAD:")
    print("-" * 80)
    
    # Columnas de etiquetas (excluyendo las de texto)
    label_columns = [col for col in df.columns if col.startswith("Is") and col not in ["IsToxic"]]
    
    print(f"   🏷️  Etiquetas disponibles: {len(label_columns)}")
    
    # Distribución de la etiqueta principal
    if "IsToxic" in df.columns:
        toxic_dist = df["IsToxic"].value_counts()
        total = len(df)
        print(f"\n   🎯 Distribución de IsToxic:")
        for value, count in toxic_dist.items():
            percentage = (count / total) * 100
            print(f"      {value}: {count:,} ({percentage:.1f}%)")
    
    # Distribución de otras etiquetas
    print(f"\n   📊 Distribución de otras etiquetas:")
    for col in label_columns[:5]:  # Solo las primeras 5 para no saturar
        if col in df.columns:
            dist = df[col].value_counts()
            total = len(df)
            print(f"\n      {col}:")
            for value, count in dist.items():
                percentage = (count / total) * 100
                print(f"         {value}: {count:,} ({percentage:.1f}%)")

def main():
    """Función principal"""
    print("🚀 PREPROCESAMIENTO COMPLETO DEL DATASET - ToxiGuard")
    print("=" * 80)
    
    try:
        # Cargar y preprocesar dataset
        df_processed = load_and_preprocess_dataset()
        
        if df_processed is not None:
            # Analizar distribución de toxicidad
            analyze_toxicity_distribution(df_processed)
            
            print(f"\n🎉 ¡Proceso completado exitosamente!")
            print(f"   El dataset está listo para vectorización y entrenamiento")
        else:
            print(f"\n❌ No se pudo completar el proceso")
            
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
