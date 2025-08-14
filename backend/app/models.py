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
    """Modelo para la respuesta del análisis de toxicidad"""
    toxic: bool = Field(
        ..., 
        description="Indica si el texto es considerado tóxico"
    )
    score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Score de toxicidad de 0.0 a 1.0"
    )
    toxicity_percentage: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Nivel de toxicidad en porcentaje (0-100)"
    )
    category: Optional[str] = Field(
        None,
        description="Categoría de toxicidad detectada (insulto, acoso, spam, etc.)"
    )
    labels: List[str] = Field(
        ..., 
        description="Lista de etiquetas de toxicidad detectadas"
    )
    text_length: int = Field(
        ..., 
        description="Longitud del texto analizado"
    )
    keywords_found: int = Field(
        ..., 
        description="Número de palabras clave tóxicas encontradas"
    )
    response_time_ms: float = Field(
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

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    error: str = Field(..., description="Descripción del error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del error")
    status_code: int = Field(..., description="Código de estado HTTP")
