#!/usr/bin/env python3
"""
Script para entrenar modelo de Machine Learning para detección de toxicidad
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

# Agregar el directorio padre al path para importar config
sys.path.append(str(Path(__file__).parent.parent))
from ml.config import DATA_DIR, MODELS_DIR, RANDOM_STATE, TEST_SIZE
from ml.preprocess import preprocess_batch

def load_and_preprocess_dataset():
    """
    Carga y preprocesa el dataset completo
    """
    print("📊 PASO 1: Cargando y preprocesando dataset...")
    
    # Cargar dataset
    csv_path = DATA_DIR / "toxic_comments.csv"
    
    if not csv_path.exists():
        print(f"   ❌ Dataset no encontrado: {csv_path}")
        return None, None
    
    print(f"   📁 Archivo encontrado: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"   ✅ Dataset cargado: {df.shape[0]:,} filas × {df.shape[1]} columnas")
    
    # Verificar columnas necesarias
    if 'Text' not in df.columns or 'IsToxic' not in df.columns:
        print(f"   ❌ Columnas 'Text' o 'IsToxic' no encontradas")
        print(f"   📋 Columnas disponibles: {list(df.columns)}")
        return None, None
    
    # Preprocesar textos
    print(f"   🔄 Preprocesando {len(df)} textos...")
    start_time = time.time()
    
    try:
        processed_texts = preprocess_batch(df['Text'].tolist())
        processing_time = time.time() - start_time
        
        print(f"   ✅ Preprocesamiento completado en {processing_time:.2f} segundos")
        
        # Agregar columna procesada
        df['ProcessedText'] = processed_texts
        
        # Verificar que no haya textos vacíos
        empty_texts = df['ProcessedText'].str.len() == 0
        if empty_texts.sum() > 0:
            print(f"   ⚠️  {empty_texts.sum()} textos quedaron vacíos después del preprocesamiento")
            # Filtrar textos vacíos
            df = df[~empty_texts].reset_index(drop=True)
            print(f"   ✅ Dataset filtrado: {len(df)} filas restantes")
        
        return df, processed_texts
        
    except Exception as e:
        print(f"   ❌ Error durante preprocesamiento: {e}")
        return None, None

def prepare_features_and_labels(df):
    """
    Prepara características (X) y etiquetas (y) para el entrenamiento
    """
    print(f"\n🔧 PASO 2: Preparando características y etiquetas...")
    
    # Usar texto procesado como características
    X = df['ProcessedText'].values
    y = df['IsToxic'].values
    
    print(f"   📝 Características (X): {len(X)} textos")
    print(f"   🏷️  Etiquetas (y): {len(y)} valores")
    
    # Verificar distribución de clases
    unique, counts = np.unique(y, return_counts=True)
    print(f"   📊 Distribución de clases:")
    for label, count in zip(unique, counts):
        percentage = (count / len(y)) * 100
        print(f"      Clase {label}: {count:,} ({percentage:.1f}%)")
    
    # Dividir en train y test
    print(f"   🔀 Dividiendo en train ({1-TEST_SIZE:.0%}) y test ({TEST_SIZE:.0%})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    
    print(f"   ✅ Datos divididos:")
    print(f"      Train: {len(X_train):,} muestras")
    print(f"      Test: {len(X_test):,} muestras")
    
    return X_train, X_test, y_train, y_test

def create_and_train_models(X_train, X_test, y_train, y_test):
    """
    Crea y entrena modelos de clasificación
    """
    print(f"\n🤖 PASO 3: Creando y entrenando modelos...")
    
    # Configurar vectorizador TF-IDF
    print(f"   📊 Configurando TfidfVectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=10000,  # Máximo 10,000 características
        min_df=2,            # Término debe aparecer en al menos 2 documentos
        max_df=0.95,         # Término no debe aparecer en más del 95% de documentos
        ngram_range=(1, 2),  # Unigramas y bigramas
        stop_words='english' # Stop words en inglés
    )
    
    # Modelos a entrenar
    models = {
        'LogisticRegression': LogisticRegression(
            random_state=RANDOM_STATE,
            max_iter=1000,
            C=1.0
        ),
        'MultinomialNB': MultinomialNB(
            alpha=1.0
        )
    }
    
    results = {}
    
    for model_name, model in models.items():
        print(f"\n   🚀 Entrenando {model_name}...")
        
        # Crear pipeline
        pipeline = Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', model)
        ])
        
        # Entrenar modelo
        start_time = time.time()
        pipeline.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        # Predecir en test
        y_pred = pipeline.predict(X_test)
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"      ⏱️  Tiempo de entrenamiento: {training_time:.2f} segundos")
        print(f"      📊 Accuracy: {accuracy:.4f}")
        print(f"      🎯 F1-Score: {f1:.4f}")
        
        # Guardar resultados
        results[model_name] = {
            'pipeline': pipeline,
            'accuracy': accuracy,
            'f1_score': f1,
            'training_time': training_time,
            'predictions': y_pred
        }
    
    return results, vectorizer

def evaluate_models(results, y_test, X_test):
    """
    Evalúa los modelos entrenados con métricas detalladas
    """
    print(f"\n📈 PASO 4: Evaluando modelos...")
    
    best_model = None
    best_score = 0
    
    for model_name, result in results.items():
        print(f"\n   📊 EVALUACIÓN DE {model_name.upper()}:")
        print("-" * 50)
        
        # Métricas básicas
        print(f"      Accuracy: {result['accuracy']:.4f}")
        print(f"      F1-Score: {result['f1_score']:.4f}")
        print(f"      Tiempo de entrenamiento: {result['training_time']:.2f}s")
        
        # Reporte de clasificación
        print(f"\n      📋 REPORTE DE CLASIFICACIÓN:")
        report = classification_report(y_test, result['predictions'], target_names=['No Tóxico', 'Tóxico'])
        for line in report.split('\n'):
            if line.strip():
                print(f"         {line}")
        
        # Matriz de confusión
        cm = confusion_matrix(y_test, result['predictions'])
        print(f"\n      🎯 MATRIZ DE CONFUSIÓN:")
        print(f"         Predicción")
        print(f"         No Tóxico  Tóxico")
        print(f"Actual   {cm[0][0]:>8}  {cm[0][1]:>6}")
        print(f"No Tóxico")
        print(f"Actual   {cm[1][0]:>8}  {cm[1][1]:>6}")
        print(f"Tóxico")
        
        # Determinar mejor modelo
        if result['f1_score'] > best_score:
            best_score = result['f1_score']
            best_model = model_name
    
    print(f"\n🏆 MEJOR MODELO: {best_model}")
    print(f"   F1-Score: {best_score:.4f}")
    
    return best_model

def save_models(results, vectorizer, best_model_name):
    """
    Guarda los modelos entrenados y el vectorizador
    """
    print(f"\n💾 PASO 5: Guardando modelos...")
    
    # Crear directorio de modelos si no existe
    MODELS_DIR.mkdir(exist_ok=True)
    print(f"   📁 Directorio de modelos: {MODELS_DIR}")
    
    # Guardar vectorizador
    vectorizer_path = MODELS_DIR / "vectorizer.pkl"
    try:
        joblib.dump(vectorizer, vectorizer_path)
        print(f"   ✅ Vectorizador guardado: {vectorizer_path}")
    except Exception as e:
        print(f"   ❌ Error guardando vectorizador: {e}")
    
    # Guardar mejor modelo
    best_model_path = MODELS_DIR / "toxic_model.pkl"
    try:
        best_pipeline = results[best_model_name]['pipeline']
        joblib.dump(best_pipeline, best_model_path)
        print(f"   ✅ Mejor modelo guardado: {best_model_path}")
    except Exception as e:
        print(f"   ❌ Error guardando modelo: {e}")
    
    # Guardar todos los modelos
    all_models_path = MODELS_DIR / "all_models.pkl"
    try:
        joblib.dump(results, all_models_path)
        print(f"   ✅ Todos los modelos guardados: {all_models_path}")
    except Exception as e:
        print(f"   ❌ Error guardando todos los modelos: {e}")
    
            # Guardar información del mejor modelo
        model_info_path = MODELS_DIR / "model_info.txt"
        try:
            with open(model_info_path, 'w', encoding='utf-8') as f:
                f.write(f"MEJOR MODELO: {best_model_name}\n")
                f.write(f"FECHA DE ENTRENAMIENTO: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"ACCURACY: {results[best_model_name]['accuracy']:.4f}\n")
                f.write(f"F1-SCORE: {results[best_model_name]['f1_score']:.4f}\n")
                f.write(f"TIEMPO DE ENTRENAMIENTO: {results[best_model_name]['training_time']:.2f}s\n")
                f.write(f"TAMAÑO DEL DATASET: {len(df):,} muestras\n")
                f.write(f"CARACTERÍSTICAS TF-IDF: {vectorizer.get_feature_names_out().shape[0]:,}\n")
            print(f"   ✅ Información del modelo guardada: {model_info_path}")
        except Exception as e:
            print(f"   ❌ Error guardando información: {e}")

def test_saved_model():
    """
    Prueba el modelo guardado para verificar que funciona correctamente
    """
    print(f"\n🧪 PASO 6: Probando modelo guardado...")
    
    model_path = MODELS_DIR / "toxic_model.pkl"
    vectorizer_path = MODELS_DIR / "vectorizer.pkl"
    
    if not model_path.exists() or not vectorizer_path.exists():
        print(f"   ❌ Modelo o vectorizador no encontrado")
        return
    
    try:
        # Cargar modelo y vectorizador
        loaded_model = joblib.load(model_path)
        loaded_vectorizer = joblib.load(vectorizer_path)
        
        print(f"   ✅ Modelo y vectorizador cargados exitosamente")
        
        # Textos de prueba
        test_texts = [
            "Hello world! This is a nice comment.",
            "You are an idiot and I hate you!",
            "This is a neutral comment about the weather.",
            "Go to hell you stupid person!"
        ]
        
        print(f"   📝 Probando con {len(test_texts)} textos de ejemplo...")
        
        for i, text in enumerate(test_texts, 1):
            # Preprocesar texto
            processed_text = preprocess_batch([text])[0]
            
            # Predecir
            prediction = loaded_model.predict([processed_text])[0]
            probability = loaded_model.predict_proba([processed_text])[0]
            
            print(f"      {i}. Texto: {text[:50]}{'...' if len(text) > 50 else ''}")
            print(f"         Procesado: {processed_text[:50]}{'...' if len(processed_text) > 50 else ''}")
            print(f"         Predicción: {'Tóxico' if prediction else 'No Tóxico'}")
            print(f"         Probabilidad: {float(probability[prediction]):.3f}")
        
        print(f"   ✅ Modelo funcionando correctamente")
        
    except Exception as e:
        print(f"   ❌ Error probando modelo: {e}")

def main():
    """
    Función principal que ejecuta todo el pipeline de entrenamiento
    """
    print("🚀 ENTRENAMIENTO DE MODELO ML - ToxiGuard")
    print("=" * 70)
    
    try:
        # Paso 1: Cargar y preprocesar dataset
        df, processed_texts = load_and_preprocess_dataset()
        if df is None:
            print("❌ No se pudo cargar el dataset")
            return
        
        # Paso 2: Preparar características y etiquetas
        X_train, X_test, y_train, y_test = prepare_features_and_labels(df)
        
        # Paso 3: Crear y entrenar modelos
        results, vectorizer = create_and_train_models(X_train, X_test, y_train, y_test)
        
        # Paso 4: Evaluar modelos
        best_model_name = evaluate_models(results, y_test, X_test)
        
        # Paso 5: Guardar modelos
        save_models(results, vectorizer, best_model_name)
        
        # Paso 6: Probar modelo guardado
        test_saved_model()
        
        print(f"\n🎉 ¡ENTRENAMIENTO COMPLETADO EXITOSAMENTE!")
        print(f"   Modelo guardado en: {MODELS_DIR}")
        print(f"   Mejor modelo: {best_model_name}")
        print(f"   F1-Score: {results[best_model_name]['f1_score']:.4f}")
        
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
