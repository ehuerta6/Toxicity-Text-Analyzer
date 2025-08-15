"""
🚀 ToxiGuard API - Backend Optimizado con Análisis Contextual
API para detección de comentarios tóxicos usando Machine Learning optimizado y análisis contextual
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from datetime import datetime
from typing import List, Optional
import os

# Importar clasificadores
from .improved_classifier import optimized_classifier
from .ml_classifier import ml_classifier
from .hybrid_classifier import hybrid_classifier
from .contextual_classifier import contextual_classifier
from .models import AnalyzeRequest, AnalyzeResponse, BatchAnalyzeRequest, BatchAnalyzeResponse
from .database import AnalysisHistoryDB

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar FastAPI
app = FastAPI(
    title="ToxiGuard API",
    description="API profesional para detección de toxicidad en texto usando ML avanzado y análisis contextual con embeddings",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar base de datos de historial
history_db = None
try:
    history_db = AnalysisHistoryDB()
    logger.info("✅ Base de datos de historial inicializada")
except Exception as e:
    logger.warning(f"⚠️ No se pudo inicializar la base de datos: {e}")

# Seleccionar clasificador principal (híbrido ultra-sensible por defecto)
primary_classifier = hybrid_classifier
logger.info(f"✅ Clasificador principal: {primary_classifier.__class__.__name__}")

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    logger.info("🚀 ToxiGuard API iniciando con análisis ultra-sensible...")
    
    # Verificar estado de los clasificadores
    classifier_info = primary_classifier.get_classifier_info()
    logger.info(f"📊 Estado de clasificadores: {classifier_info}")
    
    # Verificar disponibilidad del clasificador avanzado
    if hasattr(primary_classifier, 'advanced_classifier'):
        logger.info("✅ Clasificador avanzado ultra-sensible disponible")
        advanced_info = primary_classifier.advanced_classifier.get_classifier_info()
        logger.info(f"🚨 Clasificador avanzado: {advanced_info}")
    
    # Verificar disponibilidad del clasificador contextual
    if contextual_classifier.embedding_model:
        logger.info("✅ Clasificador contextual con embeddings disponible")
    else:
        logger.warning("⚠️ Clasificador contextual no disponible, usando fallback")
    
    logger.info("✅ ToxiGuard API lista para recibir solicitudes")

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
        content={
            "error": "Error de validación",
            "detail": str(exc),
            "timestamp": datetime.now()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones generales de manera optimizada"""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detail": "Ocurrió un error inesperado",
            "timestamp": datetime.now()
        }
    )

@app.get("/")
async def root():
    """Endpoint raíz optimizado con información contextual"""
    return {
        "message": "ToxiGuard API - Backend Optimizado con Análisis Contextual",
        "version": "2.1.0",
        "status": "operational",
        "features": [
            "Análisis contextual con embeddings",
            "Detección de negaciones y contexto",
            "Clasificación híbrida avanzada",
            "Análisis por oraciones"
        ]
    }

@app.get("/classifier-info")
async def get_classifier_info():
    """
    Obtener información del clasificador actual con detalles contextuales
    
    Returns:
        Información detallada del clasificador incluyendo capacidades contextuales
    """
    try:
        info = primary_classifier.get_classifier_info()
        return {
            "classifier_type": primary_classifier.__class__.__name__,
            "info": info,
            "contextual_features": {
                "sentence_analysis": True,
                "embedding_similarity": contextual_classifier.embedding_model is not None,
                "context_awareness": True,
                "negation_detection": True,
                "embedding_model": contextual_classifier.model_name if contextual_classifier.embedding_model else "Not available"
            },
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"Error obteniendo información del clasificador: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/switch-classifier")
async def switch_classifier(classifier_type: str = "contextual"):
    """
    Cambiar entre clasificadores disponibles
    
    Args:
        classifier_type: "contextual", "ml", o "rules"
        
    Returns:
        Confirmación del cambio
    """
    try:
        if hasattr(primary_classifier, 'set_primary_classifier'):
            primary_classifier.set_primary_classifier(classifier_type)
            return {
                "message": f"Clasificador cambiado a: {classifier_type}",
                "current_mode": f"{classifier_type} primary",
                "available_classifiers": ["contextual", "ml", "rules"],
                "timestamp": datetime.now()
            }
        else:
            return {
                "message": "Clasificador actual no soporta cambio de modo",
                "current_mode": "Fixed",
                "timestamp": datetime.now()
            }
    except Exception as e:
        logger.error(f"Error cambiando clasificador: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/health")
