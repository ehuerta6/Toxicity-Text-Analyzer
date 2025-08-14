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
│   └── main.py              # Punto de entrada de FastAPI
├── .venv/                    # Entorno virtual de Python
├── requirements.txt          # Dependencias de Python
├── .env                      # Variables de entorno
├── .gitignore               # Archivos a ignorar en Git
├── test_server.py            # Script de prueba del servidor
└── README.md                 # Este archivo
```

## 🚀 Endpoints implementados

- `GET /` - Información general de la API
- `GET /health` - Verificación de estado del servicio
- `GET /api/health` - Endpoint alternativo de salud

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Python 3.8+** - Lenguaje principal
- **uvicorn** - Servidor ASGI para desarrollo
- **pydantic** - Validación de datos
- **python-dotenv** - Manejo de variables de entorno
- **requests** - Cliente HTTP para pruebas

## 📋 Configuración completada ✅

1. ✅ Entorno virtual de Python creado (`.venv`)
2. ✅ Dependencias instaladas (`fastapi`, `uvicorn[standard]`, `pydantic`, `python-dotenv`)
3. ✅ Estructura de carpetas y archivos base creada
4. ✅ Endpoints básicos de salud implementados
5. ✅ Configuración de CORS para frontend
6. ✅ Variables de entorno configuradas
7. ✅ Servidor funcionando en puerto 8000

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

# Endpoint raíz
curl http://localhost:8000/

# Usar el script de prueba
python test_server.py
```

## 🌐 URLs de acceso

- **Servidor local:** http://localhost:8000
- **Documentación automática:** http://localhost:8000/docs
- **Documentación alternativa:** http://localhost:8000/redoc

## 📝 Próximos pasos

1. Implementar endpoint `POST /analyze` para análisis de toxicidad
2. Crear modelos Pydantic para validación de datos
3. Integrar modelo ML de toxicidad
4. Añadir base de datos para historial
5. Implementar autenticación y autorización

## 🔧 Variables de entorno

El archivo `.env` contiene:

- `FRONTEND_URL` - URL del frontend para CORS
- `HOST` - Host del servidor
- `PORT` - Puerto del servidor
- `DATABASE_URL` - URL de la base de datos (futuro)
- `MODEL_PATH` - Ruta a los modelos ML (futuro)

---

_Backend configurado y funcionando - Fase 1 completada ✅_
