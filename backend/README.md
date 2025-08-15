# Backend - ToxiGuard

Esta carpeta contiene el servidor backend de ToxiGuard, construido con FastAPI y Python, ahora con **análisis contextual avanzado**.

## 🎯 Propósito

El backend se encarga de:

- Recibir comentarios del frontend
- Procesar el texto usando **análisis contextual con embeddings**
- Clasificar la toxicidad considerando el **contexto completo de las frases**
- Devolver resultados estructurados al frontend

## 🧠 Nuevas Funcionalidades - Análisis Contextual

### ✅ Análisis Contextual con Embeddings

- **Detección de negaciones**: "no eres tonto" → baja toxicidad
- **Análisis por oraciones**: Cada oración se analiza independientemente
- **Similitud semántica**: Compara con ejemplos contextuales
- **Modelo ligero**: `all-MiniLM-L6-v2` para rendimiento optimizado

### ✅ Categorías Contextuales

- **Insulto directo**: "eres un idiota" → alta toxicidad
- **Insulto negado**: "no eres tonto" → baja toxicidad
- **Acoso directo**: "te voy a matar" → alta toxicidad
- **Acoso negado**: "no te voy a hacer daño" → baja toxicidad
- **Discriminación directa**: "los negros son inferiores" → alta toxicidad
- **Discriminación negada**: "todos somos iguales" → baja toxicidad

## 🏗 Arquitectura

```
backend/
├── app/
│   ├── main.py                    # Punto de entrada de FastAPI con endpoints
│   ├── models.py                  # Modelos Pydantic para validación
│   ├── services.py                # Clasificador de toxicidad (legacy)
│   ├── contextual_classifier.py   # 🆕 Clasificador contextual con embeddings
│   ├── hybrid_classifier.py       # Clasificador híbrido mejorado
│   ├── improved_classifier.py     # Clasificador optimizado
│   ├── ml_classifier.py           # Clasificador ML
│   └── advanced_preprocessor.py   # Preprocesador avanzado
├── .venv/                         # Entorno virtual de Python
├── requirements.txt               # Dependencias de Python (actualizadas)
├── .env                          # Variables de entorno
├── .gitignore                    # Archivos a ignorar en Git
├── test_contextual_analysis.py   # 🆕 Pruebas del análisis contextual
├── test_server.py                # Script de prueba del servidor
├── test_analyze.py               # Script de prueba del endpoint /analyze
├── quick_test.py                 # Prueba rápida del endpoint
└── README.md                     # Este archivo
```

## 🚀 Endpoints implementados

- `GET /` - Información general de la API
- `GET /health` - Verificación de estado del servicio
- `GET /info` - Información del sistema con capacidades contextuales
- `POST /analyze` - **MEJORADO** Análisis contextual de toxicidad
- `GET /classifier-info` - **MEJORADO** Información del clasificador contextual
- `POST /switch-classifier` - **MEJORADO** Cambiar entre clasificadores
- `POST /batch-analyze` - Análisis en lote
- `GET /history` - Historial de análisis
- `GET /stats` - Estadísticas del sistema

## 🔍 Endpoint /analyze (MEJORADO)

### Request

```json
{
  "text": "No eres tonto, eres muy inteligente"
}
```

### Response (Contextual)

```json
{
  "text": "No eres tonto, eres muy inteligente",
  "is_toxic": false,
  "toxicity_percentage": 15.2,
  "toxicity_category": "safe",
  "confidence": 0.85,
  "detected_categories": ["insulto_negado"],
  "word_count": 6,
  "response_time_ms": 245,
  "timestamp": "2024-01-15T10:30:00",
  "model_used": "contextual_classifier_v1",
  "classification_technique": "Híbrido - Análisis Contextual con Embeddings",
  "explanations": {
    "insulto_negado": "Detectó insulto negado (contexto positivo) (similitud: 78.5%) - El contexto indica que se está negando la toxicidad"
  }
}
```

### Comparación: Análisis Tradicional vs Contextual

| Texto             | Análisis Tradicional | Análisis Contextual |
| ----------------- | -------------------- | ------------------- |
| "Eres un idiota"  | 85% tóxico           | 85% tóxico          |
| "No eres tonto"   | 75% tóxico ❌        | 15% tóxico ✅       |
| "Te voy a matar"  | 90% tóxico           | 90% tóxico          |
| "No te haré daño" | 60% tóxico ❌        | 10% tóxico ✅       |

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Python 3.8+** - Lenguaje principal
- **sentence-transformers** - 🆕 Análisis contextual con embeddings
- **torch** - 🆕 Backend para transformers
- **transformers** - 🆕 Modelos de Hugging Face
- **scikit-learn** - Machine Learning
- **spacy** - Procesamiento de lenguaje natural
- **uvicorn** - Servidor ASGI para desarrollo
- **pydantic** - Validación de datos
- **python-dotenv** - Manejo de variables de entorno
- **requests** - Cliente HTTP para pruebas

