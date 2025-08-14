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
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── models/              # Modelos Pydantic para validación
│   ├── services/            # Lógica de negocio y ML
│   └── utils/               # Utilidades y helpers
├── requirements.txt          # Dependencias de Python
├── .env.example             # Variables de entorno de ejemplo
└── README.md                # Este archivo
```

## 🚀 Endpoints principales

- `GET /health` - Verificación de estado del servicio
- `POST /analyze` - Análisis de toxicidad de comentarios
- `GET /history` - Historial de comentarios analizados (futuro)

## 🛠 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Python 3.8+** - Lenguaje principal
- **scikit-learn** - Modelos de Machine Learning
- **spaCy** - Procesamiento de lenguaje natural
- **Pydantic** - Validación de datos
- **SQLite/PostgreSQL** - Base de datos (opcional para MVP)

## 📋 Próximos pasos

1. Configurar entorno virtual de Python
2. Instalar dependencias con `pip install -r requirements.txt`
3. Crear estructura de carpetas y archivos base
4. Implementar endpoints básicos de salud y análisis
5. Integrar modelo ML de toxicidad

---

_Configuración pendiente - Fase 1 del proyecto_
