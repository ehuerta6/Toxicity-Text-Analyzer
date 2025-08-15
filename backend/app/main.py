"""
🚀 ToxiGuard API - Backend Optimizado
API para detección de comentarios tóxicos usando Machine Learning optimizado
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime

from .models import AnalyzeRequest, AnalyzeResponse, ErrorResponse, BatchAnalyzeRequest, BatchAnalyzeResponse
from .improved_classifier import optimized_classifier
from .database import history_db

# Configurar logging optimizado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI optimizada
app = FastAPI(
    title="ToxiGuard API",
    description="API optimizada para detección de comentarios tóxicos",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Variables globales optimizadas
startup_time = None
app_start_time = None

@app.on_event("startup")
async def startup_event():
    """Evento optimizado de inicio de la aplicación"""
    global startup_time, app_start_time
    startup_time = time.time()
    app_start_time = datetime.now()
    
    logger.info("🚀 Iniciando ToxiGuard API optimizada...")
    
    try:
        test_result = optimized_classifier.analyze_text("test")
        logger.info("✅ Clasificador optimizado inicializado correctamente")
    except Exception as e:
        logger.error(f"❌ Error inicializando clasificador: {e}")
        raise
    
    startup_duration = time.time() - startup_time
    logger.info(f"🚀 API optimizada iniciada en {startup_duration:.2f} segundos")

# Configurar CORS optimizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

# Middleware optimizado para medir tiempo de respuesta
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Maneja errores de validación de manera optimizada"""
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
    """Maneja excepciones generales de manera optimizada"""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Error interno del servidor",
            detail="Ocurrió un error inesperado",
            timestamp=datetime.now()
        ).dict()
    )

@app.get("/")
async def root():
    """Endpoint raíz optimizado"""
    return {
        "message": "ToxiGuard API - Backend Optimizado",
        "version": "2.0.0",
        "status": "operational",
        "uptime": time.time() - startup_time if startup_time else 0,
        "start_time": app_start_time.isoformat() if app_start_time else None
    }

