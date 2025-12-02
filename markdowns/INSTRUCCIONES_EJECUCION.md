# 🎯 Instrucciones de Ejecución - Guía Turística Virtual

## ✅ Sistema Completado

Has recibido un sistema completo de Guía Turística Virtual con las siguientes características:

### 📦 Archivos Creados:

#### Archivos Principales:
- ✅ `app.py` - Aplicación principal de Streamlit
- ✅ `config.py` - Configuración central
- ✅ `database.py` - Conexión con Supabase (14KB)
- ✅ `n8n_integration.py` - Integración con n8n (11KB)
- ✅ `requirements.txt` - Dependencias Python

#### Páginas de la Aplicación (8 páginas):
- ✅ `pages/cities_page.py` - Exploración de ciudades
- ✅ `pages/pois_page.py` - Puntos de interés
- ✅ `pages/audio_page.py` - Audio-guías con IA
- ✅ `pages/bookings_page.py` - Sistema de reservas
- ✅ `pages/favorites_page.py` - Favoritos
- ✅ `pages/achievements_page.py` - Gamificación
- ✅ `pages/stats_page.py` - Estadísticas
- ✅ `pages/reports_page.py` - Generación de reportes PDF

#### Configuración:
- ✅ `.env` - Variables de entorno (con tus credenciales de Supabase)
- ✅ `.env.example` - Plantilla de configuración
- ✅ `n8n.json` - Workflow de n8n

#### Documentación:
- ✅ `README.md` - Documentación completa
- ✅ `GUIA_RAPIDA.md` - Guía de inicio rápido
- ✅ `start.bat` - Script de inicio automático

---

## 🚀 PASOS PARA EJECUTAR

### Paso 1: Instalar Dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

**Dependencias que se instalarán:**
- streamlit (Framework web)
- requests (Llamadas HTTP)
- pandas (Manejo de datos)
- plotly (Gráficos interactivos)
- fpdf (Generación de PDFs)
- supabase (Cliente de Supabase)
- python-dotenv (Variables de entorno)
- numpy (Operaciones numéricas)
- Pillow (Manejo de imágenes)

### Paso 2: Ejecutar la Aplicación

**Opción A - Usando el script automático (Recomendado para Windows):**

Simplemente haz doble clic en:
```
start.bat
```

**Opción B - Manualmente:**

```bash
streamlit run app.py
```

### Paso 3: Acceder a la Aplicación

La aplicación se abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

Si no se abre automáticamente, copia y pega esa URL en tu navegador.

---

## 🎮 CÓMO USAR LA APLICACIÓN

### 1️⃣ Iniciar Sesión

Al abrir la aplicación:
1. Verás un formulario de login en el **sidebar izquierdo**
2. Ingresa tu **email** (ej: `usuario@ejemplo.com`)
3. Ingresa tu **nombre** (ej: `Juan Pérez`)
4. Haz clic en **"Entrar"**

El sistema automáticamente:
- Buscará si ya existes en la base de datos
- Si no existes, creará tu cuenta
- Te asignará un ID de usuario
- Guardará tu sesión

### 2️⃣ Explorar Funcionalidades

#### 🏠 Inicio
- Vista general del sistema
- Métricas globales
- Ciudades destacadas

#### 🌍 Explorar Ciudades
- Ver todas las ciudades disponibles
- Filtrar por país
- Ver detalles de cada ciudad
- Ver POIs de cada ciudad

#### 📍 Puntos de Interés
- Explorar lugares turísticos
- Filtrar por ciudad, categoría, dificultad
- Añadir a favoritos ❤️
- Ver detalles completos
- Dejar reseñas y calificaciones

#### 🎧 Audio-Guías
- **Generar Nueva**: Crea audio-guías personalizadas con IA
- **Mis Audio-Guías**: Historial de guías generadas
- Configurar idioma y tipo de voz
- Reproducir audio-guías

#### 🎫 Mis Reservas
- **Nueva Reserva**: Crear reservas para visitas
- **Mis Reservas**: Ver historial de reservas
- Cancelar reservas
- Ver códigos de confirmación

#### ⭐ Favoritos
- Ver lugares guardados
- Filtrar por ciudad o categoría
- Acceso rápido a tus lugares preferidos

#### 🎮 Gamificación
- **Mis Logros**: Logros desbloqueados
- **Logros Disponibles**: Objetivos por completar
- **Estadísticas**: Progreso y ranking
- Sistema de puntos y niveles

#### 📊 Estadísticas
- **Tendencias**: Gráficos de actividad
- **Popularidad**: Lugares más visitados
- **Mi Actividad**: Tu historial personal

#### 📄 Reportes
- Generar reportes en PDF
- Diferentes tipos de reportes
- Personalizar contenido
- Descargar reportes

---

## 🔌 CONEXIÓN CON SUPABASE

### Estado Actual: ✅ CONFIGURADO

Tu aplicación ya está conectada a Supabase con:

```
URL: https://eaxnurtyjkkwllodyppb.supabase.co
```

### Tablas Disponibles:
- ✅ `users` - Usuarios del sistema
- ✅ `cities` - Ciudades disponibles
- ✅ `points_of_interest` - Puntos de interés
- ✅ `user_visits` - Visitas de usuarios
- ✅ `user_achievements` - Logros y gamificación
- ✅ `bookings` - Reservas
- ✅ `usage_stats` - Estadísticas de uso
- ✅ `audio_guides` - Audio-guías generadas
- ✅ `favorites` - Favoritos de usuarios

