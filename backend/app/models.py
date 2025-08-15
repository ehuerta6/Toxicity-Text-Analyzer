from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class AnalyzeRequest(BaseModel):
    """Modelo para la solicitud de análisis de toxicidad"""
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=10000,
        description="Texto a analizar para detectar toxicidad"
    )
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('El texto no puede estar vacío')
        if len(v.strip()) > 10000:
            raise ValueError('El texto no puede exceder los 10,000 caracteres')
        return v.strip()

class AnalyzeResponse(BaseModel):
    """Modelo optimizado para la respuesta del análisis de toxicidad"""
    text: str = Field(
        ..., 
        description="Texto original analizado"
    )
    is_toxic: bool = Field(
        ..., 
        description="Indica si el texto es considerado tóxico"
    )
    toxicity_percentage: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Nivel de toxicidad en porcentaje (0-100)"
    )
    toxicity_category: str = Field(
        ...,
        description="Categoría de toxicidad detectada (safe, moderate, high_risk)"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nivel de confianza del análisis (0.0 a 1.0)"
    )
    detected_categories: List[str] = Field(
        default_factory=list,
        description="Lista de categorías de toxicidad detectadas"
    )
    word_count: int = Field(
        ..., 
        description="Número de palabras en el texto analizado"
    )
    response_time_ms: int = Field(
        ...,
        description="Tiempo de respuesta en milisegundos"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp del análisis"
    )
    model_used: str = Field(
        ...,
        description="Tipo de modelo utilizado para el análisis"
    )
    classification_technique: str = Field(
        ...,
        description="Técnica de clasificación utilizada (ej: Naïve Bayes, Random Forest, SVM, etc.)"
    )

class BatchAnalyzeRequest(BaseModel):
    """Modelo para solicitudes de análisis en lote"""
    texts: List[str] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="Lista de textos a analizar (máximo 100)"
    )

class BatchAnalyzeResponse(BaseModel):
    """Modelo para respuestas de análisis en lote"""
    texts_analyzed: int = Field(
        ...,
        description="Número de textos analizados exitosamente"
    )
    average_toxicity: float = Field(
        ...,
        description="Toxicidad promedio de todos los textos analizados"
    )
    results: List[dict] = Field(
        ...,
        description="Lista de resultados de análisis individuales"
    )
    response_time_ms: int = Field(
        ...,
        description="Tiempo total de respuesta en milisegundos"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp del análisis en lote"
    )

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    error: str = Field(..., description="Descripción del error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del error")
    status_code: int = Field(..., description="Código de estado HTTP")

class HealthResponse(BaseModel):
    """Modelo para respuestas de salud del sistema"""
    status: str = Field(..., description="Estado del sistema")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la verificación")
    uptime: float = Field(..., description="Tiempo de actividad en segundos")
    classifier: str = Field(..., description="Estado del clasificador")
    database: str = Field(..., description="Estado de la base de datos")

class InfoResponse(BaseModel):
    """Modelo para información del sistema"""
    name: str = Field(..., description="Nombre del sistema")
    version: str = Field(..., description="Versión del sistema")
    description: str = Field(..., description="Descripción del sistema")
    features: List[str] = Field(..., description="Características disponibles")
    endpoints: List[str] = Field(..., description="Endpoints disponibles")

class HistoryResponse(BaseModel):
    """Modelo para respuestas de historial"""
    history: List[dict] = Field(..., description="Lista de análisis del historial")
    total: int = Field(..., description="Número total de análisis")
    limit: int = Field(..., description="Límite de resultados")
    offset: int = Field(..., description="Desplazamiento para paginación")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la consulta")

class StatsResponse(BaseModel):
    """Modelo para respuestas de estadísticas"""
    total_analyses: int = Field(..., description="Total de análisis realizados")
    average_toxicity: float = Field(..., description="Toxicidad promedio")
    most_common_category: str = Field(..., description="Categoría más común")
    system_uptime: float = Field(..., description="Tiempo de actividad del sistema")
    classifier_status: str = Field(..., description="Estado del clasificador")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de las estadísticas")