@app.get("/health")
async def health_check():
    """Verificación de salud optimizada"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "uptime": time.time() - startup_time if startup_time else 0,
        "classifier": "optimized",
        "database": "connected" if history_db else "disconnected"
    }

@app.get("/info")
async def get_info():
    """Información del sistema optimizada"""
    return {
        "name": "ToxiGuard API",
        "version": "2.0.0",
        "description": "API optimizada para detección de toxicidad",
        "features": [
            "Clasificador optimizado",
            "Análisis contextual mejorado",
            "Rendimiento optimizado",
            "Memoria reducida"
        ],
        "endpoints": [
            "/",
            "/health",
            "/info",
            "/analyze",
            "/batch-analyze",
            "/history",
            "/stats"
        ]
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Análisis optimizado de toxicidad de texto
    
    Args:
        request: Solicitud de análisis
        
    Returns:
        Respuesta con análisis de toxicidad optimizado
    """
    start_time = time.time()
    
    try:
        if not request.text or not request.text.strip():
            raise ValueError("El texto no puede estar vacío")
        
        if len(request.text) > 10000:
            raise ValueError("El texto excede el límite de 10,000 caracteres")
        
        # Análisis optimizado usando el clasificador mejorado
        analysis_result = optimized_classifier.analyze_text(request.text)
        
        # Calcular tiempo de respuesta
        response_time = int((time.time() - start_time) * 1000)
        
        # Crear respuesta optimizada
        response = AnalyzeResponse(
            text=request.text,
            toxicity_percentage=analysis_result["toxicity_percentage"],
            toxicity_level=analysis_result["toxicity_level"],
            confidence=analysis_result["confidence"],
            model_used=analysis_result["model_used"],
            response_time_ms=response_time,
            timestamp=datetime.now(),
            analysis_details=analysis_result.get("details", {})
        )
        
        # Guardar en historial si está habilitado
        if history_db:
            try:
                await history_db.save_analysis(request.text, response.dict())
            except Exception as e:
                logger.warning(f"No se pudo guardar en historial: {e}")
        
        logger.info(f"Análisis completado en {response_time}ms - Toxicidad: {analysis_result['toxicity_percentage']}%")
        return response
        
    except ValueError as e:
        logger.warning(f"Error de validación: {e}")
        raise
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/batch-analyze", response_model=BatchAnalyzeResponse)
async def batch_analyze_texts(request: BatchAnalyzeRequest):
    """
    Análisis en lote optimizado de múltiples textos
    
    Args:
        request: Solicitud de análisis en lote
        
    Returns:
        Respuesta con análisis en lote optimizado
    """
    start_time = time.time()
    
    try:
        if not request.texts or len(request.texts) == 0:
            raise ValueError("La lista de textos no puede estar vacía")
        
        if len(request.texts) > 50:
            raise ValueError("Máximo 50 textos por lote")
        
        results = []
        total_toxicity = 0
        
        for text in request.texts:
            if not text or not text.strip():
                continue
                
            if len(text) > 10000:
                continue
            
            try:
                analysis_result = optimized_classifier.analyze_text(text)
                results.append({
                    "text": text,
                    "toxicity_percentage": analysis_result["toxicity_percentage"],
                    "toxicity_level": analysis_result["toxicity_level"],
                    "confidence": analysis_result["confidence"]
                })
                total_toxicity += analysis_result["toxicity_percentage"]
            except Exception as e:
                logger.warning(f"Error analizando texto: {e}")
                results.append({
                    "text": text,
                    "error": str(e)
                })
        
        if not results:
            raise ValueError("No se pudo analizar ningún texto")
        
        # Calcular estadísticas del lote
        avg_toxicity = total_toxicity / len([r for r in results if "error" not in r])
        response_time = int((time.time() - start_time) * 1000)
        
        response = BatchAnalyzeResponse(
            texts_analyzed=len(results),
            average_toxicity=round(avg_toxicity, 2),
            results=results,
            response_time_ms=response_time,
            timestamp=datetime.now()
        )
        
        logger.info(f"Análisis en lote completado: {len(results)} textos en {response_time}ms")
        return response
        
    except ValueError as e:
        logger.warning(f"Error de validación en lote: {e}")
        raise
    except Exception as e:
        logger.error(f"Error en análisis en lote: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/history")
async def get_analysis_history(limit: int = 100, offset: int = 0):
    """
    Obtener historial de análisis optimizado
    
    Args:
        limit: Límite de resultados (máximo 100)
        offset: Desplazamiento para paginación
        
    Returns:
        Historial de análisis optimizado
    """
    try:
        if not history_db:
            raise HTTPException(status_code=503, detail="Base de datos no disponible")
        
        if limit > 100:
            limit = 100
        
        if offset < 0:
            offset = 0
        
        history = await history_db.get_recent_analyses(limit, offset)
        
        return {
            "total": len(history),
            "limit": limit,
            "offset": offset,
            "analyses": history,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/stats")
async def get_analysis_stats():
    """
    Obtener estadísticas de análisis optimizadas
    
    Returns:
        Estadísticas del sistema optimizadas
    """
    try:
        if not history_db:
            raise HTTPException(status_code=503, detail="Base de datos no disponible")
        
        stats = await history_db.get_statistics()
        
        return {
            "total_analyses": stats.get("total_analyses", 0),
            "average_toxicity": stats.get("average_toxicity", 0),
            "toxicity_distribution": stats.get("toxicity_distribution", {}),
            "model_performance": stats.get("model_performance", {}),
            "last_24h_analyses": stats.get("last_24h_analyses", 0),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.delete("/history")
async def clear_analysis_history():
    """
    Limpiar historial de análisis (solo para desarrollo)
    
    Returns:
        Confirmación de limpieza
    """
    try:
        if not history_db:
            raise HTTPException(status_code=503, detail="Base de datos no disponible")
        
        await history_db.clear_history()
        
        logger.info("Historial de análisis limpiado")
        return {
            "message": "Historial limpiado exitosamente",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error limpiando historial: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
