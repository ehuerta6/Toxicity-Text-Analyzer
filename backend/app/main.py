"""
🚀 ToxiGuard API - Backend Principal
API para detección de comentarios tóxicos usando Machine Learning
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar módulos locales
from .models import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from .services import toxicity_classifier
from .database import history_db
from .model import ml_model

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="ToxiGuard API",
    description="API para detección de comentarios tóxicos usando Machine Learning",
    version="1.0.0"
)

# Variables globales
startup_time = None

# ================================
# 🚀 EVENTOS DE INICIO
# ================================

@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    global startup_time
    startup_time = time.time()
    
    logger.info("🚀 Iniciando ToxiGuard API...")
    
    # Cargar modelo ML
    if ml_model.load_model():
        logger.info("✅ Modelo ML cargado exitosamente")
    else:
        logger.warning("⚠️ Modelo ML no disponible, usando clasificador mejorado")
    
    startup_duration = time.time() - startup_time
    logger.info(f"🚀 API iniciada en {startup_duration:.2f} segundos")

# ================================
# 🔧 MIDDLEWARE Y CONFIGURACIÓN
# ================================

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Middleware para medir tiempo de respuesta
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ================================
# 🛡️ MANEJADORES DE EXCEPCIONES
# ================================

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Maneja errores de validación"""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="Error de validación",
            detail=str(exc),
            timestamp=datetime.now()
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja errores generales"""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Error interno del servidor",
            detail="Ocurrió un error inesperado",
            timestamp=datetime.now()
        ).dict()
    )

# ================================
# 🏠 ENDPOINTS PRINCIPALES
# ================================

@app.get("/")
async def root():
    """Endpoint raíz con información básica"""
    return {
        "message": "ToxiGuard API - Detección de Toxicidad",
        "version": "1.0.0",
        "status": "running",
        "uptime": time.time() - startup_time if startup_time else 0,
        "model_loaded": ml_model.is_loaded,
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health",
            "model_status": "/model/status"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de salud del sistema"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": time.time() - startup_time if startup_time else 0,
        "model_status": "loaded" if ml_model.is_loaded else "not_loaded",
        "phase": "production"
    }

@app.get("/api/health")
async def api_health():
    """Endpoint de salud de la API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "phase": "production"
    }

# ================================
# 🤖 ENDPOINTS DE MODELO ML
# ================================

@app.get("/ml/status")
async def ml_model_status():
    """Endpoint para verificar el estado del modelo ML"""
    return ml_model.get_status()

@app.post("/ml/test")
async def test_ml_model(text: str):
    """Endpoint para probar el modelo ML con un texto específico"""
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Texto no puede estar vacío")
    
    try:
        if ml_model.is_loaded:
            is_toxic, score, toxicity_percentage, labels = ml_model.predict(text)
            return {
                "text": text,
                "toxic": is_toxic,
                "score": score,
                "toxicity_percentage": toxicity_percentage,
                "labels": labels,
                "model_used": "ML Model"
            }
        else:
            # Fallback al clasificador mejorado
            is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = toxicity_classifier.analyze_text(text)
            return {
                "text": text,
                "toxic": is_toxic,
                "score": score,
                "toxicity_percentage": toxicity_percentage,
                "labels": labels + ["fallback"],
                "model_used": "Enhanced Classifier"
            }
    except Exception as e:
        logger.error(f"Error en test ML: {e}")
        raise HTTPException(status_code=500, detail=f"Error probando modelo: {str(e)}")