### Datos de Ejemplo:

La base de datos incluye:
- 4 ciudades (Madrid, Barcelona, París, Roma)
- 4 puntos de interés iniciales
- Estructura completa para todas las funcionalidades

---

## 🤖 INTEGRACIÓN CON n8n (OPCIONAL)

### ¿Qué funciona SIN n8n?

✅ **TODO funciona sin n8n**, excepto:
- Generación real de audio-guías con IA
- Procesamiento de pagos con Stripe
- Envío de emails
- Integración con Google Maps

### ¿Qué hace n8n?

n8n automatiza:
- 🎧 Generación de audio con OpenAI + ElevenLabs
- 💳 Procesamiento de pagos con Stripe
- 📧 Envío de notificaciones
- 🗺️ Búsqueda de lugares con Google Maps
- 🤖 Recomendaciones inteligentes

### Cómo Activar n8n:

1. **Instalar n8n:**
```bash
npm install -g n8n
```

2. **Ejecutar n8n:**
```bash
n8n start
```

3. **Importar workflow:**
- Abre `http://localhost:5678`
- Import from File → `n8n.json`

4. **Configurar APIs:**
- OpenAI API Key
- ElevenLabs API Key
- Google Maps API Key
- Stripe API Key

5. **Actualizar .env:**
```env
N8N_WEBHOOK_URL=http://localhost:5678/webhook/tourist-guide
```

---

## 📊 ESTRUCTURA DE DATOS

### Crear un Usuario:
```python
{
    "email": "usuario@ejemplo.com",
    "name": "Juan Pérez",
    "subscription_tier": "free"
}
```

### Crear una Ciudad:
```python
{
    "name": "Madrid",
    "country": "España",
    "description": "Capital de España",
    "price": 9.99
}
```

### Crear un POI:
```python
{
    "city_id": "uuid-de-ciudad",
    "name": "Palacio Real",
    "description": "Residencia oficial...",
    "latitude": 40.417944,
    "longitude": -3.714347,
    "category": "Histórico",
    "visit_duration": 90,
    "entry_price": 12.00
}
```

---

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### ✅ Completamente Funcionales:

1. **Sistema de Usuarios**
   - Registro automático
   - Login simple
   - Gestión de sesiones
   - Perfiles de usuario

2. **Exploración**
   - Ciudades con filtros
   - POIs con búsqueda
   - Favoritos
   - Detalles completos

3. **Reservas**
   - Crear reservas
   - Ver historial
   - Cancelar reservas
   - Códigos de confirmación

4. **Gamificación**
   - Sistema de puntos
   - Logros automáticos
   - Niveles de usuario
   - Ranking

5. **Estadísticas**
   - Gráficos interactivos
   - Análisis de datos
   - Métricas personales
   - Tendencias

6. **Reportes**
   - Generación de PDFs
   - Múltiples tipos
   - Personalización
   - Descarga directa

### 🔧 Requieren n8n:

1. **Audio-Guías con IA**
   - Generación con OpenAI
   - Conversión a audio con ElevenLabs
   - Múltiples idiomas

2. **Pagos**
   - Procesamiento con Stripe
   - Confirmaciones
   - Reembolsos

3. **Notificaciones**
   - Emails automáticos
   - SMS (opcional)
   - Push notifications

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### Error: Connection to Supabase failed

1. Verifica tu conexión a internet
2. Revisa las credenciales en `.env`
3. Verifica que tu proyecto Supabase esté activo

### La aplicación no inicia

```bash
# Verifica la instalación de Streamlit
streamlit --version

# Reinstala si es necesario
pip install --upgrade streamlit
```

### Puerto 8501 ocupado

```bash
# Usa otro puerto
streamlit run app.py --server.port 8502
```

### Error al generar PDFs

```bash
# Reinstala fpdf
pip install --upgrade fpdf
```

---

## 📈 PRÓXIMOS PASOS

### 1. Añadir Más Datos

Desde Supabase, añade:
- Más ciudades
- Más puntos de interés
- Imágenes reales
- Descripciones detalladas

### 2. Configurar n8n

Para funcionalidades avanzadas:
- Instala n8n
- Configura las APIs
- Activa el workflow

### 3. Personalizar

Modifica:
- Colores y estilos en `app.py`
- Textos y traducciones
- Funcionalidades específicas

### 4. Desplegar

Opciones de deployment:
- Streamlit Cloud (gratis)
- Heroku
- AWS
- Google Cloud

---

## 📞 SOPORTE

Si tienes problemas:

1. **Revisa la documentación:**
   - `README.md`
   - `GUIA_RAPIDA.md`
   - Este archivo

2. **Verifica los logs:**
   - La terminal muestra errores detallados
   - Streamlit muestra warnings en la app

3. **Consulta las documentaciones oficiales:**
   - [Streamlit Docs](https://docs.streamlit.io)
   - [Supabase Docs](https://supabase.com/docs)
   - [n8n Docs](https://docs.n8n.io)

---

## ✨ ¡LISTO PARA USAR!

Tu aplicación está **100% funcional** y lista para usar.

### Comando para iniciar:

```bash
streamlit run app.py
```

### O simplemente:

```bash
start.bat
```

**¡Disfruta tu Guía Turística Virtual! 🌍✨**
