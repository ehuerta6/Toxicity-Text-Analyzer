#!/usr/bin/env python3
"""
Script para cargar y explorar el dataset de comentarios tóxicos
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar config
sys.path.append(str(Path(__file__).parent.parent))
from ml.config import DATA_DIR

def load_toxic_comments_dataset():
    """Carga el dataset de comentarios tóxicos"""
    print("📊 Cargando dataset de comentarios tóxicos...")
    
    try:
        # Ruta al archivo CSV
        csv_path = DATA_DIR / "toxic_comments.csv"
        
        if not csv_path.exists():
            print(f"   ❌ Archivo no encontrado: {csv_path}")
            return None
        
        print(f"   📁 Archivo encontrado: {csv_path}")
        print(f"   📏 Tamaño del archivo: {csv_path.stat().st_size / 1024:.1f} KB")
        
        # Cargar el dataset
        print("   📥 Cargando CSV...")
        df = pd.read_csv(csv_path)
        
        print(f"   ✅ Dataset cargado exitosamente")
        print(f"   📊 Forma del dataset: {df.shape}")
        
        return df
        
    except Exception as e:
        print(f"   ❌ Error cargando dataset: {e}")
        return None

def explore_dataset(df):
    """Explora la estructura y contenido del dataset"""
    if df is None:
        return
    
    print("\n🔍 EXPLORANDO DATASET")
    print("=" * 50)
    
    # Información básica
    print("📋 INFORMACIÓN BÁSICA:")
    print(f"   Filas: {df.shape[0]:,}")
    print(f"   Columnas: {df.shape[1]}")
    
    # Columnas disponibles
    print(f"\n🏷️  COLUMNAS DISPONIBLES ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")
    
    # Tipos de datos
    print(f"\n🔧 TIPOS DE DATOS:")
    for col, dtype in df.dtypes.items():
        print(f"   {col}: {dtype}")
    
    # Primeras filas
    print(f"\n👀 PRIMERAS 5 FILAS:")
    print("-" * 50)
    print(df.head().to_string(index=False))
    
    # Estadísticas de las columnas de etiquetas
    label_columns = [col for col in df.columns if col not in ['id', 'comment_text']]
    if label_columns:
        print(f"\n📊 ESTADÍSTICAS DE ETIQUETAS:")
        print("-" * 50)
        
        for col in label_columns:
            if col in df.columns:
                value_counts = df[col].value_counts()
                total = len(df)
                print(f"\n   {col}:")
                for value, count in value_counts.items():
                    percentage = (count / total) * 100
                    print(f"     {value}: {count:,} ({percentage:.1f}%)")
    
    # Información sobre comentarios
    if 'comment_text' in df.columns:
        print(f"\n📝 ESTADÍSTICAS DE TEXTO:")
        print("-" * 50)
        
        # Longitud de comentarios
        text_lengths = df['comment_text'].str.len()
        print(f"   Longitud promedio: {text_lengths.mean():.1f} caracteres")
        print(f"   Longitud mínima: {text_lengths.min()} caracteres")
        print(f"   Longitud máxima: {text_lengths.max()} caracteres")
        
        # Comentarios vacíos
        empty_comments = df['comment_text'].isna().sum()
        print(f"   Comentarios vacíos: {empty_comments:,}")
        
        # Ejemplos de comentarios tóxicos
        print(f"\n💀 EJEMPLOS DE COMENTARIOS TÓXICOS:")
        print("-" * 50)
        
        for label in label_columns[:3]:  # Solo las primeras 3 etiquetas
            if label in df.columns:
                toxic_examples = df[df[label] == 1]['comment_text'].head(2)
                if not toxic_examples.empty:
                    print(f"\n   {label}:")
                    for i, text in enumerate(toxic_examples, 1):
                        print(f"     {i}. {text[:100]}{'...' if len(text) > 100 else ''}")

def show_data_preview(df):
    """Muestra una vista previa más detallada de los datos"""
    if df is None:
        return
    
    print(f"\n📋 VISTA PREVIA COMPLETA")
    print("=" * 80)
    
    # Mostrar información del dataset
    print(f"Dataset: toxic_comments.csv")
    print(f"Forma: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    print(f"Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # Mostrar las primeras filas con formato mejorado
    print(f"\n📊 PRIMERAS 5 FILAS DEL DATASET:")
    print("=" * 80)
    
    # Configurar pandas para mostrar más información
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print(df.head().to_string(index=True))
    
    # Mostrar información de columnas
    print(f"\n🏷️  INFORMACIÓN DE COLUMNAS:")
    print("=" * 80)
    print(df.info())

def main():
    """Función principal"""
    print("🚀 CARGA Y EXPLORACIÓN DE DATASET - ToxiGuard")
    print("=" * 60)
    
    # Cargar dataset
    df = load_toxic_comments_dataset()
    
    if df is not None:
        # Explorar dataset
        explore_dataset(df)
        
        # Mostrar vista previa detallada
        show_data_preview(df)
        
        print(f"\n🎉 Dataset cargado y explorado exitosamente!")
        print(f"   Listo para preprocesamiento y entrenamiento de modelos")
    else:
        print(f"\n❌ No se pudo cargar el dataset")
        print(f"   Verifica que el archivo toxic_comments.csv esté en la carpeta data/")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
