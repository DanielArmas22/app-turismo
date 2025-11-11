"""
Configuración central de la aplicación
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tciaojtfllfqroanvcuz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRjaWFvanRmbGxmcXJvYW52Y3V6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NjM3MjcsImV4cCI6MjA3NzMzOTcyN30.L4X57t6EUw8zXswAtMJniyY3A2MFCHvB1ClRKQf6XpE")

# Configuración de n8n
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://n8n.yamboly.lat/webhook/tourist-guide")

# Configuración de la aplicación
APP_TITLE = "🏛️ Guía Turística Virtual"
APP_ICON = "🏛️"
APP_LAYOUT = "wide"

# Configuración de idiomas
LANGUAGES = {
    "es": "Español",
    "en": "English",
    "fr": "Français",
    "it": "Italiano"
}

# Configuración de suscripciones
SUBSCRIPTION_TIERS = {
    "free": {
        "name": "Gratuito",
        "price": 0,
        "features": ["Acceso básico", "1 ciudad", "Audio-guías limitadas"]
    },
    "basic": {
        "name": "Básico",
        "price": 9.99,
        "features": ["5 ciudades", "Audio-guías ilimitadas", "Sin anuncios"]
    },
    "premium": {
        "name": "Premium",
        "price": 19.99,
        "features": ["Todas las ciudades", "Contenido AR", "Soporte prioritario"]
    },
    "enterprise": {
        "name": "Empresarial",
        "price": 49.99,
        "features": ["Todo incluido", "API access", "Personalización"]
    }
}

# Categorías de POIs
POI_CATEGORIES = [
    "Histórico",
    "Cultural",
    "Arquitectónico",
    "Gastronómico",
    "Natural",
    "Iconico",
    "Religioso",
    "Moderno"
]

# Niveles de dificultad
DIFFICULTY_LEVELS = ["Fácil", "Moderado", "Difícil"]

# Estados de reserva
BOOKING_STATUSES = {
    "pending": "Pendiente",
    "confirmed": "Confirmada",
    "cancelled": "Cancelada",
    "completed": "Completada",
    "refunded": "Reembolsada"
}

# Tipos de logros
ACHIEVEMENT_TYPES = {
    "visitas": "Visitas",
    "explorador": "Explorador",
    "coleccionista": "Coleccionista",
    "social": "Social",
    "experto": "Experto",
    "especial": "Especial"
}

# Voces disponibles para audio-guías (n8n / ElevenLabs)
AUDIO_VOICES = {
    "Alloy": "alloy",
    "Echo": "echo",
    "Fable": "fable",
    "Nova": "nova",
    "Onyx": "onyx",
    "Shimmer": "shimmer",
}