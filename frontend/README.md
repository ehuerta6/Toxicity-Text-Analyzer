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
│   │   └── ToxicityResult.tsx   # Componente de visualización de resultados
│   ├── lib/                  # Utilidades y servicios
│   │   └── api.ts               # Funciones de comunicación con el backend
│   ├── App.tsx               # Componente principal de la aplicación
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
- **✅ Integración con backend** - Comunicación completa implementada
- **✅ Interfaz de usuario** - Textarea, botón de análisis y visualización de resultados
- **✅ Manejo de errores** - Gestión de errores de red y backend
- **✅ Estados de carga** - Indicadores visuales durante el análisis

## 🛠 Tecnologías

- **React 18** - Biblioteca de interfaz de usuario
- **TypeScript** - Tipado estático para mayor robustez
- **Vite** - Build tool rápido y moderno
- **TailwindCSS** - Framework CSS utilitario con componentes personalizados
- **PostCSS** - Procesamiento de CSS
- **Autoprefixer** - Añade prefijos de navegador automáticamente
- **Fetch API** - Comunicación HTTP con el backend

## 📋 Configuración completada ✅

1. ✅ Proyecto inicializado con Vite + React + TypeScript
2. ✅ TailwindCSS instalado y configurado
3. ✅ PostCSS y Autoprefixer configurados
4. ✅ Variables de entorno configuradas (VITE_API_URL)
5. ✅ Servidor de desarrollo funcionando en puerto 5173
6. ✅ **NUEVO** Integración completa con backend implementada
7. ✅ **NUEVO** Interfaz de usuario funcional
8. ✅ **NUEVO** Manejo de estados y errores
9. ✅ Estilos base de TailwindCSS con componentes personalizados
10. ✅ Configuración de TypeScript optimizada

## 🔌 Integración con Backend

### API Functions (`src/lib/api.ts`)

- **`analyze(text: string)`** - Envía texto al backend para análisis
- **`checkBackendHealth()`** - Verifica la salud del backend
- **Tipos TypeScript** - Interfaces para request/response

### Endpoints utilizados

- **`POST /analyze`** - Análisis principal de toxicidad
- **`GET /health`** - Verificación de salud del backend

### Manejo de errores

- Errores de red (conexión fallida)
- Errores del backend (respuestas HTTP no exitosas)
- Validación de entrada (texto vacío)
- Estados de carga durante el análisis

## 🎨 Interfaz de Usuario

### Componente Principal (`src/App.tsx`)

- **Header** - Título y descripción de la aplicación
- **Textarea** - Input para ingresar texto a analizar
- **Botones** - "Analizar" y "Limpiar" con estados deshabilitados
- **Contador de caracteres** - Muestra longitud del texto
- **Estados de carga** - Spinner y texto "Analizando..."

### Componente de Resultados (`src/components/ToxicityResult.tsx`)

- **Estado principal** - Badge "TÓXICO" o "NO TÓXICO"
- **Score visual** - Porcentaje con barra de progreso
- **Detalles** - Longitud del texto y palabras clave encontradas
- **Etiquetas** - Categorías de toxicidad detectadas
- **Estados** - Carga, error y resultados
- **Animaciones** - Transiciones suaves y efectos visuales

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

- **Frontend (desarrollo):** http://localhost:5173
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
3. ✅ ~~Crear componentes básicos de UI~~ **COMPLETADO**
4. ✅ ~~Implementar comunicación con el backend~~ **COMPLETADO**
5. ✅ ~~Añadir manejo de estados y errores~~ **COMPLETADO**
6. 🔄 Implementar diseño responsivo y mejoras de UX
7. 🔄 Añadir historial de análisis
8. 🔄 Implementar autenticación (futuro)

## 🧪 Desarrollo

### Estructura de archivos

- **`src/App.tsx`** - Componente principal con lógica de análisis
- **`src/components/ToxicityResult.tsx`** - Visualización de resultados
- **`src/lib/api.ts`** - Funciones de comunicación con backend
- **`src/index.css`** - Estilos base de TailwindCSS
- **`tailwind.config.js`** - Configuración de TailwindCSS
- **`postcss.config.js`** - Configuración de PostCSS

### Scripts disponibles

- `npm run dev` - Servidor de desarrollo
- `npm run build` - Construir para producción
- `npm run preview` - Previsualizar build
- `npm run lint` - Linting del código

## 🔍 Flujo de la aplicación

1. **Usuario ingresa texto** en el textarea
2. **Hace clic en "Analizar"** para enviar al backend
3. **Frontend muestra estado de carga** con spinner
4. **Backend procesa y responde** con análisis de toxicidad
5. **Frontend muestra resultados** con visualización completa
6. **Manejo de errores** si algo falla en el proceso

---

_Frontend configurado y funcionando con integración completa - Fase 1 completada ✅_