# ================================
# 🔍 ENDPOINT PRINCIPAL DE ANÁLISIS
# ================================

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_toxicity(request: AnalyzeRequest):
    """
    Analiza un texto para detectar toxicidad usando Machine Learning
    
    - **text**: Texto a analizar (máximo 10,000 caracteres)
    
    Retorna:
    - **toxic**: Boolean indicando si es tóxico
    - **score**: Score de toxicidad de 0.0 a 1.0
    - **toxicity_percentage**: Nivel de toxicidad en porcentaje (0-100)
    - **category**: Categoría detectada (insulto, acoso, spam, etc.)
    - **labels**: Lista de etiquetas de toxicidad
    - **text_length**: Longitud del texto analizado
    - **keywords_found**: Número de palabras clave encontradas
    - **response_time_ms**: Tiempo de respuesta en milisegundos
    - **timestamp**: Timestamp del análisis
    - **model_used**: Tipo de modelo utilizado
    """
    start_time = time.time()
    
    try:
        # Validación de entrada
        if not request.text or not request.text.strip():
            raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
        
        if len(request.text) > 10000:
            raise HTTPException(status_code=400, detail="El texto no puede exceder 10,000 caracteres")
        
        # Análisis con modelo ML si está disponible
        if ml_model.is_loaded:
            try:
                is_toxic, score, toxicity_percentage, labels = ml_model.predict(request.text)
                text_length = len(request.text)
                
                # Categorización usando el clasificador mejorado
                _, _, _, _, keywords_found, category, _ = toxicity_classifier.analyze_text(request.text)
                
                model_used = "ML Model"
                
            except Exception as ml_error:
                logger.warning(f"Error en modelo ML, usando fallback: {ml_error}")
                # Fallback al clasificador mejorado
                is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = toxicity_classifier.analyze_text(request.text)
                model_used = "Enhanced Classifier (ML Fallback)"
        else:
            # Usar clasificador mejorado
            is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = toxicity_classifier.analyze_text(request.text)
            model_used = "Enhanced Classifier"
        
        # Calcular tiempo de respuesta
        response_time_ms = round((time.time() - start_time) * 1000, 2)
        
        # Crear respuesta
        response = AnalyzeResponse(
            toxic=is_toxic,
            score=round(score, 3),
            toxicity_percentage=toxicity_percentage,
            category=category,
            labels=labels,
            text_length=text_length,
            keywords_found=keywords_found,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(),
            model_used=model_used
        )
        
        # Guardar en el historial (async para no bloquear)
        try:
            history_db.save_analysis(request.text, response.dict())
        except Exception as e:
            logger.warning(f"Error guardando en historial: {e}")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado en análisis: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor durante el análisis"
        )

# ================================
# 🔑 ENDPOINTS DE PALABRAS CLAVE
# ================================

@app.get("/keywords")
async def get_keywords():
    """Retorna la lista de palabras clave tóxicas utilizadas por el clasificador"""
    return {
        "keywords": toxicity_classifier.get_keywords_list(),
        "count": len(toxicity_classifier.toxic_keywords),
        "threshold": toxicity_classifier.get_toxicity_threshold(),
        "categories": toxicity_classifier.get_categories_info()
    }

@app.post("/keywords/add")
async def add_keyword(keyword: str, category: str = "insulto"):
    """Añade una nueva palabra clave tóxica al clasificador"""
    if not keyword or not keyword.strip():
        raise HTTPException(
            status_code=400,
            detail="La palabra clave no puede estar vacía"
        )
    
    if category not in toxicity_classifier.toxicity_categories:
        raise HTTPException(
            status_code=400,
            detail=f"Categoría '{category}' no válida. Categorías disponibles: {list(toxicity_classifier.toxicity_categories.keys())}"
        )
    
    toxicity_classifier.add_keyword(keyword, category)
    return {
        "message": f"Palabra clave '{keyword}' añadida exitosamente a la categoría '{category}'",
        "total_keywords": len(toxicity_classifier.toxic_keywords),
        "category_keywords": len(toxicity_classifier.toxicity_categories[category])
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

@app.get("/categories")
async def get_categories():
    """Retorna información detallada de todas las categorías de toxicidad"""
    return {
        "categories": toxicity_classifier.get_categories_info(),
        "total_categories": len(toxicity_classifier.toxicity_categories),
        "weights": toxicity_classifier.category_weights
    }

# ================================
# 📚 ENDPOINTS DE HISTORIAL
# ================================

@app.get("/history")
async def get_analysis_history(limit: int = 50, offset: int = 0):
    """Obtiene el historial de análisis"""
    try:
        history = history_db.get_history(limit=limit, offset=offset)
        return {
            "history": history,
            "total": len(history),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo historial: {str(e)}"
        )

@app.get("/history/stats")
async def get_history_statistics():
    """Obtiene estadísticas del historial de análisis"""
    try:
        stats = history_db.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )

