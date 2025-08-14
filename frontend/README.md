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
│   ├── components/           # Componentes reutilizables (futuro)
│   ├── services/             # Llamadas a la API del backend (futuro)
│   ├── types/                # Definiciones de TypeScript (futuro)
│   ├── utils/                # Utilidades y helpers (futuro)
│   ├── App.tsx               # Componente principal simplificado
│   ├── main.tsx              # Punto de entrada
│   └── index.css             # Estilos base de TailwindCSS
├── public/                   # Archivos estáticos
├── package.json              # Dependencias y scripts
├── tailwind.config.js        # Configuración de TailwindCSS
├── postcss.config.js         # Configuración de PostCSS
├── tsconfig.json             # Configuración de TypeScript
├── .env                      # Variables de entorno
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos a ignorar en Git
└── README.md                 # Este archivo
```

## 🚀 Funcionalidades implementadas

- **✅ Setup inicial** - Proyecto Vite + React + TypeScript configurado
- **✅ TailwindCSS** - Framework CSS utilitario configurado y funcionando
- **✅ Variables de entorno** - Configuración de API URL
- **✅ Servidor de desarrollo** - Funcionando en puerto 5173
- **✅ Pantalla en blanco** - Lista para implementar componentes

## 🛠 Tecnologías

- **React 18** - Biblioteca de interfaz de usuario
- **TypeScript** - Tipado estático para mayor robustez
- **Vite** - Build tool rápido y moderno
- **TailwindCSS** - Framework CSS utilitario con componentes personalizados
- **PostCSS** - Procesamiento de CSS
- **Autoprefixer** - Añade prefijos de navegador automáticamente

## 📋 Configuración completada ✅

1. ✅ Proyecto inicializado con Vite + React + TypeScript
2. ✅ TailwindCSS instalado y configurado
3. ✅ PostCSS y Autoprefixer configurados
4. ✅ Variables de entorno configuradas (VITE_API_URL)
5. ✅ Servidor de desarrollo funcionando en puerto 5173
6. ✅ Pantalla en blanco lista para implementar componentes
7. ✅ Estilos base de TailwindCSS con componentes personalizados
8. ✅ Configuración de TypeScript optimizada

## 🚀 Cómo ejecutar

### 1. Instalar dependencias

```bash
npm install
```

### 2. Ejecutar servidor de desarrollo

```bash
npm run dev
```

### 3. Construir para producción

```bash
npm run build
```

### 4. Previsualizar build de producción

```bash
npm run preview
```

## 🌐 URLs de acceso

- **Servidor de desarrollo:** http://localhost:5173
- **Backend API:** http://localhost:8000 (configurado en .env)

## 🔧 Variables de entorno

El archivo `.env` contiene:

- `VITE_API_URL` - URL del backend para comunicación
- `VITE_APP_TITLE` - Título de la aplicación
- `VITE_APP_VERSION` - Versión de la aplicación
- `VITE_DEV_MODE` - Modo de desarrollo

## 🎨 Estilos y componentes

### Colores personalizados

- **Primary:** Azules para elementos principales
- **Toxic:** Rojos para contenido tóxico
- **Safe:** Verdes para contenido seguro
- **Neutral:** Grises para elementos neutros

### Componentes CSS personalizados

- **Botones:** `.btn`, `.btn-primary`, `.btn-danger`, `.btn-success`
- **Inputs:** `.input` con estilos consistentes
- **Tarjetas:** `.card` para contenedores
- **Badges:** `.badge-toxic`, `.badge-safe`, `.badge-neutral`

### Animaciones

- **fade-in:** Aparecer gradualmente
- **slide-up:** Deslizar hacia arriba
- **pulse-slow:** Pulsación lenta

## 📝 Próximos pasos

1. ✅ ~~Inicializar proyecto con Vite + React + TypeScript~~ **COMPLETADO**
2. ✅ ~~Configurar TailwindCSS~~ **COMPLETADO**
3. 🔄 Crear componentes básicos de UI:
   - Componente de input para comentarios
   - Componente de visualización de resultados
   - Layout principal de la aplicación
4. 🔄 Implementar comunicación con el backend
5. 🔄 Añadir manejo de estados y errores
6. 🔄 Implementar diseño responsivo

## 🧪 Desarrollo

### Estructura de archivos

- **`src/App.tsx`** - Componente principal (simplificado)
- **`src/index.css`** - Estilos base de TailwindCSS
- **`tailwind.config.js`** - Configuración de TailwindCSS
- **`postcss.config.js`** - Configuración de PostCSS

### Scripts disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Construir para producción
- `npm run preview` - Previsualizar build
- `npm run lint` - Linting del código

---

_Frontend configurado y funcionando - Fase 1 completada ✅_
