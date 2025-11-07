"""
Módulo de integración con n8n
"""
import requests
from typing import Dict, Optional, Any
import streamlit as st
from datetime import datetime
import config

class N8NIntegration:
    """Clase para manejar todas las integraciones con n8n"""
    
    def __init__(self):
        """Inicializa la integración con n8n"""
        # Asegurar que la URL no tenga -test
        webhook_url = config.N8N_WEBHOOK_URL
        if webhook_url and "-test" in webhook_url:
            webhook_url = webhook_url.replace("-test", "")
        self.webhook_url = webhook_url
    
    def _call_webhook(self, action_type: str, data: Dict) -> Optional[Dict]:
        """
        Método privado para llamar al webhook de n8n
        
        Args:
            action_type: Tipo de acción a ejecutar
            data: Datos a enviar al webhook
            
        Returns:
            Respuesta del webhook o None si hay error
        """
        now = datetime.now()
        payload = {
            "action_type": action_type,
            "timestamp": now.isoformat() if now else None,
            **data
        }
        
        try:
            # Timeout muy alto para permitir procesamiento de audio (sin límite práctico)
            # El servidor puede tardar varios minutos en generar el audio
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=None,  # Sin timeout - espera indefinidamente
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            
            # Verificar el Content-Type de la respuesta
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Si la respuesta es un archivo de audio
            if 'audio' in content_type or response.headers.get('Content-Type', '').startswith('audio/'):
                # Es un archivo de audio binario
                audio_data = response.content
                audio_size = len(audio_data)
                
                # Guardar el audio en un archivo temporal o usar directamente
                import tempfile
                import os
                
                # Crear un archivo temporal
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(audio_data)
                    tmp_file_path = tmp_file.name
                
                # Retornar información del audio
                result = {
                    'audio_url': tmp_file_path,  # Ruta del archivo temporal
                    'audio_data': audio_data,  # Datos binarios del audio
                    'audio_size': audio_size,
                    'content_type': content_type,
                    'is_binary': True
                }
                
                return result
            
            # Intentar parsear como JSON
            try:
                result = response.json()
                return result
            except ValueError as json_error:
                st.error(f"❌ Error al parsear respuesta: {str(json_error)}")
                return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Tiempo de espera agotado. El servicio está tardando demasiado.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 No se pudo conectar con el servicio n8n. Verifica que esté ejecutándose.")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ Error HTTP {e.response.status_code}")
            return None
        except Exception as e:
            st.error(f"❌ Error al conectar con n8n: {str(e)}")
            return None
    
    # ==================== AUDIO-GUÍAS ====================
    
    def generate_audio_guide(self, poi_id: str, poi_name: str, 
                           poi_description: str = "", 
                           user_id: str = "anonymous",
                           voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Optional[Dict]:
        """
        Obtiene una audio-guía para un punto de interés usando el endpoint de n8n
        
        Args:
            poi_id: ID del punto de interés
            poi_name: Nombre del POI
            poi_description: Descripción del POI
            user_id: ID del usuario
            voice_id: ID de la voz de ElevenLabs (default: "21m00Tcm4TlvDq8ikWAM")
            
        Returns:
            Diccionario con la URL del audio, transcripción y metadatos
        """
        data = {
            "user_id": user_id,
            "poi_id": poi_id,
            "poi_name": poi_name,
            "poi_description": poi_description,
            "voice_id": voice_id
        }
        
        return self._call_webhook("get_audio_guide", data)
    
    # ==================== RECOMENDACIONES ====================
    
    def get_poi_recommendations(self, city_id: str, 
                               user_id: str = "anonymous",
                               lat: float = None,
                               lng: float = None,
                               preferences: Optional[Dict] = None) -> Optional[Dict]:
        """
        Obtiene recomendaciones de POIs usando Google Maps + Supabase
        
        Args:
            city_id: ID de la ciudad
            user_id: ID del usuario
            lat: Latitud de la ubicación
            lng: Longitud de la ubicación
            preferences: Preferencias del usuario (categorías, duración, etc.)
            
        Returns:
            Lista de POIs recomendados
        """
        data = {
            "city_id": city_id,
            "user_id": user_id
        }
        
        # Añadir coordenadas si están disponibles
        if lat is not None:
            data["lat"] = lat
        if lng is not None:
            data["lng"] = lng
        
        # Añadir preferencias si existen
        if preferences:
            data.update(preferences)
        
        return self._call_webhook("get_poi_recommendations", data)
    
    # ==================== RESERVAS Y PAGOS ====================
    
    def create_booking(self, poi_id: str,
                      poi_name: str,
                      booking_date: datetime,
                      number_of_people: int,
                      total_price: float,
                      user_id: str,
                      contact_email: str,
                      contact_phone: str = None,
                      currency: str = "EUR") -> Optional[Dict]:
        """
        Crea una reserva usando el webhook de n8n
        
        Args:
            poi_id: ID del punto de interés
            poi_name: Nombre del punto de interés
            booking_date: Fecha y hora de la reserva
            number_of_people: Número de personas
            total_price: Precio total
            user_id: ID del usuario
            contact_email: Email de contacto
            contact_phone: Teléfono de contacto (opcional)
            currency: Moneda (EUR, USD, etc.)
            
        Returns:
            Información de la reserva creada
        """
        data = {
            "user_id": user_id,
            "poi_id": poi_id,
            "poi_name": poi_name,
            "booking_date": booking_date.isoformat(),
            "number_of_people": number_of_people,
            "total_price": total_price,
            "currency": currency,
            "contact_email": contact_email,
            "contact_phone": contact_phone or ""
        }
        
        return self._call_webhook("create_booking", data)
    
    def create_booking_with_payment(self, poi_id: str, 
                                   booking_date: datetime,
                                   number_of_people: int,
                                   total_price: float,
                                   user_id: str,
                                   user_email: str,
                                   currency: str = "EUR",
                                   payment_method: str = "stripe") -> Optional[Dict]:
        """
        Crea una reserva y procesa el pago usando Stripe
        
        Args:
            poi_id: ID del punto de interés
            booking_date: Fecha y hora de la reserva
            number_of_people: Número de personas
            total_price: Precio total
            user_id: ID del usuario
            user_email: Email del usuario
            currency: Moneda (EUR, USD, etc.)
            payment_method: Método de pago
            
        Returns:
            Información de la reserva y pago con payment_id
        """
        data = {
            "user_id": user_id,
            "poi_id": poi_id,
            "booking_date": booking_date.isoformat(),
            "number_of_people": number_of_people,
            "total_price": total_price,
            "currency": currency,
            "status": "pending",
            "payment_method": payment_method,
            "user_email": user_email
        }
        
        return self._call_webhook("booking", data)
    
    # ==================== NOTIFICACIONES ====================
    
    def send_notification(self, user_id: str, 
                         notification_type: str,
                         message: str,
                         email: Optional[str] = None) -> Optional[Dict]:
        """
        Envía una notificación al usuario (email, SMS, push)
        
        Args:
            user_id: ID del usuario
            notification_type: Tipo de notificación (email, sms, push)
            message: Mensaje a enviar
            email: Email del destinatario (si aplica)
            
        Returns:
            Confirmación del envío
        """
        data = {
            "user_id": user_id,
            "notification_type": notification_type,
            "message": message,
            "email": email
        }
        
        return self._call_webhook("send_notification", data)
    
    # ==================== ANÁLISIS Y REPORTES ====================
    
    def generate_analytics_report(self, user_id: Optional[str] = None,
                                  start_date: Optional[datetime] = None,
                                  end_date: Optional[datetime] = None,
                                  report_type: str = "summary") -> Optional[Dict]:
        """
        Genera un reporte de análisis
        
        Args:
            user_id: ID del usuario (None para reporte global)
            start_date: Fecha de inicio
            end_date: Fecha de fin
            report_type: Tipo de reporte (summary, detailed, financial)
            
        Returns:
            Datos del reporte
        """
        data = {
            "user_id": user_id,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "report_type": report_type
        }
        
        return self._call_webhook("generate_report", data)
    
    # ==================== CONTENIDO AR ====================
    
    def get_ar_content(self, poi_id: str, 
                      user_id: str = "anonymous") -> Optional[Dict]:
        """
        Obtiene contenido de realidad aumentada para un POI
        
        Args:
            poi_id: ID del punto de interés
            user_id: ID del usuario
            
        Returns:
            URLs y metadatos del contenido AR
        """
        data = {
            "poi_id": poi_id,
            "user_id": user_id
        }
        
        return self._call_webhook("get_ar_content", data)
    
    # ==================== TRADUCCIÓN ====================
    
    def translate_content(self, text: str, 
                         source_lang: str = "es",
                         target_lang: str = "en") -> Optional[Dict]:
        """
        Traduce contenido a otro idioma
        
        Args:
            text: Texto a traducir
            source_lang: Idioma origen
            target_lang: Idioma destino
            
        Returns:
            Texto traducido
        """
        data = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        return self._call_webhook("translate_content", data)
    
    # ==================== GAMIFICACIÓN ====================
    
    def check_achievements(self, user_id: str, 
                          action: str,
                          metadata: Optional[Dict] = None) -> Optional[Dict]:
        """
        Verifica si el usuario ha desbloqueado nuevos logros
        
        Args:
            user_id: ID del usuario
            action: Acción realizada
            metadata: Metadatos adicionales
            
        Returns:
            Logros desbloqueados
        """
        data = {
            "user_id": user_id,
            "action": action,
            "metadata": metadata or {}
        }
        
        return self._call_webhook("check_achievements", data)
    
    # ==================== BÚSQUEDA INTELIGENTE ====================
    
    def smart_search(self, query: str,
                    city_id: Optional[str] = None,
                    filters: Optional[Dict] = None) -> Optional[Dict]:
        """
        Realiza una búsqueda inteligente de POIs usando IA
        
        Args:
            query: Consulta de búsqueda
            city_id: ID de la ciudad (opcional)
            filters: Filtros adicionales
            
        Returns:
            Resultados de búsqueda ordenados por relevancia
        """
        data = {
            "query": query,
            "city_id": city_id,
            "filters": filters or {}
        }
        
        return self._call_webhook("smart_search", data)
    
    # ==================== ITINERARIOS ====================
    
    def generate_itinerary(self, city_id: str,
                          duration_days: int,
                          preferences: Dict,
                          user_id: str = "anonymous") -> Optional[Dict]:
        """
        Genera un itinerario personalizado usando IA
        
        Args:
            city_id: ID de la ciudad
            duration_days: Duración del viaje en días
            preferences: Preferencias del usuario
            user_id: ID del usuario
            
        Returns:
            Itinerario día por día
        """
        data = {
            "city_id": city_id,
            "duration_days": duration_days,
            "preferences": preferences,
            "user_id": user_id
        }
        
        return self._call_webhook("generate_itinerary", data)


# Instancia global de n8n
@st.cache_resource
def get_n8n_integration():
    """Obtiene una instancia cacheada de la integración con n8n"""
    # Limpiar caché si es necesario (forzar recreación)
    return N8NIntegration()
