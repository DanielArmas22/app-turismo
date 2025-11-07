"""
Página de Recomendaciones de POIs
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import config

def show(db, n8n):
    """Muestra la página de recomendaciones personalizadas"""
    
    st.title("🎯 Recomendaciones Personalizadas")
    st.markdown("Descubre lugares increíbles basados en tu ubicación y preferencias")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Debes iniciar sesión para obtener recomendaciones personalizadas")
        return
    
    # Tabs
    tab1, tab2 = st.tabs(["🔍 Buscar Recomendaciones", "💾 Mis Recomendaciones"])
    
    with tab1:
        show_search_recommendations(db, n8n)
    
    with tab2:
        show_saved_recommendations(db, n8n)


def show_search_recommendations(db, n8n):
    """Muestra el formulario para buscar recomendaciones"""
    
    st.subheader("🔍 Buscar Lugares Recomendados")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selección de ciudad
        cities = db.get_cities()
        if not cities:
            st.error("No hay ciudades disponibles")
            return
        
        city_options = {c['name']: c for c in cities}
        selected_city_name = st.selectbox("Ciudad", list(city_options.keys()))
        selected_city = city_options[selected_city_name]
        
        # Coordenadas (usar las de la ciudad por defecto)
        st.markdown("### 📍 Ubicación")
        col_a, col_b = st.columns(2)
        with col_a:
            latitude = st.number_input(
                "Latitud", 
                value=float(selected_city.get('latitude', 41.4036)),
                format="%.6f",
                help="Coordenada de latitud para buscar lugares cercanos"
            )
        with col_b:
            longitude = st.number_input(
                "Longitud", 
                value=float(selected_city.get('longitude', 2.1744)),
                format="%.6f",
                help="Coordenada de longitud para buscar lugares cercanos"
            )
        
        # Preferencias
        st.markdown("### 🎯 Preferencias")
        
        col_x, col_y = st.columns(2)
        with col_x:
            categories = st.multiselect(
                "Categorías de interés",
                config.POI_CATEGORIES,
                default=[]
            )
        
        with col_y:
            max_distance = st.slider(
                "Distancia máxima (km)",
                min_value=1,
                max_value=50,
                value=10
            )
        
        col_z, col_w = st.columns(2)
        with col_z:
            min_rating = st.slider(
                "Rating mínimo",
                min_value=0.0,
                max_value=5.0,
                value=3.5,
                step=0.5
            )
        
        with col_w:
            max_results = st.number_input(
                "Número de resultados",
                min_value=5,
                max_value=50,
                value=10
            )
    
    with col2:
        st.markdown("### 🗺️ Vista Previa")
        st.info(f"""
        **Ciudad:** {selected_city_name}
        
        **Coordenadas:**
        - Lat: {latitude}
        - Lng: {longitude}
        
        **Filtros:**
        - Categorías: {len(categories) if categories else 'Todas'}
        - Distancia: {max_distance} km
        - Rating: ≥ {min_rating}
        """)
    
    # Botón de búsqueda
    st.markdown("---")
    
    if st.button("🔍 Buscar Recomendaciones", type="primary", use_container_width=True):
        search_recommendations(db, n8n, selected_city['id'], latitude, longitude, 
                             categories, max_distance, min_rating, max_results)


def search_recommendations(db, n8n, city_id, lat, lng, categories, max_distance, min_rating, max_results):
    """Busca recomendaciones usando n8n"""
    
    with st.spinner("🔍 Buscando recomendaciones personalizadas..."):
        try:
            # Preparar preferencias
            preferences = {
                "max_distance": max_distance,
                "min_rating": min_rating,
                "max_results": max_results
            }
            
            if categories:
                preferences["categories"] = categories
            
            # Llamar a n8n
            result = n8n.get_poi_recommendations(
                city_id=city_id,
                user_id=st.session_state.user_id,
                lat=lat,
                lng=lng,
                preferences=preferences
            )
            
            if result is None:
                st.error("❌ No se pudo conectar con el servicio de recomendaciones")
                st.info("💡 **Soluciones posibles:**")
                st.info("1. Verifica que el servicio n8n esté activo")
                st.info("2. Revisa la URL del webhook en la configuración")
                st.info("3. Verifica tu conexión a internet")
                
                # Mostrar POIs locales como alternativa
                st.markdown("---")
                st.subheader("📍 Lugares Disponibles en la Ciudad")
                show_local_pois_fallback(db, city_id, lat, lng)
                return
            
            if result and 'recommendations' in result:
                recommendations = result['recommendations']
                
                if not recommendations:
                    st.warning("No se encontraron recomendaciones con los criterios especificados")
                    return
                
                st.success(f"✅ Se encontraron {len(recommendations)} recomendaciones")
                
                # Guardar recomendaciones en la base de datos
                save_recommendations_to_db(db, recommendations, city_id, lat, lng)
                
                # Mostrar resultados
                display_recommendations(db, recommendations, lat, lng)
                
            elif result and 'pois' in result:
                # Formato alternativo de respuesta
                pois = result['pois']
                st.success(f"✅ Se encontraron {len(pois)} recomendaciones")
                display_recommendations(db, pois, lat, lng)
            else:
                st.warning("⚠️ El servicio respondió pero sin recomendaciones")
                st.info("Mostrando lugares disponibles en la base de datos local...")
                show_local_pois_fallback(db, city_id, lat, lng)
                
        except Exception as e:
            st.error(f"❌ Error al buscar recomendaciones: {str(e)}")
            st.info("Mostrando lugares disponibles en la base de datos local...")
            show_local_pois_fallback(db, city_id, lat, lng)


def save_recommendations_to_db(db, recommendations, city_id, lat, lng):
    """Guarda las recomendaciones en la base de datos"""
    
    try:
        for rec in recommendations:
            # Verificar si el POI ya existe
            poi_id = rec.get('id') or rec.get('poi_id')
            
            if poi_id:
                # Guardar como favorito o en una tabla de recomendaciones
                # Por ahora, registrar como estadística de uso
                db.create_usage_stat({
                    "user_id": st.session_state.user_id,
                    "action_type": "recommendation_received",
                    "poi_id": poi_id,
                    "metadata": {
                        "city_id": city_id,
                        "lat": lat,
                        "lng": lng,
                        "score": rec.get('score', 0)
                    }
                })
    except Exception as e:
        st.warning(f"No se pudieron guardar todas las recomendaciones: {str(e)}")


def display_recommendations(db, recommendations, user_lat, user_lng):
    """Muestra las recomendaciones con mapa"""
    
    st.markdown("---")
    st.subheader("🎯 Lugares Recomendados")
    
    # Preparar datos para el mapa
    map_data = []
    for rec in recommendations:
        lat = rec.get('latitude') or rec.get('lat')
        lng = rec.get('longitude') or rec.get('lng')
        
        if lat and lng:
            map_data.append({
                'lat': float(lat),
                'lon': float(lng),
                'name': rec.get('name', 'Sin nombre'),
                'rating': rec.get('rating', 0)
            })
    
    # Mostrar mapa si hay datos
    if map_data:
        st.markdown("### 🗺️ Mapa de Recomendaciones")
        
        # Crear DataFrame para el mapa
        df_map = pd.DataFrame(map_data)
        
        # Mostrar mapa con pydeck (más interactivo)
        try:
            import pydeck as pdk
            
            # Capa de puntos para las recomendaciones
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=df_map,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
                pickable=True,
                auto_highlight=True
            )
            
            # Punto de usuario
            user_layer = pdk.Layer(
                'ScatterplotLayer',
                data=pd.DataFrame([{'lat': user_lat, 'lon': user_lng}]),
                get_position='[lon, lat]',
                get_color='[0, 128, 255, 200]',
                get_radius=300,
                pickable=True
            )
            
            # Vista del mapa
            view_state = pdk.ViewState(
                latitude=user_lat,
                longitude=user_lng,
                zoom=12,
                pitch=0
            )
            
            # Renderizar mapa
            r = pdk.Deck(
                layers=[layer, user_layer],
                initial_view_state=view_state,
                tooltip={"text": "{name}\n⭐ {rating}"},
                map_style='mapbox://styles/mapbox/light-v10'
            )
            
            st.pydeck_chart(r)
            
        except ImportError:
            # Fallback a mapa simple de Streamlit
            st.map(df_map)
        
        st.caption("🔵 Tu ubicación | 🔴 Lugares recomendados")
    
    # Lista de recomendaciones
    st.markdown("---")
    st.markdown("### 📋 Lista de Recomendaciones")
    
    for idx, rec in enumerate(recommendations, 1):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                name = rec.get('name', 'Sin nombre')
                st.markdown(f"**{idx}. {name}**")
                
                # Información básica
                info_parts = []
                if rec.get('category'):
                    info_parts.append(f"📌 {rec['category']}")
                if rec.get('rating'):
                    info_parts.append(f"⭐ {rec['rating']:.1f}")
                if rec.get('distance'):
                    info_parts.append(f"📍 {rec['distance']:.1f} km")
                
                if info_parts:
                    st.caption(" • ".join(info_parts))
                
                # Descripción
                if rec.get('description'):
                    st.write(rec['description'][:150] + "...")
            
            with col2:
                # Score o relevancia
                score = rec.get('score', rec.get('relevance_score', 0))
                if score:
                    st.metric("Relevancia", f"{score:.0%}")
                
                # Precio
                price = rec.get('entry_price', rec.get('price', 0))
                if price:
                    st.caption(f"💰 €{price:.2f}")
            
            with col3:
                # Acciones
                poi_id = rec.get('id') or rec.get('poi_id')
                
                if poi_id and st.session_state.user_id:
                    if st.button("❤️ Guardar", key=f"save_{poi_id}_{idx}", use_container_width=True):
                        db.add_favorite(st.session_state.user_id, poi_id)
                        st.success("Guardado!")
                        st.rerun()
                
                # Ver en mapa
                lat = rec.get('latitude') or rec.get('lat')
                lng = rec.get('longitude') or rec.get('lng')
                if lat and lng:
                    maps_url = f"https://www.google.com/maps?q={lat},{lng}"
                    st.markdown(f"[🗺️ Ver]({maps_url})", unsafe_allow_html=True)
            
            st.divider()


def show_local_pois_fallback(db, city_id, user_lat, user_lng):
    """Muestra POIs locales como alternativa cuando n8n no está disponible"""
    
    try:
        # Obtener POIs de la ciudad
        pois = db.get_pois(city_id=city_id)
        
        if not pois:
            st.warning("No hay lugares disponibles en la base de datos local para esta ciudad")
            return
        
        st.info(f"📍 Mostrando {len(pois)} lugares desde la base de datos local")
        
        # Calcular distancia aproximada (si tienen coordenadas)
        import math
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            """Calcula distancia en km usando fórmula de Haversine"""
            R = 6371  # Radio de la Tierra en km
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            return R * c
        
        # Agregar distancia a cada POI
        for poi in pois:
            if poi.get('latitude') and poi.get('longitude'):
                distance = calculate_distance(
                    user_lat, user_lng,
                    float(poi['latitude']), float(poi['longitude'])
                )
                poi['distance'] = distance
            else:
                poi['distance'] = None
        
        # Ordenar por distancia
        pois_with_distance = [p for p in pois if p.get('distance') is not None]
        pois_without_distance = [p for p in pois if p.get('distance') is None]
        pois_sorted = sorted(pois_with_distance, key=lambda x: x['distance']) + pois_without_distance
        
        # Mostrar como recomendaciones
        display_recommendations(db, pois_sorted, user_lat, user_lng)
        
    except Exception as e:
        st.error(f"Error al cargar lugares locales: {str(e)}")


def show_saved_recommendations(db, n8n):
    """Muestra las recomendaciones guardadas del usuario"""
    
    st.subheader("💾 Mis Recomendaciones Guardadas")
    
    # Obtener estadísticas de recomendaciones
    try:
        stats = db.get_user_stats(st.session_state.user_id)
        
        # Filtrar solo las recomendaciones
        recommendations_stats = [
            s for s in stats 
            if s.get('action_type') == 'recommendation_received'
        ]
        
        if not recommendations_stats:
            st.info("No tienes recomendaciones guardadas aún. ¡Busca algunas en la pestaña anterior!")
            return
        
        st.metric("📊 Total de Recomendaciones Recibidas", len(recommendations_stats))
        
        # Agrupar por ciudad
        cities_dict = {}
        for stat in recommendations_stats:
            metadata = stat.get('metadata', {})
            city_id = metadata.get('city_id')
            
            if city_id:
                if city_id not in cities_dict:
                    cities_dict[city_id] = []
                cities_dict[city_id].append(stat)
        
        # Mostrar por ciudad
        for city_id, city_stats in cities_dict.items():
            city = db.get_city(city_id)
            if city:
                with st.expander(f"📍 {city['name']} ({len(city_stats)} recomendaciones)", expanded=False):
                    for stat in city_stats:
                        poi_id = stat.get('poi_id')
                        if poi_id:
                            poi = db.get_poi(poi_id)
                            if poi:
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.write(f"**{poi['name']}**")
                                    st.caption(f"⭐ {poi.get('rating', 0):.1f} • 📌 {poi.get('category', 'N/A')}")
                                with col2:
                                    if st.button("Ver", key=f"view_saved_{poi_id}", use_container_width=True):
                                        st.session_state.selected_poi = poi_id
                                        st.info("Redirigiendo...")
                                st.divider()
    
    except Exception as e:
        st.error(f"Error al cargar recomendaciones: {str(e)}")
