# Models - ToxiGuard

Esta carpeta está reservada para almacenar los modelos de Machine Learning entrenados y sus archivos relacionados.

## 🎯 Propósito

La carpeta `models/` almacenará:

- Modelos entrenados de clasificación de toxicidad
- Vectores TF-IDF pre-entrenados
- Archivos de configuración del modelo
- Scripts de entrenamiento y evaluación
- Modelos de diferentes versiones y experimentos

## 📁 Estructura futura

```
models/
├── trained/                   # Modelos entrenados listos para producción
│   ├── toxicity_classifier.pkl    # Modelo principal de clasificación
│   ├── tfidf_vectorizer.pkl       # Vectorizador TF-IDF
│   └── model_metadata.json        # Metadatos del modelo (versión, métricas, etc.)
├── experiments/               # Modelos de experimentos y pruebas
├── scripts/                   # Scripts de entrenamiento y evaluación
│   ├── train_model.py             # Entrenamiento del modelo
│   ├── evaluate_model.py          # Evaluación de rendimiento
│   └── preprocess_data.py         # Preprocesamiento de datos
└── README.md                  # Este archivo
```

## 🤖 Tipos de modelos

### Modelo principal (MVP)

- **Algoritmo:** Logistic Regression o Multinomial Naive Bayes
- **Vectorización:** TF-IDF
- **Entrada:** Texto preprocesado
- **Salida:** Probabilidad de toxicidad (0-1) + clasificación binaria

### Modelos futuros

- **Deep Learning:** BERT, DistilBERT para mejor comprensión semántica
- **Ensemble:** Combinación de múltiples modelos para mayor precisión
- **Multiclass:** Clasificación en subcategorías (insulto, acoso, spam, etc.)

## 📊 Métricas de evaluación

- **Accuracy:** Precisión general del modelo
- **Precision/Recall:** Balance entre falsos positivos y negativos
- **F1-Score:** Media armónica de precisión y recall
- **ROC-AUC:** Área bajo la curva ROC

## 🔄 Pipeline de entrenamiento

1. **Preprocesamiento:** Limpieza, tokenización, lematización
2. **Vectorización:** Conversión de texto a vectores numéricos
3. **Entrenamiento:** Ajuste de hiperparámetros y entrenamiento
4. **Evaluación:** Validación cruzada y métricas de rendimiento
5. **Persistencia:** Guardado del modelo y vectorizador

## 📋 Próximos pasos

1. Preparar dataset de entrenamiento (Jigsaw Toxic Comments)
2. Implementar pipeline de preprocesamiento
3. Entrenar modelo base con Logistic Regression
4. Evaluar rendimiento y ajustar hiperparámetros
5. Guardar modelo entrenado para producción

---

_Reservado para modelos ML - Fase 2 del proyecto_