@app.get("/history/search")
async def search_analysis_history(q: str, limit: int = 20):
    """Busca en el historial de análisis"""
    if not q or not q.strip():
        raise HTTPException(
            status_code=400,
            detail="El parámetro de búsqueda 'q' no puede estar vacío"
        )
    
    try:
        results = history_db.search_history(q.strip(), limit=limit)
        return {
            "results": results,
            "query": q,
            "total": len(results),
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en búsqueda: {str(e)}"
        )

@app.delete("/history/{analysis_id}")
async def delete_analysis(analysis_id: int):
    """Elimina un análisis específico del historial"""
    try:
        deleted = history_db.delete_analysis(analysis_id)
        if deleted:
            return {"message": f"Análisis {analysis_id} eliminado exitosamente"}
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Análisis {analysis_id} no encontrado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando análisis: {str(e)}"
        )

@app.delete("/history")
async def clear_analysis_history():
    """Limpia todo el historial de análisis"""
    try:
        deleted_count = history_db.clear_history()
        return {
            "message": f"Historial limpiado exitosamente",
            "deleted_analyses": deleted_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error limpiando historial: {str(e)}"
        )

# ================================
# 🔧 ENDPOINTS DE GESTIÓN DEL MODELO
# ================================

@app.get("/model/status")
async def get_model_status():
    """Obtiene el estado del modelo ML"""
    try:
        # Importar aquí para evitar errores de import circular
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from ml.model_manager import ModelManager
        
        manager = ModelManager()
        status = manager.get_model_status()
        
        # Agregar información del estado actual del servidor
        status['server_model_loaded'] = ml_model.is_loaded
        status['server_model_type'] = type(ml_model.model).__name__ if ml_model.model else None
        
        return status
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo estado del modelo: {str(e)}"
        )

@app.post("/model/reload")
async def reload_model():
    """Recarga el modelo ML desde archivos"""
    try:
        success = ml_model.load_model()
        
        if success:
            return {
                "message": "Modelo recargado exitosamente",
                "model_loaded": ml_model.is_loaded,
                "model_type": type(ml_model.model).__name__ if ml_model.model else None
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Error recargando modelo"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error recargando modelo: {str(e)}"
        )

@app.post("/model/backup")
async def create_model_backup():
    """Crea un backup del modelo actual"""
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from ml.model_manager import ModelManager
        
        manager = ModelManager()
        success = manager.backup_current_model()
        
        if success:
            return {
                "message": "Backup creado exitosamente",
                "backup_created": True
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="No se pudo crear el backup"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creando backup: {str(e)}"
        )

@app.get("/model/needs-retrain")
async def check_retrain_needed():
    """Verifica si el modelo necesita reentrenamiento"""
    try:
        import sys
        from pathlib import Path
        sys.path.append(str(Path(__file__).parent.parent))
        from ml.model_manager import ModelManager
        
        manager = ModelManager()
        needs_retrain = manager.needs_retraining()
        age = manager.get_model_age()
        
        return {
            "needs_retraining": needs_retrain,
            "model_age_days": age.days if age else None,
            "recommendation": (
                "Modelo requiere reentrenamiento" if needs_retrain 
                else "Modelo está actualizado"
            )
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verificando reentrenamiento: {str(e)}"
        )

# ================================
# 🚀 INICIO DEL SERVIDOR
# ================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
