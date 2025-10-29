# 🏛️ Guía Turística Virtual

Sistema completo de guía turística virtual con IA, integrado con n8n y Supabase.

## 🚀 Características

- 🎧 **Audio-Guías con IA**: Generación de contenido usando OpenAI + ElevenLabs
- 📍 **Recomendaciones Inteligentes**: Sugerencias personalizadas basadas en ubicación
- 🎫 **Sistema de Reservas**: Integración con Stripe para pagos
- 🎮 **Gamificación**: Sistema de puntos y logros
- 📊 **Estadísticas Avanzadas**: Análisis y visualización de datos
- 📄 **Generación de Reportes**: Exportación a PDF

## 📋 Requisitos Previos

- Python 3.8 o superior
- Cuenta de Supabase (ya configurada)
- n8n instalado y ejecutándose (opcional para funcionalidades avanzadas)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd app-turismo
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
copy .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
# Supabase (YA CONFIGURADO)
SUPABASE_URL=https://eaxnurtyjkkwllodyppb.supabase.co
SUPABASE_KEY=tu_clave_aqui

# n8n Webhook (Configura cuando tengas n8n)
N8N_WEBHOOK_URL=http://localhost:5678/webhook/tourist-guide
```

## 🗄️ Configuración de Base de Datos

Las tablas de Supabase ya están creadas según el schema proporcionado. Si necesitas recrearlas:

1. Ve a tu proyecto en Supabase
2. Abre el SQL Editor
3. Ejecuta el script SQL completo que se encuentra en la documentación

## 🎯 Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
app-turismo/
├── app.py                  # Aplicación principal
├── config.py              # Configuración central
├── database.py            # Módulo de conexión con Supabase
├── n8n_integration.py     # Integración con n8n
├── requirements.txt       # Dependencias Python
├── .env.example          # Ejemplo de variables de entorno
├── n8n.json              # Workflow de n8n
├── pages/                # Páginas de la aplicación
│   ├── __init__.py
│   ├── cities_page.py    # Exploración de ciudades
│   ├── pois_page.py      # Puntos de interés
│   ├── audio_page.py     # Audio-guías
│   ├── bookings_page.py  # Reservas
│   ├── favorites_page.py # Favoritos
│   ├── achievements_page.py # Gamificación
│   ├── stats_page.py     # Estadísticas
│   └── reports_page.py   # Reportes PDF
└── README.md             # Este archivo
```

## 🔌 Configuración de n8n (Opcional)

Para habilitar las funcionalidades avanzadas con n8n:

### 1. Instalar n8n

```bash
npm install -g n8n
```

### 2. Ejecutar n8n

```bash
n8n start
```

### 3. Importar el workflow

1. Abre n8n en `http://localhost:5678`
2. Ve a Workflows > Import from File
3. Selecciona el archivo `n8n.json`
4. Configura las credenciales para:
   - OpenAI
   - ElevenLabs
   - Google Maps
   - Stripe
   - Supabase

### 4. Activar el workflow

Una vez configurado, activa el workflow y copia la URL del webhook.

### 5. Actualizar .env

Actualiza la variable `N8N_WEBHOOK_URL` en tu archivo `.env` con la URL del webhook.

## 🎮 Uso de la Aplicación

### Inicio de Sesión

1. Abre la aplicación
2. En el sidebar, ingresa tu email y nombre
3. Haz clic en "Entrar"

### Explorar Ciudades

1. Ve a "🌍 Explorar Ciudades"
2. Navega por las ciudades disponibles
3. Haz clic en "Ver Detalles" para más información

### Generar Audio-Guías

1. Ve a "🎧 Audio-Guías"
2. Selecciona una ciudad y punto de interés
3. Configura idioma y voz
4. Haz clic en "Generar Audio-Guía"

### Realizar Reservas

1. Ve a "🎫 Mis Reservas"
2. Selecciona "Nueva Reserva"
3. Completa el formulario
4. Confirma la reserva

### Ver Estadísticas

1. Ve a "📊 Estadísticas"
2. Explora las diferentes pestañas:
   - Tendencias generales
   - Popularidad de lugares
   - Tu actividad personal

### Generar Reportes

1. Ve a "📄 Reportes"
2. Selecciona el tipo de reporte
3. Configura las opciones
4. Descarga el PDF

## 🎯 Funcionalidades Principales

### Sin n8n (Modo Básico)
- ✅ Exploración de ciudades y POIs
- ✅ Sistema de favoritos
- ✅ Visualización de estadísticas
- ✅ Generación de reportes PDF
- ✅ Sistema de gamificación
- ✅ Gestión de reservas (sin pago)

### Con n8n (Modo Completo)
- ✅ Todo lo anterior +
- ✅ Generación de audio-guías con IA
- ✅ Recomendaciones inteligentes
- ✅ Procesamiento de pagos con Stripe
- ✅ Notificaciones por email
- ✅ Contenido AR

## 🔑 Datos de Ejemplo

La base de datos incluye datos de ejemplo:

**Ciudades:**
- Madrid, España
- Barcelona, España
- París, Francia
- Roma, Italia

**Puntos de Interés:**
- Palacio Real (Madrid)
- Museo del Prado (Madrid)
- Sagrada Familia (Barcelona)
- Torre Eiffel (París)

## 🐛 Solución de Problemas

### Error de conexión con Supabase

Verifica que:
- Las credenciales en `.env` sean correctas
- Tu proyecto de Supabase esté activo
- Las políticas RLS estén configuradas

### n8n no responde

Verifica que:
- n8n esté ejecutándose
- La URL del webhook sea correcta
- Las credenciales de las APIs estén configuradas

### Error al instalar dependencias

```bash
# Actualiza pip
python -m pip install --upgrade pip

# Instala de nuevo
pip install -r requirements.txt
```

## 📚 Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python
- **Base de Datos**: Supabase (PostgreSQL)
- **Automatización**: n8n
- **IA**: OpenAI GPT-4
- **Text-to-Speech**: ElevenLabs
- **Mapas**: Google Maps API
- **Pagos**: Stripe
- **Visualización**: Plotly
- **PDFs**: FPDF

## 🤝 Contribuir

Este es un proyecto educativo. Siéntete libre de:
- Reportar bugs
- Sugerir mejoras
- Añadir nuevas funcionalidades

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como proyecto de demostración de integración entre Streamlit, n8n y Supabase.

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Verifica los logs de la aplicación
3. Consulta la documentación de Supabase y n8n

---

**¡Disfruta explorando el mundo con tu Guía Turística Virtual! 🌍✨**
