#!/usr/bin/env python3
"""
Preprocesador de texto para ToxiGuard usando spaCy
"""

import re
import spacy
import pandas as pd
from typing import List, Optional, Dict, Any
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar config
sys.path.append(str(Path(__file__).parent.parent))
from ml.config import (
    SPACY_MODEL, 
    SPACY_DISABLE, 
    TEXT_PREPROCESSING,
    MAX_TEXT_LENGTH,
    MIN_TEXT_LENGTH
)

class TextPreprocessor:
    """
    Clase para preprocesar texto usando spaCy
    """
    
    def __init__(self, model_name: str = SPACY_MODEL, disable: List[str] = None):
        """
        Inicializa el preprocesador
        
        Args:
            model_name: Nombre del modelo de spaCy a usar
            disable: Componentes de spaCy a deshabilitar
        """
        self.model_name = model_name
        self.disable = disable or SPACY_DISABLE
        
        print(f"🔧 Inicializando preprocesador de texto...")
        print(f"   📥 Cargando modelo spaCy: {model_name}")
        
        try:
            # Cargar modelo de spaCy
            self.nlp = spacy.load(model_name, disable=self.disable)
            print(f"   ✅ Modelo cargado exitosamente")
            
            # Configurar pipeline
            self._setup_pipeline()
            
        except Exception as e:
            print(f"   ❌ Error cargando modelo: {e}")
            raise
    
    def _setup_pipeline(self):
        """Configura el pipeline de spaCy"""
        print(f"   ⚙️  Configurando pipeline...")
        
        # Verificar componentes disponibles
        available_components = self.nlp.pipe_names
        print(f"   📋 Componentes disponibles: {available_components}")
        
        # Configurar componentes deshabilitados
        if self.disable:
            print(f"   🚫 Componentes deshabilitados: {self.disable}")
        
        print(f"   ✅ Pipeline configurado")
    
    def clean_text(self, text: str, max_length: int = None) -> str:
        """
        Limpia y normaliza un texto
        
        Args:
            text: Texto a limpiar
            max_length: Longitud máxima del texto (opcional)
            
        Returns:
            Texto limpio y normalizado
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Truncar si es muy largo
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        # Aplicar configuración de preprocesamiento
        if TEXT_PREPROCESSING.get("lowercase", True):
            text = text.lower()
        
        if TEXT_PREPROCESSING.get("remove_urls", True):
            text = self._remove_urls(text)
        
        if TEXT_PREPROCESSING.get("remove_emails", True):
            text = self._remove_emails(text)
        
        if TEXT_PREPROCESSING.get("remove_numbers", False):
            text = self._remove_numbers(text)
        
        if TEXT_PREPROCESSING.get("remove_punctuation", True):
            text = self._remove_punctuation(text)
        
        if TEXT_PREPROCESSING.get("remove_extra_whitespace", True):
            text = self._remove_extra_whitespace(text)
        
        return text.strip()
    
    def preprocess_text(self, text: str, return_tokens: bool = False) -> str:
        """
        Preprocesa texto usando spaCy (lematización, stop words, etc.)
        
        Args:
            text: Texto a preprocesar
            return_tokens: Si True, retorna tokens separados por espacio
            
        Returns:
            Texto preprocesado
        """
        if not text:
            return ""
        
        # Limpiar texto básico
        clean_text = self.clean_text(text)
        
        # Procesar con spaCy
        doc = self.nlp(clean_text)
        
        # Aplicar preprocesamiento avanzado
        tokens = []
        for token in doc:
            # Filtrar por longitud mínima
            if len(token.text) < TEXT_PREPROCESSING.get("min_token_length", 2):
                continue
            
            # Filtrar stop words
            if TEXT_PREPROCESSING.get("remove_stopwords", True) and token.is_stop:
                continue
            
            # Aplicar lematización
            if TEXT_PREPROCESSING.get("lemmatize", True):
                token_text = token.lemma_
            else:
                token_text = token.text
            
            # Filtrar tokens vacíos
            if token_text.strip():
                tokens.append(token_text)
        
        if return_tokens:
            return tokens
        
        return " ".join(tokens)
    
    def preprocess_batch(self, texts: List[str], return_tokens: bool = False) -> List[str]:
        """
        Preprocesa una lista de textos en lote
        
        Args:
            texts: Lista de textos a preprocesar
            return_tokens: Si True, retorna listas de tokens
            
        Returns:
            Lista de textos preprocesados
        """
        print(f"🔄 Preprocesando lote de {len(texts)} textos...")
        
        processed_texts = []
        for i, text in enumerate(texts):
            if i % 100 == 0:
                print(f"   📝 Procesando texto {i+1}/{len(texts)}")
            
            processed = self.preprocess_text(text, return_tokens)
            processed_texts.append(processed)
        
        print(f"   ✅ Lote preprocesado exitosamente")
        return processed_texts
    
    def preprocess_dataframe(self, df: pd.DataFrame, text_column: str = "Text", 
                           new_column: str = "ProcessedText") -> pd.DataFrame:
        """
        Preprocesa una columna de texto en un DataFrame
        
        Args:
            df: DataFrame con los datos
            text_column: Nombre de la columna de texto
            new_column: Nombre de la nueva columna procesada
            
        Returns:
            DataFrame con la nueva columna procesada
        """
        print(f"📊 Preprocesando DataFrame...")
        print(f"   📝 Columna de texto: {text_column}")
        print(f"   🆕 Nueva columna: {new_column}")
        
        if text_column not in df.columns:
            raise ValueError(f"Columna '{text_column}' no encontrada en el DataFrame")
        
        # Preprocesar textos en lote
        processed_texts = self.preprocess_batch(df[text_column].tolist())
        
        # Agregar nueva columna
        df[new_column] = processed_texts
        
        print(f"   ✅ DataFrame preprocesado exitosamente")
        return df
    
    def get_text_statistics(self, text: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas del texto procesado
        
        Args:
            text: Texto a analizar
            
        Returns:
            Diccionario con estadísticas
        """
        if not text:
            return {}
        
        doc = self.nlp(text)
        
        # Contar oraciones de forma segura
        try:
            sentence_count = len(list(doc.sents))
        except:
            sentence_count = 1  # Fallback si no hay componente de oraciones
        
        stats = {
            "original_length": len(text),
            "processed_length": len(self.preprocess_text(text)),
            "token_count": len([token for token in doc if not token.is_space]),
            "sentence_count": sentence_count,
            "unique_tokens": len(set([token.text.lower() for token in doc if not token.is_space])),
            "stop_words": len([token for token in doc if token.is_stop]),
            "punctuation_count": len([token for token in doc if token.is_punct]),
            "numbers_count": len([token for token in doc if token.like_num]),
            "urls_count": len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)),
            "emails_count": len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        }
        
        return stats
    
    def _remove_urls(self, text: str) -> str:
        """Elimina URLs del texto"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def _remove_emails(self, text: str) -> str:
        """Elimina emails del texto"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_pattern, '', text)
    
    def _remove_numbers(self, text: str) -> str:
        """Elimina números del texto"""
        return re.sub(r'\d+', '', text)
    
    def _remove_punctuation(self, text: str) -> str:
        """Elimina puntuación del texto"""
        return re.sub(r'[^\w\s]', '', text)
    
    def _remove_extra_whitespace(self, text: str) -> str:
        """Elimina espacios extra del texto"""
        return re.sub(r'\s+', ' ', text)
    
    def test_preprocessing(self, sample_texts: List[str] = None) -> None:
        """
        Prueba el preprocesamiento con textos de ejemplo
        
        Args:
            sample_texts: Lista de textos de prueba (opcional)
        """
        if sample_texts is None:
            sample_texts = [
                "Hello world! This is a test sentence.",
                "Check out this link: https://example.com and email me@test.com",
                "I can't believe this is happening!!!",
                "The quick brown fox jumps over the lazy dog 123."
            ]
        
        print(f"\n🧪 PRUEBA DE PREPROCESAMIENTO")
        print("=" * 60)
        
        for i, text in enumerate(sample_texts, 1):
            print(f"\n📝 Texto {i}:")
            print(f"   Original: {text}")
            
            # Limpiar texto básico
            clean_text = self.clean_text(text)
            print(f"   Limpio: {clean_text}")
            
            # Preprocesar con spaCy
            processed_text = self.preprocess_text(text)
            print(f"   Procesado: {processed_text}")
            
            # Estadísticas
            stats = self.get_text_statistics(text)
            print(f"   Estadísticas: {len(stats)} métricas calculadas")
        
        print(f"\n✅ Prueba de preprocesamiento completada")

def main():
    """Función principal para probar el preprocesador"""
    print("🚀 INICIALIZANDO PREPROCESADOR DE TEXTO - ToxiGuard")
    print("=" * 70)
    
    try:
        # Crear preprocesador
        preprocessor = TextPreprocessor()
        
        # Probar preprocesamiento
        preprocessor.test_preprocessing()
        
        print(f"\n🎉 Preprocesador inicializado correctamente!")
        print(f"   Listo para procesar datasets de comentarios")
        
    except Exception as e:
        print(f"\n❌ Error inicializando preprocesador: {e}")
        print(f"   Verifica que spaCy esté instalado correctamente")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
