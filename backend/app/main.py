from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import joblib
from pathlib import Path
import sys
import time
from datetime import datetime

# Agregar el directorio padre al path para importar módulos ML
sys.path.append(str(Path(__file__).parent.parent))
from ml.preprocess import preprocess_text

from .models import AnalyzeRequest, AnalyzeResponse, ErrorResponse
from .services import toxicity_classifier
from .database import history_db

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(
    title="ToxiGuard API",
    description="API para detección de comentarios tóxicos usando Machine Learning",
    version="1.0.0"
)

# Variables globales para el modelo ML
ml_model = None
ml_vectorizer = None
model_loaded = False

def load_ml_model():
    """Carga el modelo ML entrenado y el vectorizador"""
    global ml_model, ml_vectorizer, model_loaded
    
    try:
        models_dir = Path(__file__).parent.parent.parent / "models"
        
        # Cargar modelo
        model_path = models_dir / "toxic_model.pkl"
        if model_path.exists():
            ml_model = joblib.load(model_path)
            print(f"✅ Modelo ML cargado exitosamente: {model_path}")
        else:
            print(f"⚠️  Modelo ML no encontrado: {model_path}")
            return False
        
        # Cargar vectorizador
        vectorizer_path = models_dir / "vectorizer.pkl"
        if vectorizer_path.exists():
            ml_vectorizer = joblib.load(vectorizer_path)
            print(f"✅ Vectorizador ML cargado exitosamente: {vectorizer_path}")
        else:
            print(f"⚠️  Vectorizador ML no encontrado: {vectorizer_path}")
            return False
        
        model_loaded = True
        print("🚀 Modelo ML completamente cargado y listo para usar")
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelo ML: {e}")
        model_loaded = False
        ml_model = None
        ml_vectorizer = None
        return False

# Cargar modelo ML al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    print("🚀 Iniciando ToxiGuard API...")
    load_ml_model()

# Configurar CORS - Solo permitir llamadas desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "http://localhost:3000",  # Para desarrollo local
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

# Exception handler personalizado
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error="Error de validación",
            detail=str(exc),
            status_code=400
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Error interno del servidor",
            detail=str(exc),
            status_code=500
        ).dict()
    )

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "ToxiGuard API",
        "version": "1.0.0",
        "status": "running",
        "phase": "3 - Enhanced API"
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
        "phase": "3 - Enhanced API",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/ml/status")
async def ml_model_status():
    """Endpoint para verificar el estado del modelo ML"""
    return {
        "model_loaded": model_loaded,
        "ml_model_available": ml_model is not None,
        "vectorizer_available": ml_vectorizer is not None,
        "status": "ready" if model_loaded else "not_ready",
        "message": "Modelo ML cargado y listo" if model_loaded else "Modelo ML no disponible",
        "fallback_available": True
    }

@app.post("/ml/test")
async def test_ml_model(text: str):
    """Endpoint para probar el modelo ML con un texto específico"""
    if not model_loaded or ml_model is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo ML no disponible"
        )
    
    try:
        # Preprocesar texto
        processed_text = preprocess_text(text)
        
        # Vectorizar y predecir
        prediction = ml_model.predict([processed_text])[0]
        probability = ml_model.predict_proba([processed_text])[0]
        
        return {
            "text": text,
            "processed_text": processed_text,
            "prediction": bool(prediction),
            "prediction_class": "toxic" if prediction else "safe",
            "probabilities": {
                "safe": float(probability[0]),
                "toxic": float(probability[1])
            },
            "confidence": float(probability[int(prediction)]),
            "model_status": "ML Model"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error probando modelo ML: {str(e)}"
        )

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
        # Verificar que el modelo ML esté cargado
        if not model_loaded or ml_model is None:
            # Fallback al clasificador mejorado si el modelo ML no está disponible
            print("⚠️  Modelo ML no disponible, usando clasificador mejorado")
            is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = toxicity_classifier.analyze_text(
                request.text
            )
            model_used = "Enhanced Classifier"
        else:
            # Usar modelo ML para análisis
            print(f"🤖 Analizando texto con modelo ML: {len(request.text)} caracteres")
            
            # Preprocesar texto
            processed_text = preprocess_text(request.text)
            
            # Vectorizar y predecir
            prediction = ml_model.predict([processed_text])[0]
            probability = ml_model.predict_proba([processed_text])[0]
            
            # Obtener resultados
            is_toxic = bool(prediction)
            score = float(probability[int(prediction)])  # Probabilidad de la clase predicha
            text_length = len(request.text)
            toxicity_percentage = round(score * 100, 1)
            
            # Determinar etiquetas basadas en la predicción
            if is_toxic:
                labels = ["toxic", "ml_detected"]
                # Intentar categorizar usando el clasificador mejorado
                _, _, _, _, _, detected_category, _ = toxicity_classifier.analyze_text(request.text)
                category = detected_category
            else:
                labels = ["safe", "ml_detected"]
                category = None
            
            # Contar palabras clave encontradas (para compatibilidad)
            keywords_found = len([word for word in request.text.lower().split() 
                                if word in toxicity_classifier.toxic_keywords])
            
            model_used = "ML Model"
        
        # Calcular tiempo de respuesta
        response_time_ms = round((time.time() - start_time) * 1000, 2)
        
        # Crear respuesta
        response = AnalyzeResponse(
            toxic=is_toxic,
            score=round(score, 3),  # Redondear a 3 decimales
            toxicity_percentage=toxicity_percentage,
            category=category,
            labels=labels,
            text_length=text_length,
            keywords_found=keywords_found,
            response_time_ms=response_time_ms,
            timestamp=datetime.now(),
            model_used=model_used
        )
        
        # Guardar en el historial
        try:
            history_db.save_analysis(request.text, response.dict())
            print(f"💾 Análisis guardado en historial")
        except Exception as e:
            print(f"⚠️ Error guardando en historial: {e}")
        
        return response
        
    except Exception as e:
        print(f"❌ Error en análisis ML: {e}")
        # Fallback al clasificador mejorado en caso de error
        try:
            print("🔄 Intentando fallback al clasificador mejorado...")
            is_toxic, score, labels, text_length, keywords_found, category, toxicity_percentage = toxicity_classifier.analyze_text(
                request.text
            )
            
            response_time_ms = round((time.time() - start_time) * 1000, 2)
            
            # Crear respuesta de fallback
            fallback_response = AnalyzeResponse(
                toxic=is_toxic,
                score=round(score, 3),
                toxicity_percentage=toxicity_percentage,
                category=category,
                labels=labels + ["fallback"],
                text_length=text_length,
                keywords_found=keywords_found,
                response_time_ms=response_time_ms,
                timestamp=datetime.now(),
                model_used="Enhanced Classifier (Fallback)"
            )
            
            # Guardar en el historial
            try:
                history_db.save_analysis(request.text, fallback_response.dict())
                print(f"💾 Análisis de fallback guardado en historial")
            except Exception as e:
                print(f"⚠️ Error guardando fallback en historial: {e}")
            
            return fallback_response
            
        except Exception as fallback_error:
            raise HTTPException(
                status_code=500,
                detail=f"Error en análisis ML y fallback: {str(e)} -> {str(fallback_error)}"
            )

@app.get("/keywords")
async def get_keywords():
    """Retorna la lista de palabras clave tóxicas utilizadas por el clasificador"""
    return {
        "keywords": toxicity_classifier.get_keywords_list(),
        "count": len(toxicity_classifier.toxic_keywords),
        "threshold": toxicity_classifier.toxicity_threshold,
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