## 📋 Configuración completada ✅

1. ✅ Entorno virtual de Python creado (`.venv`)
2. ✅ Dependencias actualizadas con sentence-transformers
3. ✅ Estructura de carpetas y archivos base creada
4. ✅ Endpoints básicos de salud implementados
5. ✅ **MEJORADO** Endpoint `/analyze` con análisis contextual
6. ✅ **NUEVO** Clasificador contextual con embeddings
7. ✅ **MEJORADO** Clasificador híbrido con prioridad contextual
8. ✅ Configuración de CORS para frontend
9. ✅ Variables de entorno configuradas
10. ✅ Servidor funcionando en puerto 8000
11. ✅ Modelos Pydantic para validación de datos
12. ✅ **NUEVO** Script de pruebas contextuales

## 🚀 Cómo ejecutar

### 1. Activar entorno virtual

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

### 2. Instalar dependencias (actualizadas)

```bash
pip install -r requirements.txt
```

### 3. Ejecutar servidor

```bash
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### 4. Probar análisis contextual

```bash
# Prueba específica del análisis contextual
python test_contextual_analysis.py

# Prueba general del servidor
python test_server.py

# Prueba del endpoint /analyze
python test_analyze.py

# Prueba rápida
python quick_test.py
```

## 🌐 URLs de acceso

- **Servidor local:** http://localhost:8000
- **Documentación automática:** http://localhost:8000/docs
- **Documentación alternativa:** http://localhost:8000/redoc

## 🧪 Pruebas del Análisis Contextual

### Ejecutar pruebas específicas

```bash
python test_contextual_analysis.py
```

Este script prueba:

- ✅ Detección de insultos directos
- ✅ Detección de negaciones (contexto positivo)
- ✅ Análisis de acoso directo y negado
- ✅ Análisis de discriminación directa y negada
- ✅ Textos neutrales
- ✅ Textos mixtos

### Casos de prueba incluidos

1. **"Eres un idiota completo"** → Alta toxicidad esperada
2. **"No eres tonto, eres muy inteligente"** → Baja toxicidad por contexto positivo
3. **"Te voy a matar si no haces lo que digo"** → Alta toxicidad por amenaza
4. **"No te voy a hacer daño, solo quiero ayudarte"** → Baja toxicidad por negación
5. **"Los negros son inferiores a los blancos"** → Alta toxicidad por discriminación
6. **"Todos somos iguales, no discrimino a nadie"** → Baja toxicidad por mensaje positivo

## 📝 Próximos pasos

1. ✅ ~~Implementar endpoint `POST /analyze` para análisis de toxicidad~~ **COMPLETADO**
2. ✅ ~~Crear modelos Pydantic para validación de datos~~ **COMPLETADO**
3. ✅ ~~Integrar modelo ML avanzado de toxicidad~~ **COMPLETADO**
4. ✅ ~~Implementar análisis contextual con embeddings~~ **COMPLETADO**
5. 🔄 Optimizar rendimiento del modelo de embeddings
6. 📊 Añadir base de datos para historial de análisis
7. 🔐 Implementar autenticación y autorización
8. 📈 Añadir métricas y estadísticas de uso

## 🔧 Variables de entorno

El archivo `.env` contiene:

- `FRONTEND_URL` - URL del frontend para CORS
- `HOST` - Host del servidor
- `PORT` - Puerto del servidor
- `DATABASE_URL` - URL de la base de datos (futuro)
- `MODEL_PATH` - Ruta a los modelos ML (futuro)

## 🧪 Pruebas

### Prueba del análisis contextual

```bash
python test_contextual_analysis.py
```

### Prueba completa con múltiples casos

```bash
python test_analyze.py
```

### Prueba del servidor básico

```bash
python test_server.py
```

### Prueba rápida

```bash
python quick_test.py
```

## 🎯 Beneficios del Análisis Contextual

### ✅ Precisión Mejorada

- Detecta negaciones y contexto positivo
- Evita falsos positivos en frases como "no eres tonto"
- Análisis semántico en lugar de solo palabras clave

### ✅ Flexibilidad

- Funciona con embeddings o fallback a reglas
- Múltiples clasificadores disponibles
- Fácil cambio entre modos de análisis

### ✅ Rendimiento

- Modelo de embeddings ligero (all-MiniLM-L6-v2)
- Análisis por oraciones para mejor contexto
- Fallback automático si embeddings no están disponibles

---

_Backend configurado y funcionando con análisis contextual avanzado - Fase 2 completada ✅_
