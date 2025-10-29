"""
Página de Favoritos
"""
import streamlit as st

def show(db, n8n):
    """Muestra la página de favoritos"""
    
    st.title("⭐ Mis Favoritos")
    st.markdown("Lugares que has guardado para visitar más tarde")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Debes iniciar sesión para ver tus favoritos")
        return
    
    # Obtener favoritos
    favorites = db.get_user_favorites(st.session_state.user_id)
    
    if not favorites:
        st.info("📌 No tienes favoritos aún. Explora lugares y añádelos a tus favoritos.")
        
        if st.button("🌍 Explorar Ciudades", use_container_width=True):
            st.info("Redirigiendo a explorar ciudades...")
        
        return
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❤️ Total Favoritos", len(favorites))
    with col2:
        cities = set(f.get('points_of_interest', {}).get('cities', {}).get('name') for f in favorites)
        st.metric("🌍 Ciudades", len(cities))
    with col3:
        categories = set(f.get('points_of_interest', {}).get('category') for f in favorites)
        st.metric("📊 Categorías", len(categories))
    
    st.markdown("---")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.selectbox(
            "Filtrar por ciudad",
            ["Todas"] + sorted(list(cities))
        )
    with col2:
        category_filter = st.selectbox(
            "Filtrar por categoría",
            ["Todas"] + sorted(list(categories))
        )
    
    # Aplicar filtros
    filtered_favorites = favorites
    if city_filter != "Todas":
        filtered_favorites = [f for f in favorites 
                            if f.get('points_of_interest', {}).get('cities', {}).get('name') == city_filter]
    if category_filter != "Todas":
        filtered_favorites = [f for f in favorites 
                            if f.get('points_of_interest', {}).get('category') == category_filter]
    
    st.markdown(f"### 📍 {len(filtered_favorites)} lugares favoritos")
    st.markdown("---")
    
    # Listar favoritos
    for favorite in filtered_favorites:
        poi = favorite.get('points_of_interest', {})
        city = poi.get('cities', {})
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### ⭐ {poi.get('name', 'N/A')}")
                
                # Información básica
                info_cols = st.columns(4)
                with info_cols[0]:
                    st.caption(f"📍 {city.get('name', 'N/A')}")
                with info_cols[1]:
                    st.caption(f"📌 {poi.get('category', 'N/A')}")
                with info_cols[2]:
                    st.caption(f"⭐ {poi.get('rating', 0):.1f}/5.0")
                with info_cols[3]:
                    st.caption(f"🕐 {poi.get('visit_duration', 0)} min")
                
                # Descripción
                if poi.get('short_description'):
                    st.write(poi['short_description'])
                elif poi.get('description'):
                    st.write(poi['description'][:150] + "...")
                
                # Notas del usuario
                if favorite.get('notes'):
                    st.info(f"📝 **Tus notas:** {favorite['notes']}")
            
            with col2:
                # Botones de acción
                if st.button("👁️ Ver Detalles", key=f"view_{poi['id']}", use_container_width=True):
                    st.session_state.selected_poi = poi['id']
                    st.info("Mostrando detalles...")
                
                if st.button("🎧 Audio-Guía", key=f"audio_{poi['id']}", use_container_width=True):
                    st.info("Generando audio-guía...")
                
                if st.button("🎫 Reservar", key=f"book_{poi['id']}", use_container_width=True):
                    st.info("Redirigiendo a reservas...")
                
                if st.button("💔 Quitar", key=f"remove_{poi['id']}", use_container_width=True):
                    result = db.remove_favorite(st.session_state.user_id, poi['id'])
                    if result:
                        st.success("Eliminado de favoritos")
                        st.rerun()
            
            st.divider()
    
    # Exportar favoritos
    st.markdown("---")
    if st.button("📥 Exportar Favoritos (PDF)", use_container_width=True):
        st.info("Función de exportación en desarrollo...")
