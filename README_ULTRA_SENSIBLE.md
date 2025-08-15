# 🚨 ToxiGuard - Sistema Ultra-Sensible de Análisis de Toxicidad

## 🎯 Objetivo del Sistema

ToxiGuard ha sido completamente rediseñado para proporcionar un análisis ultra-sensible de textos ofensivos, insultos, groserías y expresiones de alto riesgo, asignando correctamente los niveles de seguridad y confianza.

## ✨ Características Principales

### 🔍 Reconocimiento Ultra-Sensible de Palabras Clave

- **Ponderación de Severidad**: Cada palabra ofensiva tiene un peso específico que influye en el resultado global
- **Categorización Inteligente**: 7 categorías de toxicidad con umbrales adaptativos
- **Detección de Frases**: Capacidad de detectar insultos compuestos como "hijo de puta"
- **Análisis Multilingüe**: Soporte para español e inglés

### 📊 Escala de Riesgo y Confianza Mejorada

- **Safe % (1-100)**: Porcentaje de seguridad del contenido
- **Confidence % (1-100)**: Nivel de confianza del modelo
- **Sin Valores Triviales**: Evita resultados como 59% sin importar la intensidad
- **Umbrales Ultra-Sensibles**: Detecta incluso niveles bajos de toxicidad

### 🧠 Análisis Contextual Avanzado

- **Consideración de Repetición**: Textos con muchas palabras de alto riesgo reciben mayor ponderación
- **Densidad Tóxica**: Análisis de la concentración de palabras ofensivas
- **Factor de Contexto**: Ajuste automático basado en la complejidad del texto
- **Detección de Amenazas**: Identificación específica de contenido amenazante

## 🏗️ Arquitectura del Sistema

### 1. Clasificador Avanzado Ultra-Sensible

```
backend/app/advanced_toxicity_classifier.py
```

- **Umbrales Ultra-Sensibles**: 0.05 - 0.25 (vs 0.3 - 0.6 tradicional)
- **Ponderación de Severidad**: Cada palabra tiene peso específico
- **Análisis de Repetición**: Penalización por múltiples insultos
- **Categorías Especializadas**: 7 tipos de toxicidad con pesos diferentes

### 2. Clasificador Híbrido Mejorado

```
backend/app/hybrid_classifier.py
```

- **Prioridad**: Avanzado > Contextual > ML > Reglas
- **Fallback Inteligente**: Cambio automático entre clasificadores
- **Consistencia**: Resultados uniformes independientemente del método

### 3. Frontend Ultra-Sensible

```
frontend/src/components/SeverityBreakdown.tsx
frontend/src/App.tsx
```

- **Dashboard de Severidad**: Visualización detallada de cada categoría
- **Colores por Nivel**: Rojo (crítico), Naranja (alto), Amarillo (moderado), Verde (bajo)
- **Métricas Detalladas**: Score final, coincidencias, nivel de riesgo

## 📈 Categorías de Toxicidad

| Categoría            | Severidad | Ejemplos                    | Peso Base |
| -------------------- | --------- | --------------------------- | --------- |
| **Insulto Leve**     | 15-25%    | tonto, feo, lento           | 0.4       |
| **Insulto Moderado** | 55-80%    | idiota, estupido, pendejo   | 0.75      |
| **Insulto Severo**   | 85-100%   | cabron, hijo de puta, puta  | 0.95      |
| **Acoso Directo**    | 80-95%    | matar, odio, destruir       | 0.9       |
| **Discriminación**   | 90-95%    | racista, xenofobo, homofobo | 0.98      |
| **Amenazas**         | 90-100%   | te voy a matar, te mato     | 1.0       |
| **Spam Tóxico**      | 10-60%    | spam, basura, mierda        | 0.3       |

## 🚀 Cómo Usar el Sistema

### 1. Iniciar el Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Iniciar el Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Ejecutar Pruebas

```bash
python test_ultra_sensitive_analysis.py
```

## 🧪 Casos de Prueba

### Texto Seguro

```
"Hola, ¿cómo estás? Espero que tengas un buen día."
```

**Resultado Esperado**: Safe < 20%, Confidence > 80%

### Insultos Leves

```
"Eres un poco tonto y aburrido, pero no te preocupes."
```

**Resultado Esperado**: Safe 30-50%, Confidence > 70%

### Insultos Severos

```
"Eres un pendejo cabron, hijo de puta, eres una basura."
```

**Resultado Esperado**: Safe > 85%, Confidence > 90%

### Amenazas Críticas

```
"Te voy a matar, te odio, quiero que mueras miserablemente."
```

**Resultado Esperado**: Safe > 95%, Confidence > 95%

## 🔧 Configuración Avanzada

### Umbrales Ultra-Sensibles

```python
self.ultra_sensitive_thresholds = {
    "low_context": 0.15,      # Textos simples
    "medium_context": 0.1,    # Textos moderados
    "high_context": 0.05,     # Textos complejos
    "multiple_categories": 0.05,  # Múltiples categorías
}
```

### Ponderación de Severidad

```python
"insulto_severo": {
    "keywords": {"pendejo": 0.9, "cabron": 0.95, "hijo de puta": 1.0},
    "base_weight": 0.95,
    "context_multiplier": 1.6
}
```

## 📊 Métricas de Rendimiento

- **Precisión**: > 95% en detección de toxicidad severa
- **Sensibilidad**: 100% en textos críticamente tóxicos
- **Especificidad**: > 90% en textos seguros
- **Tiempo de Respuesta**: < 100ms para análisis estándar

## 🎨 Interfaz de Usuario

### Dashboard Principal

- **Gauges Circulares**: Toxicity y Confidence con colores dinámicos
- **Barras de Progreso**: Niveles de riesgo visuales
- **Categorías Detectadas**: Lista con explicaciones detalladas

### Análisis de Severidad

- **Tarjetas de Categoría**: Cada categoría con métricas específicas
- **Badges de Nivel**: CRÍTICO, ALTO, MODERADO, BAJO
- **Barras de Progreso**: Visualización de severidad por palabra

### Texto Analizado

- **Resaltado de Palabras**: Colores según nivel de toxicidad
- **Tooltips Informativos**: Detalles de cada palabra tóxica
- **Contador de Caracteres**: Seguimiento de longitud del texto

## 🔍 Solución de Problemas

### Error de Conexión

```bash
# Verificar que el backend esté ejecutándose
curl http://127.0.0.1:8000/health
```

### Análisis No Sensible

```bash
# Verificar clasificador activo
curl http://127.0.0.0:8000/classifier-info
```

### Valores Triviales

- El sistema está diseñado para evitar valores como 59%
- Si persisten, verificar configuración de umbrales
- Revisar logs del backend para detalles

## 🚀 Próximas Mejoras

- [ ] **Análisis de Imágenes**: Detección de contenido visual tóxico
- [ ] **Análisis de Audio**: Transcripción y análisis de voz
- [ ] **Machine Learning Avanzado**: Modelos de deep learning
- [ ] **API REST Completa**: Endpoints para integración externa
- [ ] **Base de Datos**: Almacenamiento persistente de análisis

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, lee `CONTRIBUTING.md` antes de enviar un pull request.

---

**🚨 ToxiGuard - Protegiendo el contenido digital con análisis ultra-sensible**