async def health_check():
    """Verificación de salud optimizada con estado ultra-sensible"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "classifier": "hybrid_ultra_sensitive",
        "database": "connected" if history_db else "disconnected",
        "advanced_analysis": True,
        "contextual_analysis": contextual_classifier.embedding_model is not None,
        "ultra_sensitive_features": {
            "severity_weighting": True,
            "ultra_sensitive_thresholds": True,
            "repetition_analysis": True
        }
    }

@app.get("/info")
async def get_info():
    """Información del sistema optimizada con capacidades ultra-sensibles"""
    return {
        "name": "ToxiGuard API",
        "version": "2.1.0",
        "description": "API optimizada para detección de toxicidad con análisis ultra-sensible y contextual",
        "features": [
            "Análisis ultra-sensible con ponderación de severidad",
            "Análisis contextual con embeddings",
            "Detección de negaciones (ej: 'no eres tonto')",
            "Clasificador híbrido ultra-sensible avanzado",
            "Análisis por oraciones",
            "Rendimiento optimizado",
            "Memoria reducida",
            "Umbrales ultra-sensibles para evitar valores triviales"
        ],
        "advanced_analysis": {
            "enabled": True,
            "ultra_sensitive": True,
            "severity_weighting": True,
            "capabilities": [
                "Análisis ultra-sensible de palabras ofensivas",
                "Ponderación por severidad de cada palabra",
                "Detección de amenazas y discriminación",
                "Umbrales adaptativos ultra-sensibles",
                "Análisis de repetición y densidad tóxica"
            ]
        },
        "contextual_analysis": {
            "enabled": contextual_classifier.embedding_model is not None,
            "model": contextual_classifier.model_name if contextual_classifier.embedding_model else "Not available",
            "capabilities": [
                "Análisis de contexto completo",
                "Detección de negaciones",
                "Similitud semántica",
                "Análisis por oraciones"
            ]
        },
        "endpoints": [
            "/",
            "/health",
            "/info",
            "/analyze",
            "/batch-analyze",
            "/history",
            "/stats",
            "/classifier-info",
            "/switch-classifier"
        ]
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Análisis optimizado de toxicidad de texto con análisis contextual
    
    Args:
        request: Solicitud de análisis
        
    Returns:
        Respuesta con análisis de toxicidad optimizado y contextual
    """
    start_time = time.time()
    
    try:
        if not request.text or not request.text.strip():
            raise ValueError("El texto no puede estar vacío")
        
        if len(request.text) > 10000:
            raise ValueError("El texto excede el límite de 10,000 caracteres")
        
        # Análisis optimizado usando el clasificador mejorado con contextual
        analysis_result = primary_classifier.analyze_text(request.text)
        
        # Calcular tiempo de respuesta
        response_time = int((time.time() - start_time) * 1000)
        
        # Crear respuesta optimizada
        response = AnalyzeResponse(
            text=request.text,
            is_toxic=analysis_result["is_toxic"],
            toxicity_percentage=analysis_result["toxicity_percentage"],
            toxicity_category=analysis_result["toxicity_level"],  # Mapear toxicity_level a toxicity_category
            confidence=analysis_result["confidence"],
            detected_categories=analysis_result["details"]["detected_categories"],
            word_count=analysis_result["details"]["word_count"],
            response_time_ms=response_time,
            timestamp=datetime.now(),
            model_used=analysis_result["model_used"],
            classification_technique=analysis_result.get("classification_technique", "Técnica no especificada"),
            explanations=analysis_result["details"].get("explanations", {}),
            severity_breakdown=analysis_result["details"].get("severity_breakdown", {}),
            ultra_sensitive_analysis=analysis_result["details"].get("ultra_sensitive_analysis", False)
        )
        
        # Guardar en historial si está habilitado
        if history_db:
            try:
                await history_db.save_analysis(request.text, response.dict())
            except Exception as e:
                logger.warning(f"No se pudo guardar en historial: {e}")
        
        logger.info(f"Análisis contextual completado en {response_time}ms - Toxicidad: {analysis_result['toxicity_percentage']}%")
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
                analysis_result = primary_classifier.analyze_text(text)
                results.append({
                    "text": text,
                    "toxicity_percentage": analysis_result["toxicity_percentage"],
                    "toxicity_level": analysis_result["toxicity_level"],
                    "confidence": analysis_result["confidence"],
                    "is_toxic": analysis_result["is_toxic"],
                    "detected_categories": analysis_result["details"]["detected_categories"],
                    "word_count": analysis_result["details"]["word_count"],
                    "classification_technique": analysis_result.get("classification_technique", "Técnica no especificada"),
                    "explanations": analysis_result["details"].get("explanations", {})
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
