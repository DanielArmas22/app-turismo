"""
Módulo de conexión y operaciones con Supabase
"""
from supabase import create_client, Client
from typing import List, Dict, Optional, Any
import streamlit as st
from datetime import datetime
import config

class SupabaseDB:
    """Clase para manejar todas las operaciones con Supabase"""
    
    def __init__(self):
        """Inicializa la conexión con Supabase"""
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    
    # ==================== OPERACIONES DE CIUDADES ====================
    
    def get_cities(self, is_active: bool = True) -> List[Dict]:
        """Obtiene todas las ciudades activas"""
        try:
            query = self.client.table("cities").select("*")
            if is_active:
                query = query.eq("is_active", True)
            response = query.execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener ciudades: {str(e)}")
            return []
    
    def get_city_by_id(self, city_id: str) -> Optional[Dict]:
        """Obtiene una ciudad por su ID"""
        try:
            response = self.client.table("cities").select("*").eq("id", city_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al obtener ciudad: {str(e)}")
            return None
    
    def create_city(self, city_data: Dict) -> Optional[Dict]:
        """Crea una nueva ciudad"""
        try:
            response = self.client.table("cities").insert(city_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al crear ciudad: {str(e)}")
            return None
    
    def update_city(self, city_id: str, city_data: Dict) -> Optional[Dict]:
        """Actualiza una ciudad"""
        try:
            response = self.client.table("cities").update(city_data).eq("id", city_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al actualizar ciudad: {str(e)}")
            return None
    
    def delete_city(self, city_id: str) -> bool:
        """Elimina una ciudad (soft delete)"""
        try:
            self.client.table("cities").update({"is_active": False}).eq("id", city_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al eliminar ciudad: {str(e)}")
            return False
    
    def get_all_cities(self, include_inactive: bool = False) -> List[Dict]:
        """Obtiene todas las ciudades, incluyendo inactivas si se solicita"""
        try:
            query = self.client.table("cities").select("*")
            if not include_inactive:
                query = query.eq("is_active", True)
            response = query.order("name").execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener ciudades: {str(e)}")
            return []
    
    # ==================== OPERACIONES DE POIs ====================
    
    def get_pois(self, city_id: Optional[str] = None, category: Optional[str] = None, 
                 is_active: bool = True) -> List[Dict]:
        """Obtiene puntos de interés con filtros opcionales"""
        try:
            query = self.client.table("points_of_interest").select("*, cities(*)")
            
            if is_active:
                query = query.eq("is_active", True)
            if city_id:
                query = query.eq("city_id", city_id)
            if category:
                query = query.eq("category", category)
            
            response = query.execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener POIs: {str(e)}")
            return []
    
    def get_poi_by_id(self, poi_id: str) -> Optional[Dict]:
        """Obtiene un POI por su ID"""
        try:
            response = self.client.table("points_of_interest").select("*, cities(*)").eq("id", poi_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al obtener POI: {str(e)}")
            return None
    
    def create_poi(self, poi_data: Dict) -> Optional[Dict]:
        """Crea un nuevo punto de interés"""
        try:
            response = self.client.table("points_of_interest").insert(poi_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al crear POI: {str(e)}")
            return None
    
    def update_poi_rating(self, poi_id: str, new_rating: float, total_reviews: int) -> bool:
        """Actualiza el rating de un POI"""
        try:
            self.client.table("points_of_interest").update({
                "rating": new_rating,
                "total_reviews": total_reviews
            }).eq("id", poi_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al actualizar rating: {str(e)}")
            return False
    
    def update_poi(self, poi_id: str, poi_data: Dict) -> Optional[Dict]:
        """Actualiza un POI"""
        try:
            response = self.client.table("points_of_interest").update(poi_data).eq("id", poi_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al actualizar POI: {str(e)}")
            return None
    
    def delete_poi(self, poi_id: str) -> bool:
        """Elimina un POI (soft delete)"""
        try:
            self.client.table("points_of_interest").update({"is_active": False}).eq("id", poi_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al eliminar POI: {str(e)}")
            return False
    
    def get_all_pois(self, include_inactive: bool = False) -> List[Dict]:
        """Obtiene todos los POIs, incluyendo inactivos si se solicita"""
        try:
            query = self.client.table("points_of_interest").select("*, cities(*)")
            if not include_inactive:
                query = query.eq("is_active", True)
            response = query.order("name").execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener POIs: {str(e)}")
            return []
    
    # ==================== OPERACIONES DE USUARIOS ====================
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Obtiene un usuario por email"""
        try:
            response = self.client.table("users").select("*").eq("email", email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al obtener usuario: {str(e)}")
            return None
    
    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Crea un nuevo usuario"""
        try:
            response = self.client.table("users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al crear usuario: {str(e)}")
            return None
    
    def update_user_points(self, user_id: str, points: int) -> bool:
        """Actualiza los puntos de un usuario"""
        try:
            self.client.table("users").update({
                "total_points": points
            }).eq("id", user_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al actualizar puntos: {str(e)}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Obtiene un usuario por su ID"""
        try:
            response = self.client.table("users").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al obtener usuario: {str(e)}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Obtiene todos los usuarios"""
        try:
            response = self.client.table("users").select("*").order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener usuarios: {str(e)}")
            return []
    
    def update_user(self, user_id: str, user_data: Dict) -> Optional[Dict]:
        """Actualiza un usuario"""
        try:
            response = self.client.table("users").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al actualizar usuario: {str(e)}")
            return None
    
    def delete_user(self, user_id: str) -> bool:
        """Elimina un usuario"""
        try:
            self.client.table("users").delete().eq("id", user_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al eliminar usuario: {str(e)}")
            return False
    
    # ==================== OPERACIONES DE VISITAS ====================
    
    def get_user_visits(self, user_id: str) -> List[Dict]:
        """Obtiene todas las visitas de un usuario"""
        try:
            response = self.client.table("user_visits").select(
                "*, points_of_interest(*, cities(*))"
            ).eq("user_id", user_id).order("visit_date", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener visitas: {str(e)}")
            return []
    
    def create_visit(self, visit_data: Dict) -> Optional[Dict]:
        """Registra una nueva visita"""
        try:
            response = self.client.table("user_visits").insert(visit_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al crear visita: {str(e)}")
            return None
    
    def get_poi_visits_count(self, poi_id: str) -> int:
        """Obtiene el número de visitas de un POI"""
        try:
            response = self.client.table("user_visits").select("id", count="exact").eq("poi_id", poi_id).execute()
            return response.count if response.count else 0
        except Exception as e:
            st.error(f"Error al contar visitas: {str(e)}")
            return 0
    
    def get_all_visits(self) -> List[Dict]:
        """Obtiene todas las visitas"""
        try:
            response = self.client.table("user_visits").select(
                "*, points_of_interest(*, cities(*)), users(*)"
            ).order("visit_date", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener visitas: {str(e)}")
            return []
    
    def update_visit(self, visit_id: str, visit_data: Dict) -> Optional[Dict]:
        """Actualiza una visita"""
        try:
            response = self.client.table("user_visits").update(visit_data).eq("id", visit_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al actualizar visita: {str(e)}")
            return None
    
    def delete_visit(self, visit_id: str) -> bool:
        """Elimina una visita"""
        try:
            self.client.table("user_visits").delete().eq("id", visit_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al eliminar visita: {str(e)}")
            return False
    
    # ==================== OPERACIONES DE LOGROS ====================
    
    def get_user_achievements(self, user_id: str) -> List[Dict]:
        """Obtiene todos los logros de un usuario"""
        try:
            response = self.client.table("user_achievements").select("*").eq(
                "user_id", user_id
            ).order("earned_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener logros: {str(e)}")
            return []
    
    def create_achievement(self, achievement_data: Dict) -> Optional[Dict]:
        """Crea un nuevo logro para un usuario"""
        try:
            response = self.client.table("user_achievements").insert(achievement_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            # El error puede ser por duplicado (UNIQUE constraint)
            if "duplicate" in str(e).lower():
                return None
            st.error(f"Error al crear logro: {str(e)}")
            return None
    
    # ==================== OPERACIONES DE RESERVAS ====================
    
    def get_user_bookings(self, user_id: str) -> List[Dict]:
        """Obtiene todas las reservas de un usuario"""
        try:
            response = self.client.table("bookings").select(
                "*, points_of_interest(*, cities(*))"
            ).eq("user_id", user_id).order("booking_date", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener reservas: {str(e)}")
            return []
    
    def create_booking(self, booking_data: Dict) -> Optional[Dict]:
        """Crea una nueva reserva"""
        try:
            response = self.client.table("bookings").insert(booking_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al crear reserva: {str(e)}")
            return None
    
    def update_booking_status(self, booking_id: str, status: str) -> bool:
        """Actualiza el estado de una reserva"""
        try:
            self.client.table("bookings").update({
                "status": status
            }).eq("id", booking_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al actualizar reserva: {str(e)}")
            return False
    
    def get_all_bookings(self) -> List[Dict]:
        """Obtiene todas las reservas"""
        try:
            response = self.client.table("bookings").select(
                "*, points_of_interest(*, cities(*)), users(*)"
            ).order("booking_date", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener reservas: {str(e)}")
            return []
    
    def get_booking_by_id(self, booking_id: str) -> Optional[Dict]:
        """Obtiene una reserva por su ID"""
        try:
            response = self.client.table("bookings").select(
                "*, points_of_interest(*, cities(*)), users(*)"
            ).eq("id", booking_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al obtener reserva: {str(e)}")
            return None
    
    def update_booking(self, booking_id: str, booking_data: Dict) -> Optional[Dict]:
        """Actualiza una reserva"""
        try:
            response = self.client.table("bookings").update(booking_data).eq("id", booking_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al actualizar reserva: {str(e)}")
            return None
    
    def delete_booking(self, booking_id: str) -> bool:
        """Elimina una reserva"""
        try:
            self.client.table("bookings").delete().eq("id", booking_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al eliminar reserva: {str(e)}")
            return False
    
    # ==================== OPERACIONES DE ESTADÍSTICAS ====================
    
    def create_usage_stat(self, stat_data: Dict) -> Optional[Dict]:
        """Registra una estadística de uso"""
        try:
            response = self.client.table("usage_stats").insert(stat_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            # No mostrar error al usuario para stats
            print(f"Error al crear estadística: {str(e)}")
            return None
    
    def get_usage_stats(self, user_id: Optional[str] = None, 
                       action_type: Optional[str] = None,
                       limit: int = 100) -> List[Dict]:
        """Obtiene estadísticas de uso"""
        try:
            query = self.client.table("usage_stats").select("*")
            
            if user_id:
                query = query.eq("user_id", user_id)
            if action_type:
                query = query.eq("action_type", action_type)
            
            response = query.order("timestamp", desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener estadísticas: {str(e)}")
            return []
    
    # ==================== OPERACIONES DE AUDIO-GUÍAS ====================
    
    def get_audio_guides(self, poi_id: str, language: str = "es") -> List[Dict]:
        """Obtiene audio-guías para un POI"""
        try:
            response = self.client.table("audio_guides").select("*").eq(
                "poi_id", poi_id
            ).eq("language", language).eq("is_active", True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener audio-guías: {str(e)}")
            return []
    
    def create_audio_guide(self, audio_data: Dict) -> Optional[Dict]:
        """Crea una nueva audio-guía"""
        try:
            response = self.client.table("audio_guides").insert(audio_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error al crear audio-guía: {str(e)}")
            return None
    
    def increment_audio_play_count(self, audio_id: str) -> bool:
        """Incrementa el contador de reproducciones de una audio-guía"""
        try:
            # Primero obtener el audio actual
            audio = self.client.table("audio_guides").select("play_count").eq("id", audio_id).execute()
            if audio.data:
                current_count = audio.data[0].get("play_count", 0)
                now = datetime.now()
                self.client.table("audio_guides").update({
                    "play_count": current_count + 1,
                    "last_played_at": now.isoformat() if now else None
                }).eq("id", audio_id).execute()
                return True
            return False
        except Exception as e:
            print(f"Error al incrementar contador: {str(e)}")
            return False
    
    # ==================== OPERACIONES DE FAVORITOS ====================
    
    def get_user_favorites(self, user_id: str) -> List[Dict]:
        """Obtiene los favoritos de un usuario"""
        try:
            response = self.client.table("favorites").select(
                "*, points_of_interest(*, cities(*))"
            ).eq("user_id", user_id).order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            st.error(f"Error al obtener favoritos: {str(e)}")
            return []
    
    def add_favorite(self, user_id: str, poi_id: str, notes: str = "") -> Optional[Dict]:
        """Añade un POI a favoritos"""
        try:
            response = self.client.table("favorites").insert({
                "user_id": user_id,
                "poi_id": poi_id,
                "notes": notes
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            if "duplicate" in str(e).lower():
                st.warning("Este lugar ya está en tus favoritos")
            else:
                st.error(f"Error al añadir favorito: {str(e)}")
            return None
    
    def remove_favorite(self, user_id: str, poi_id: str) -> bool:
        """Elimina un POI de favoritos"""
        try:
            self.client.table("favorites").delete().eq("user_id", user_id).eq("poi_id", poi_id).execute()
            return True
        except Exception as e:
            st.error(f"Error al eliminar favorito: {str(e)}")
            return False
    
    def is_favorite(self, user_id: str, poi_id: str) -> bool:
        """Verifica si un POI está en favoritos"""
        try:
            response = self.client.table("favorites").select("id").eq(
                "user_id", user_id
            ).eq("poi_id", poi_id).execute()
            return len(response.data) > 0
        except Exception as e:
            return False


# Instancia global de la base de datos
@st.cache_resource
def get_database():
    """Obtiene una instancia cacheada de la base de datos"""
    return SupabaseDB()
