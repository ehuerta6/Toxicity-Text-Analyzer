# Backend - ToxiGuard

Esta carpeta contiene el servidor backend de ToxiGuard, construido con FastAPI y Python.

## 🎯 Propósito

El backend se encarga de:

- Recibir comentarios del frontend
- Procesar el texto usando modelos de Machine Learning
- Clasificar la toxicidad del comentario
- Devolver resultados estructurados al frontend

## 🏗 Arquitectura

```
backend/
├── app/
│   ├── main.py              # Punto de entrada de FastAPI con endpoints
│   ├── models.py             # Modelos Pydantic para validación
│   └── services.py           # Clasificador de toxicidad
├── .venv/                    # Entorno virtual de Python
├── requirements.txt          # Dependencias de Python
├── .env                      # Variables de entorno
├── .gitignore               # Archivos a ignorar en Git
├── test_server.py            # Script de prueba del servidor
├── test_analyze.py           # Script de prueba del endpoint /analyze
├── quick_test.py             # Prueba rápida del endpoint
└── README.md                 # Este archivo
```

## 🚀 Endpoints implementados

- `GET /` - Información general de la API
- `GET /health` - Verificación de estado del servicio
- `GET /api/health` - Endpoint alternativo de salud
- `POST /analyze` - **NUEVO** Análisis de toxicidad de comentarios
- `GET /keywords` - **NUEVO** Lista de palabras clave tóxicas
- `POST /keywords/add` - **NUEVO** Añadir palabra clave tóxica
- `DELETE /keywords/remove` - **NUEVO** Remover palabra clave tóxica

## 🔍 Endpoint /analyze

### Request

```json
{
  "text": "Texto a analizar para detectar toxicidad"
}
```

### Response

```json
{
  "toxic": true,
  "score": 0.75,
  "labels": ["insulto"],
  "text_length": 45,
  "keywords_found": 2
}
```

### Clasificador naïve implementado

- **Algoritmo:** Búsqueda de palabras clave tóxicas
- **Umbral:** Score ≥ 0.34 se considera tóxico
- **Idiomas:** Español e inglés
- **Categorías:** Insulto (por defecto)
- **Score:** 0.0 a 1.0 basado en cantidad y densidad de palabras tóxicas

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Python 3.8+** - Lenguaje principal
- **uvicorn** - Servidor ASGI para desarrollo
- **pydantic** - Validación de datos
- **python-dotenv** - Manejo de variables de entorno
- **requests** - Cliente HTTP para pruebas

## 📋 Configuración completada ✅

1. ✅ Entorno virtual de Python creado (`.venv`)
2. ✅ Dependencias instaladas (`fastapi`, `uvicorn[standard]`, `pydantic`, `python-dotenv`, `requests`)
3. ✅ Estructura de carpetas y archivos base creada
4. ✅ Endpoints básicos de salud implementados
5. ✅ **NUEVO** Endpoint `/analyze` con clasificador naïve implementado
6. ✅ **NUEVO** Endpoints de gestión de palabras clave
7. ✅ Configuración de CORS para frontend
8. ✅ Variables de entorno configuradas
9. ✅ Servidor funcionando en puerto 8000
10. ✅ Modelos Pydantic para validación de datos

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

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar servidor

```bash
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### 4. Probar endpoints

```bash
# Endpoint de salud
curl http://localhost:8000/health

# Endpoint de análisis (requiere POST con JSON)
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Eres un idiota!"}'

# Usar scripts de prueba
python test_server.py      # Prueba endpoints básicos
python test_analyze.py     # Prueba endpoint /analyze
python quick_test.py       # Prueba rápida
```

## 🌐 URLs de acceso

- **Servidor local:** http://localhost:8000
- **Documentación automática:** http://localhost:8000/docs
- **Documentación alternativa:** http://localhost:8000/redoc

## 📝 Próximos pasos

1. ✅ ~~Implementar endpoint `POST /analyze` para análisis de toxicidad~~ **COMPLETADO**
2. ✅ ~~Crear modelos Pydantic para validación de datos~~ **COMPLETADO**
3. 🔄 Integrar modelo ML avanzado de toxicidad (reemplazar clasificador naïve)
4. 📊 Añadir base de datos para historial de análisis
5. 🔐 Implementar autenticación y autorización
6. 📈 Añadir métricas y estadísticas de uso

## 🔧 Variables de entorno

El archivo `.env` contiene:

- `FRONTEND_URL` - URL del frontend para CORS
- `HOST` - Host del servidor
- `PORT` - Puerto del servidor
- `DATABASE_URL` - URL de la base de datos (futuro)
- `MODEL_PATH` - Ruta a los modelos ML (futuro)

## 🧪 Pruebas

### Prueba rápida del endpoint /analyze

```bash
python quick_test.py
```

### Prueba completa con múltiples casos

```bash
python test_analyze.py
```

### Prueba del servidor básico

```bash
python test_server.py
```

---

_Backend configurado y funcionando con endpoint /analyze - Fase 1 avanzada ✅_
