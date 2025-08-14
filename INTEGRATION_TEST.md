# 🧪 Prueba de Integración Frontend ↔ Backend

Este documento contiene las instrucciones para probar la integración completa entre el frontend y backend de ToxiGuard.

## 🚀 Requisitos previos

- Backend funcionando en puerto 8000
- Frontend funcionando en puerto 5173
- Ambos servidores ejecutándose simultáneamente

## 🔧 Iniciar los servidores

### 1. Backend (Terminal 1)

```bash
cd backend
.venv\Scripts\Activate.ps1  # Windows PowerShell
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### 2. Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

## 🌐 URLs de acceso

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Documentación API:** http://localhost:8000/docs

## 🧪 Casos de prueba

### Caso 1: Texto normal (no tóxico)

1. Abre http://localhost:5173
2. Escribe: "Hola, ¿cómo estás? Es un día hermoso."
3. Haz clic en "Analizar"
4. **Resultado esperado:** "NO TÓXICO" con score bajo

### Caso 2: Texto tóxico

1. Escribe: "Eres un idiota estupido!"
2. Haz clic en "Analizar"
3. **Resultado esperado:** "TÓXICO" con score alto y etiqueta "insulto"

### Caso 3: Texto en inglés tóxico

1. Escribe: "You are a stupid idiot and asshole!"
2. Haz clic en "Analizar"
3. **Resultado esperado:** "TÓXICO" con score alto

### Caso 4: Texto vacío

1. Deja el textarea vacío
2. Haz clic en "Analizar"
3. **Resultado esperado:** Mensaje de error "Por favor, ingresa algún texto"

### Caso 5: Error de conexión

1. Detén el backend (Ctrl+C en Terminal 1)
2. Escribe cualquier texto y haz clic en "Analizar"
3. **Resultado esperado:** Mensaje de error de conexión
4. Reinicia el backend y prueba nuevamente

## ✅ Verificaciones

### Frontend

- [ ] Textarea funciona correctamente
- [ ] Botón "Analizar" se habilita/deshabilita según el texto
- [ ] Contador de caracteres funciona
- [ ] Botón "Limpiar" resetea el formulario
- [ ] Estados de carga se muestran correctamente
- [ ] Resultados se visualizan con el diseño correcto
- [ ] Errores se muestran de forma clara

### Backend

- [ ] Endpoint `/health` responde correctamente
- [ ] Endpoint `/analyze` procesa textos correctamente
- [ ] CORS permite peticiones desde el frontend
- [ ] Respuestas incluyen todos los campos requeridos

### Integración

- [ ] Frontend envía peticiones al backend correctamente
- [ ] Backend responde y frontend muestra resultados
- [ ] Manejo de errores funciona en ambos lados
- [ ] Estados de carga se sincronizan correctamente

## 🐛 Solución de problemas

### Backend no responde

```bash
# Verificar que esté corriendo
netstat -ano | findstr :8000

# Reiniciar si es necesario
cd backend
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### Frontend no responde

```bash
# Verificar que esté corriendo
netstat -ano | findstr :5173

# Reiniciar si es necesario
cd frontend
npm run dev
```

### Errores de CORS

- Verificar que `FRONTEND_URL` esté configurado en `.env` del backend
- Reiniciar ambos servidores

### Errores de TypeScript

```bash
cd frontend
npm run build  # Verificar errores de compilación
```

## 📊 Resultados esperados

### Texto normal

```json
{
  "toxic": false,
  "score": 0.0,
  "labels": [],
  "text_length": 45,
  "keywords_found": 0
}
```

### Texto tóxico

```json
{
  "toxic": true,
  "score": 0.75,
  "labels": ["insulto"],
  "text_length": 25,
  "keywords_found": 2
}
```

## 🎉 Éxito

Si todos los casos de prueba pasan correctamente, la integración está funcionando perfectamente y ToxiGuard está listo para uso en producción.

---

_Documento de pruebas de integración - ToxiGuard_
