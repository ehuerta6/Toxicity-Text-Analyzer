# 🤖 Módulo de Machine Learning - ToxiGuard

Este módulo contiene toda la funcionalidad de Machine Learning para ToxiGuard, incluyendo preprocesamiento de texto, vectorización, entrenamiento de modelos y evaluación.

## 🎯 Propósito

El módulo ML se encarga de:

- **Preprocesamiento de texto** usando spaCy
- **Vectorización TF-IDF** para convertir texto a características numéricas
- **Entrenamiento de modelos** de clasificación (Logistic Regression, Naive Bayes, Random Forest)
- **Evaluación y métricas** de rendimiento
- **Guardado y carga** de modelos entrenados

## 🏗 Arquitectura

```
ml/
├── __init__.py              # Inicialización del módulo
├── config.py                # Configuración centralizada
├── preprocessor.py          # Preprocesamiento de texto (futuro)
├── vectorizer.py            # Vectorización TF-IDF (futuro)
├── classifier.py            # Modelos de clasificación (futuro)
├── trainer.py               # Entrenamiento de modelos (futuro)
├── evaluator.py             # Evaluación y métricas (futuro)
├── utils.py                 # Utilidades comunes (futuro)
├── test_spacy.py            # Script de prueba de spaCy
└── README.md                # Este archivo
```

## 🛠 Dependencias instaladas

### ✅ Dependencias principales

- **scikit-learn** - Algoritmos de ML y herramientas
- **pandas** - Manipulación de datos
- **numpy** - Computación numérica
- **spacy** - Procesamiento de lenguaje natural

### ✅ Modelos de spaCy

- **en_core_web_sm** - Modelo en inglés (12.8 MB)

## 🔧 Configuración

### Archivo `config.py`

Contiene toda la configuración centralizada:

- **Rutas** de directorios (ML, datos, modelos)
- **Parámetros** de spaCy y preprocesamiento
- **Configuración** de TF-IDF y modelos
- **Thresholds** de clasificación
- **Métricas** de evaluación

### Variables de entorno

```bash
# Configuración de spaCy
SPACY_MODEL=en_core_web_sm

# Configuración de modelos
RANDOM_STATE=42
TEST_SIZE=0.2
```

## 🚀 Funcionalidades implementadas

### ✅ Completadas

1. **Instalación de dependencias** - Todas las librerías ML instaladas
2. **Modelo spaCy** - en_core_web_sm descargado y funcionando
3. **Estructura de carpetas** - Organización ML lista
4. **Configuración centralizada** - Archivo config.py implementado
5. **Script de prueba** - Verificación de instalación funcionando

### 🔄 Pendientes (Fase 2)

1. **Preprocesador de texto** - Limpieza y normalización
2. **Vectorizador TF-IDF** - Conversión texto → características
3. **Modelos de clasificación** - Logistic Regression, Naive Bayes
4. **Entrenador de modelos** - Pipeline de entrenamiento
5. **Evaluador** - Métricas y validación
6. **Integración con backend** - Reemplazar clasificador naïve

## 🧪 Pruebas

### Verificar instalación

```bash
cd backend
python ml/test_spacy.py
```

### Resultado esperado

```
🎉 ¡Entorno ML configurado correctamente!
   Listo para implementar modelos avanzados
```

## 📊 Casos de uso

### 1. Preprocesamiento de texto

```python
from ml.preprocessor import TextPreprocessor

preprocessor = TextPreprocessor()
clean_text = preprocessor.clean("Hello world! This is a test.")
# Resultado: "hello world test"
```

### 2. Vectorización TF-IDF

```python
from ml.vectorizer import TFIDFVectorizer

vectorizer = TFIDFVectorizer()
features = vectorizer.transform(["texto 1", "texto 2"])
```

### 3. Clasificación de toxicidad

```python
from ml.classifier import ToxicityClassifier

classifier = ToxicityClassifier()
prediction = classifier.predict("You are an idiot!")
# Resultado: {"toxic": True, "score": 0.85, "labels": ["insult"]}
```

## 🔍 Próximos pasos

### Inmediatos

1. **Implementar preprocesador** de texto con spaCy
2. **Crear vectorizador** TF-IDF
3. **Implementar modelos** básicos de clasificación

### Mediano plazo

1. **Entrenar modelos** con dataset Jigsaw
2. **Evaluar rendimiento** y comparar con naïve
3. **Integrar** en el backend existente

### Largo plazo

1. **Fine-tuning** de hiperparámetros
2. **Ensemble methods** para mejor rendimiento
3. **Modelos pre-entrenados** (BERT, DistilBERT)

## 📚 Recursos

### Documentación

- [spaCy Documentation](https://spacy.io/usage)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [pandas Documentation](https://pandas.pydata.org/docs/)

### Datasets

- **Jigsaw Toxic Comments** - Dataset principal para entrenamiento
- **Wikipedia Toxic Comments** - Dataset adicional (opcional)

### Papers y referencias

- "Toxic Comment Classification Challenge" - Kaggle
- "Deep Learning for Toxic Comment Classification" - Papers académicos

---

_Módulo ML configurado y listo para implementación - ToxiGuard Fase 2_
