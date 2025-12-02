# 🚀 Guía Rápida de Inicio

## ⚡ Inicio Rápido (3 pasos)

### 1️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar la Aplicación

**Opción A - Usando el script (Windows):**
```bash
start.bat
```

**Opción B - Manualmente:**
```bash
streamlit run app.py
```

### 3️⃣ Abrir en el Navegador

La aplicación se abrirá automáticamente en: `http://localhost:8501`

---

## 🎯 Primeros Pasos en la Aplicación

### 1. Iniciar Sesión
- En el sidebar izquierdo, ingresa tu email y nombre
- Haz clic en "Entrar"
- ¡Listo! Ya puedes usar todas las funcionalidades

### 2. Explorar Ciudades
- Ve a "🌍 Explorar Ciudades"
- Navega por las ciudades disponibles (Madrid, Barcelona, París, Roma)
- Haz clic en "Ver Detalles" para más información

### 3. Ver Puntos de Interés
- Ve a "📍 Puntos de Interés"
- Filtra por ciudad, categoría o dificultad
- Añade lugares a favoritos con el botón ❤️

### 4. Generar Audio-Guías (Requiere n8n)
- Ve a "🎧 Audio-Guías"
- Selecciona ciudad y punto de interés
- Configura idioma y tipo de voz
- Genera tu audio-guía personalizada

### 5. Hacer Reservas
- Ve a "🎫 Mis Reservas"
- Crea una nueva reserva
- Completa fecha, hora y número de personas
- Confirma tu reserva

### 6. Ganar Logros
- Ve a "🎮 Gamificación"
- Realiza actividades para ganar puntos
- Desbloquea logros especiales
- Sube de nivel

---

## 📊 Funcionalidades Disponibles

### ✅ Funciona SIN n8n:
- ✅ Exploración de ciudades
- ✅ Visualización de POIs
- ✅ Sistema de favoritos
- ✅ Gestión de reservas (sin pago)
- ✅ Sistema de gamificación
- ✅ Estadísticas y gráficos
- ✅ Generación de reportes PDF

### 🔧 Requiere n8n:
- 🎧 Generación de audio-guías con IA
- 🤖 Recomendaciones inteligentes
- 💳 Procesamiento de pagos
- 📧 Notificaciones por email
- 🌐 Integración con APIs externas

---

## 🗄️ Datos de Prueba

La aplicación viene con datos de ejemplo:

**Ciudades:**
- 🇪🇸 Madrid, España - €9.99
- 🇪🇸 Barcelona, España - €9.99
- 🇫🇷 París, Francia - €12.99
- 🇮🇹 Roma, Italia - €11.99

**Puntos de Interés:**
- 🏰 Palacio Real (Madrid)
- 🎨 Museo del Prado (Madrid)
- ⛪ Sagrada Familia (Barcelona)
- 🗼 Torre Eiffel (París)

---

## 🎮 Sistema de Puntos y Logros

### Cómo Ganar Puntos:

| Acción | Puntos |
|--------|--------|
| Primera visita | +50 |
| Primera audio-guía | +50 |
| Primera reserva | +100 |
| Dejar una reseña | +25 |
| Visitar 5 POIs | +150 |
| Generar 10 audio-guías | +200 |

### Niveles:
1. 🌱 Explorador Novato (0-500 puntos)
2. 🗺️ Viajero Activo (500-1000 puntos)
3. ⭐ Explorador Experto (1000-2000 puntos)
4. 👑 Maestro Viajero (2000+ puntos)

---

## 📱 Navegación de la App

### Sidebar (Menú Izquierdo):
- 🏠 **Inicio**: Página principal
- 🌍 **Explorar Ciudades**: Catálogo de ciudades
- 📍 **Puntos de Interés**: Lugares turísticos
- 🎧 **Audio-Guías**: Generar guías con IA
- 🎫 **Mis Reservas**: Gestionar reservas
- ⭐ **Favoritos**: Lugares guardados
- 🎮 **Gamificación**: Logros y puntos
- 📊 **Estadísticas**: Análisis de datos
- 📄 **Reportes**: Generar PDFs

---

## 🔧 Configuración Opcional de n8n

Si quieres habilitar las funcionalidades avanzadas:

### 1. Instalar n8n
```bash
npm install -g n8n
```

### 2. Ejecutar n8n
```bash
n8n start
```

### 3. Importar Workflow
1. Abre `http://localhost:5678`
2. Import from File → Selecciona `n8n.json`
3. Configura las credenciales de las APIs

### 4. Actualizar .env
```env
N8N_WEBHOOK_URL=http://localhost:5678/webhook/tourist-guide
```

---

## ❓ Preguntas Frecuentes

### ¿Necesito n8n para usar la app?
No, la aplicación funciona sin n8n. Solo necesitas n8n para funcionalidades avanzadas como audio-guías con IA.

### ¿Los datos son reales?
La aplicación usa datos de ejemplo. Puedes añadir tus propios datos desde Supabase.

### ¿Cómo añado más ciudades?
Puedes añadirlas directamente en Supabase o crear una función de administración.

### ¿Funciona offline?
No, requiere conexión a internet para conectarse a Supabase.

### ¿Puedo cambiar el diseño?
Sí, puedes modificar los archivos `.py` y el CSS en `app.py`.

---

## 🐛 Solución Rápida de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused" (Supabase)
- Verifica tu conexión a internet
- Revisa las credenciales en `.env`

### Error: "n8n webhook not responding"
- Verifica que n8n esté ejecutándose
- La app funciona sin n8n (funcionalidades limitadas)

### La app no se abre en el navegador
- Abre manualmente: `http://localhost:8501`
- Verifica que el puerto 8501 esté libre

---

## 📞 Ayuda Adicional

- 📖 Lee el `README.md` completo
- 🔍 Revisa los comentarios en el código
- 📊 Consulta la documentación de Supabase
- 🤖 Revisa la documentación de n8n

---

**¡Disfruta explorando con tu Guía Turística Virtual! 🌍✨**
