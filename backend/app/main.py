from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .models import AnalyzeRequest, AnalyzeResponse
from .services import toxicity_classifier

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="ToxiGuard API",
    description="API para detección de comentarios tóxicos usando Machine Learning",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "ToxiGuard API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio"""
    return {"status": "ok"}

@app.get("/api/health")
async def api_health():
    """Endpoint alternativo de salud para la API"""
    return {
        "status": "ok",
        "service": "ToxiGuard Backend",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_toxicity(request: AnalyzeRequest):
    """
    Analiza un texto para detectar toxicidad
    
    - **text**: Texto a analizar (máximo 10,000 caracteres)
    
    Retorna:
    - **toxic**: Boolean indicando si es tóxico
    - **score**: Score de toxicidad de 0.0 a 1.0
    - **labels**: Lista de etiquetas de toxicidad
    - **text_length**: Longitud del texto analizado
    - **keywords_found**: Número de palabras clave encontradas
    """
    try:
        # Analizar el texto usando el clasificador
        is_toxic, score, labels, text_length, keywords_found = toxicity_classifier.analyze_text(
            request.text
        )
        
        return AnalyzeResponse(
            toxic=is_toxic,
            score=round(score, 3),  # Redondear a 3 decimales
            labels=labels,
            text_length=text_length,
            keywords_found=keywords_found
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al analizar el texto: {str(e)}"
        )

@app.get("/keywords")
async def get_keywords():
    """Retorna la lista de palabras clave tóxicas utilizadas por el clasificador"""
    return {
        "keywords": toxicity_classifier.get_keywords_list(),
        "count": len(toxicity_classifier.toxic_keywords),
        "threshold": toxicity_classifier.toxicity_threshold
    }

@app.post("/keywords/add")
async def add_keyword(keyword: str):
    """Añade una nueva palabra clave tóxica al clasificador"""
    if not keyword or not keyword.strip():
        raise HTTPException(
            status_code=400,
            detail="La palabra clave no puede estar vacía"
        )
    
    toxicity_classifier.add_keyword(keyword)
    return {
        "message": f"Palabra clave '{keyword}' añadida exitosamente",
        "total_keywords": len(toxicity_classifier.toxic_keywords)
    }

@app.delete("/keywords/remove")
async def remove_keyword(keyword: str):
    """Remueve una palabra clave tóxica del clasificador"""
    if toxicity_classifier.remove_keyword(keyword):
        return {
            "message": f"Palabra clave '{keyword}' removida exitosamente",
            "total_keywords": len(toxicity_classifier.toxic_keywords)
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Palabra clave '{keyword}' no encontrada"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
