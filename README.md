# ToxiGuard – Detecta Comentarios Tóxicos

ToxiGuard es una aplicación web que analiza y clasifica comentarios en tiempo real, detectando contenido tóxico y ofreciendo información útil sobre el nivel de toxicidad. Ideal para moderadores, comunidades online o cualquier aplicación que quiera mantener un ambiente sano.

## 🎯 Objetivo

Construir un MVP funcional que permita:

- Ingresar un comentario en la web
- Clasificarlo como Tóxico o No Tóxico
- Mostrar un score de toxicidad (0-100) y categoría básica
- Servir como base para futuras mejoras y funcionalidades avanzadas

## 🛠 Stack tecnológico

- **Frontend:** React + TypeScript + TailwindCSS (Vite)
- **Backend:** FastAPI (Python) con endpoints REST
- **ML / NLP:** scikit-learn (TF-IDF + Logistic Regression), spaCy para preprocesamiento
- **Base de datos:** SQLite (opcional para MVP)
- **Deploy:** Frontend en Vercel/Netlify, Backend en Render

## 📂 Estructura del proyecto

```
toxiguard/
├── backend/          # FastAPI + modelo ML
├── frontend/         # React + Vite + TypeScript
├── models/           # Modelos entrenados y vectores TF-IDF
├── data/             # Dataset de entrenamiento
├── README.md         # Este archivo
└── ROADMAP.md        # Plan detallado del proyecto
```

## 🚀 Inicio rápido

1. Ver el [ROADMAP.md](./ROADMAP.md) para el plan completo del proyecto
2. Seguir las instrucciones en cada carpeta para configurar el entorno
3. Comenzar con la Fase 1: Setup inicial

## 📚 Documentación

- [ROADMAP.md](./ROADMAP.md) - Plan detallado del proyecto
- [backend/README.md](./backend/README.md) - Configuración del backend
- [frontend/README.md](./frontend/README.md) - Configuración del frontend
- [models/README.md](./models/README.md) - Información sobre modelos ML
- [data/README.md](./data/README.md) - Información sobre datasets

---

_Proyecto en desarrollo - Fase 1: Setup inicial_
