from pydantic import BaseModel, Field
from typing import List

class AnalyzeRequest(BaseModel):
    """Modelo para la solicitud de análisis de toxicidad"""
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=10000,
        description="Texto a analizar para detectar toxicidad"
    )

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
