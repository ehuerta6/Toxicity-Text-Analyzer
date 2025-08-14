"""
Configuración para el módulo de Machine Learning de ToxiGuard
"""

import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).parent.parent
ML_DIR = BASE_DIR / "ml"
DATA_DIR = BASE_DIR.parent / "data"
MODELS_DIR = BASE_DIR.parent / "models"

# Crear directorios si no existen
ML_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Configuración de spaCy
SPACY_MODEL = "en_core_web_sm"
SPACY_DISABLE = ["ner", "parser"]  # Deshabilitar componentes no necesarios para toxicidad

# Configuración de preprocesamiento
MAX_TEXT_LENGTH = 10000  # Longitud máxima de texto a procesar
MIN_TEXT_LENGTH = 1      # Longitud mínima de texto a procesar

# Configuración de vectorización TF-IDF
TFIDF_MAX_FEATURES = 10000
TFIDF_MIN_DF = 2        # Document frequency mínima
TFIDF_MAX_DF = 0.95     # Document frequency máxima

# Configuración de entrenamiento
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.1

# Configuración de modelos
MODEL_TYPES = {
    "logistic_regression": {
        "C": 1.0,
        "max_iter": 1000,
        "random_state": RANDOM_STATE
    },
    "naive_bayes": {
        "alpha": 1.0
    },
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": RANDOM_STATE
    }
}

# Configuración de evaluación
EVALUATION_METRICS = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc"
]

# Configuración de guardado
MODEL_EXTENSIONS = {
    "sklearn": ".pkl",
    "vectorizer": ".pkl",
    "preprocessor": ".pkl"
}

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de cache
CACHE_DIR = ML_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# Configuración de datasets
DATASET_CONFIGS = {
    "jigsaw_toxic_comments": {
        "url": "https://www.kaggle.com/datasets/julian3833/jigsaw-toxic-comment-classification-challenge",
        "filename": "jigsaw_toxic_comments.csv",
        "columns": {
            "text": "comment_text",
            "labels": ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
        }
    }
}

# Configuración de preprocesamiento de texto
TEXT_PREPROCESSING = {
    "lowercase": True,
    "remove_punctuation": True,
    "remove_numbers": False,
    "remove_urls": True,
    "remove_emails": True,
    "remove_extra_whitespace": True,
    "lemmatize": True,
    "remove_stopwords": True,
    "min_token_length": 2
}

# Configuración de características adicionales
FEATURE_ENGINEERING = {
    "text_length": True,
    "word_count": True,
    "avg_word_length": True,
    "capitalization_ratio": True,
    "punctuation_ratio": True,
    "exclamation_count": True,
    "question_count": True,
    "uppercase_count": True
}

# Configuración de threshold para clasificación
CLASSIFICATION_THRESHOLDS = {
    "default": 0.5,
    "toxic": 0.34,      # Threshold actual del clasificador naïve
    "severe_toxic": 0.7,
    "obscene": 0.5,
    "threat": 0.6,
    "insult": 0.5,
    "identity_hate": 0.6
}
