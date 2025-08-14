from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import joblib
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar módulos ML
sys.path.append(str(Path(__file__).parent.parent))
from ml.preprocess import preprocess_text

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

@app.get("/ml/status")
async def ml_model_status():
    """Endpoint para verificar el estado del modelo ML"""
    return {
        "model_loaded": model_loaded,
        "ml_model_available": ml_model is not None,
        "vectorizer_available": ml_vectorizer is not None,
        "status": "ready" if model_loaded else "not_ready",
        "message": "Modelo ML cargado y listo" if model_loaded else "Modelo ML no disponible"
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
    - **labels**: Lista de etiquetas de toxicidad
    - **text_length**: Longitud del texto analizado
    - **keywords_found**: Número de palabras clave encontradas
    """
    try:
        # Verificar que el modelo ML esté cargado
        if not model_loaded or ml_model is None:
            # Fallback al clasificador naïve si el modelo ML no está disponible
            print("⚠️  Modelo ML no disponible, usando clasificador naïve")
            is_toxic, score, labels, text_length, keywords_found = toxicity_classifier.analyze_text(
                request.text
            )
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
            
            # Determinar etiquetas basadas en la predicción
            if is_toxic:
                labels = ["toxic", "ml_detected"]
            else:
                labels = ["safe", "ml_detected"]
            
            # Contar palabras clave encontradas (para compatibilidad)
            keywords_found = len([word for word in request.text.lower().split() 
                                if word in toxicity_classifier.toxic_keywords])
        
        return AnalyzeResponse(
            toxic=is_toxic,
            score=round(score, 3),  # Redondear a 3 decimales
            labels=labels,
            text_length=text_length,
            keywords_found=keywords_found
        )
        
    except Exception as e:
        print(f"❌ Error en análisis ML: {e}")
        # Fallback al clasificador naïve en caso de error
        try:
            print("🔄 Intentando fallback al clasificador naïve...")
            is_toxic, score, labels, text_length, keywords_found = toxicity_classifier.analyze_text(
                request.text
            )
            
            return AnalyzeResponse(
                toxic=is_toxic,
                score=round(score, 3),
                labels=labels + ["fallback"],
                text_length=text_length,
                keywords_found=keywords_found
            )
            
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
