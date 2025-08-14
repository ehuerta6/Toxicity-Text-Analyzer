# Frontend - ToxiGuard

Esta carpeta contiene la interfaz de usuario de ToxiGuard, construida con React, TypeScript y TailwindCSS.

## 🎯 Propósito

El frontend se encarga de:

- Proporcionar una interfaz intuitiva para ingresar comentarios
- Enviar comentarios al backend para análisis
- Mostrar resultados de toxicidad de forma clara y visual
- Gestionar el estado de la aplicación y la comunicación con el backend

## 🏗 Arquitectura

```
frontend/
├── src/
│   ├── components/           # Componentes reutilizables
│   │   ├── CommentInput/     # Input para comentarios
│   │   ├── ToxicityResult/   # Visualización de resultados
│   │   └── Layout/           # Componentes de estructura
│   ├── services/             # Llamadas a la API del backend
│   ├── types/                # Definiciones de TypeScript
│   ├── utils/                # Utilidades y helpers
│   ├── App.tsx               # Componente principal
│   └── main.tsx              # Punto de entrada
├── public/                   # Archivos estáticos
├── package.json              # Dependencias y scripts
├── tailwind.config.js        # Configuración de TailwindCSS
├── tsconfig.json             # Configuración de TypeScript
└── README.md                 # Este archivo
```

## 🚀 Funcionalidades principales

- **Input de comentarios** - Campo de texto para ingresar contenido
- **Análisis en tiempo real** - Botón para enviar comentarios al backend
- **Visualización de resultados** - Muestra clara de toxicidad y score
- **Diseño responsivo** - Funciona en desktop y móvil
- **Feedback visual** - Indicadores de carga y estados

## 🛠 Tecnologías

- **React 18** - Biblioteca de interfaz de usuario
- **TypeScript** - Tipado estático para mayor robustez
- **Vite** - Build tool rápido y moderno
- **TailwindCSS** - Framework CSS utilitario
- **Axios/Fetch** - Cliente HTTP para comunicación con backend
- **React Hook Form** - Manejo de formularios (opcional)

## 📋 Próximos pasos

1. Inicializar proyecto con Vite + React + TypeScript
2. Configurar TailwindCSS
3. Crear componentes básicos de UI
4. Implementar comunicación con el backend
5. Añadir manejo de estados y errores

---

_Configuración pendiente - Fase 1 del proyecto_
