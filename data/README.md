# Data - ToxiGuard

Esta carpeta está reservada para almacenar los datasets de entrenamiento, validación y pruebas para los modelos de Machine Learning.

## 🎯 Propósito

La carpeta `data/` almacenará:

- Datasets de entrenamiento para clasificación de toxicidad
- Datasets de validación y pruebas
- Datos preprocesados y limpios
- Scripts de limpieza y preparación de datos
- Metadatos y documentación de los datasets

## 📁 Estructura futura

```
data/
├── raw/                       # Datasets originales sin procesar
│   ├── jigsaw_toxic_comments.csv    # Dataset principal de entrenamiento
│   └── additional_datasets/         # Otros datasets complementarios
├── processed/                 # Datos limpios y preprocesados
│   ├── train_processed.csv          # Datos de entrenamiento procesados
│   ├── validation_processed.csv     # Datos de validación procesados
│   └── test_processed.csv           # Datos de prueba procesados
├── scripts/                   # Scripts de procesamiento de datos
│   ├── download_datasets.py         # Descarga automática de datasets
│   ├── clean_data.py                # Limpieza y preprocesamiento
│   ├── split_data.py                # División en train/validation/test
│   └── explore_data.py              # Análisis exploratorio de datos
├── metadata/                  # Información sobre los datasets
│   ├── dataset_info.json            # Descripción y estadísticas
│   ├── schema.json                  # Estructura de columnas
│   └── version_control.md           # Control de versiones de datasets
└── README.md                  # Este archivo
```

## 📊 Datasets principales

### Jigsaw Toxic Comments (Principal)

- **Fuente:** Kaggle - Jigsaw Unintended Bias in Toxicity Classification
- **Tamaño:** ~2M comentarios
- **Columnas:** comment_text, toxic, severe_toxic, obscene, threat, insult, identity_hate
- **Idioma:** Inglés
- **Uso:** Entrenamiento del modelo principal

### Datasets complementarios

- **Hate Speech Detection:** Comentarios de odio en redes sociales
- **Cyberbullying:** Acoso cibernético y bullying online
- **Spam Detection:** Comentarios spam y no deseados

## 🔧 Procesamiento de datos

### Limpieza básica

- Eliminación de caracteres especiales y HTML
- Normalización de espacios y puntuación
- Conversión a minúsculas
- Eliminación de URLs y menciones

### Preprocesamiento avanzado

- Tokenización y lematización
- Eliminación de stopwords
- Normalización de texto
- Balanceo de clases (si es necesario)

### División de datos

- **Train:** 70% - Entrenamiento del modelo
- **Validation:** 15% - Ajuste de hiperparámetros
- **Test:** 15% - Evaluación final

## 📈 Estadísticas de datos

- **Distribución de clases:** Balance entre tóxico/no tóxico
- **Longitud de comentarios:** Estadísticas de longitud de texto
- **Vocabulario:** Tamaño del vocabulario y palabras más frecuentes
- **Calidad:** Porcentaje de datos faltantes o corruptos

## 📋 Próximos pasos

1. Descargar dataset Jigsaw Toxic Comments
2. Implementar scripts de limpieza y preprocesamiento
3. Dividir datos en train/validation/test
4. Realizar análisis exploratorio de datos
5. Preparar datos para entrenamiento del modelo

## ⚠️ Notas importantes

- Los datasets grandes no se incluirán en el repositorio Git
- Usar `.gitignore` para excluir archivos de datos
- Mantener solo scripts y metadatos en el repositorio
- Documentar proceso de descarga y preparación de datos

---

_Reservado para datasets - Fase 2 del proyecto_
