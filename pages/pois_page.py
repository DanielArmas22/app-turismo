"""
Página de Puntos de Interés
"""
import streamlit as st
import config

def show(db, n8n):
    """Muestra la página de puntos de interés"""
    
    st.title("📍 Puntos de Interés")
    st.markdown("Explora lugares increíbles y planifica tu visita")
    
    # Filtros
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cities = db.get_cities()
        city_options = ["Todas"] + [c['name'] for c in cities]
        selected_city_name = st.selectbox("Ciudad", city_options)
        
        selected_city_id = None
        if selected_city_name != "Todas":
            selected_city_id = next((c['id'] for c in cities if c['name'] == selected_city_name), None)
    
    with col2:
        category_options = ["Todas"] + config.POI_CATEGORIES
        selected_category = st.selectbox("Categoría", category_options)
    
    with col3:
        difficulty_options = ["Todas"] + config.DIFFICULTY_LEVELS
        selected_difficulty = st.selectbox("Dificultad", difficulty_options)
    
    with col4:
        sort_options = ["Nombre", "Rating", "Duración", "Precio"]
        sort_by = st.selectbox("Ordenar por", sort_options)
    
    # Búsqueda
    search_query = st.text_input("🔍 Buscar punto de interés", placeholder="Ej: Museo, Palacio...")
    
    st.markdown("---")
    
    # Obtener POIs con filtros
    pois = db.get_pois(
        city_id=selected_city_id,
        category=selected_category if selected_category != "Todas" else None
    )
    
    # Aplicar filtros adicionales
    if search_query:
        pois = [p for p in pois if search_query.lower() in p['name'].lower() or 
                search_query.lower() in p.get('description', '').lower()]
    
    if selected_difficulty != "Todas":
        pois = [p for p in pois if p.get('difficulty_level') == selected_difficulty]
    
    # Ordenar
    if sort_by == "Rating":
        pois = sorted(pois, key=lambda x: x.get('rating', 0), reverse=True)
    elif sort_by == "Duración":
        pois = sorted(pois, key=lambda x: x.get('visit_duration', 0))
    elif sort_by == "Precio":
        pois = sorted(pois, key=lambda x: x.get('entry_price', 0))
    else:
        pois = sorted(pois, key=lambda x: x['name'])
    
    # Mostrar resultados
    st.subheader(f"📊 {len(pois)} puntos de interés encontrados")
    
    if not pois:
        st.info("No se encontraron puntos de interés con los filtros aplicados")
    else:
        # Vista de lista
        for poi in pois:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### {poi['name']}")
                    
                    # Información básica
                    info_cols = st.columns(4)
                    with info_cols[0]:
                        st.caption(f"📌 {poi.get('category', 'Sin categoría')}")
                    with info_cols[1]:
                        st.caption(f"⭐ {poi.get('rating', 0):.1f} ({poi.get('total_reviews', 0)} reseñas)")
                    with info_cols[2]:
                        st.caption(f"🕐 {poi.get('visit_duration', 0)} min")
                    with info_cols[3]:
                        st.caption(f"💰 €{poi.get('entry_price', 0):.2f}")
                    
                    # Descripción corta
                    if poi.get('short_description'):
                        st.write(poi['short_description'])
                    elif poi.get('description'):
                        st.write(poi['description'][:150] + "...")
                    
                    # Ciudad
                    if poi.get('cities'):
                        st.caption(f"📍 {poi['cities']['name']}, {poi['cities']['country']}")
                
                with col2:
                    # Botones de acción
                    if st.button("👁️ Ver Detalles", key=f"view_{poi['id']}", use_container_width=True):
                        show_poi_details(db, n8n, poi)
                    
                    if st.session_state.user_id:
                        is_fav = db.is_favorite(st.session_state.user_id, poi['id'])
                        fav_label = "💔 Quitar" if is_fav else "❤️ Favorito"
                        
                        if st.button(fav_label, key=f"fav_{poi['id']}", use_container_width=True):
                            if is_fav:
                                db.remove_favorite(st.session_state.user_id, poi['id'])
                                st.success("Eliminado de favoritos")
                            else:
                                db.add_favorite(st.session_state.user_id, poi['id'])
                                st.success("Añadido a favoritos")
                            st.rerun()
                    
                    if st.button("🎧 Audio-Guía", key=f"audio_{poi['id']}", use_container_width=True):
                        st.session_state.selected_poi = poi['id']
                        st.info("Generando audio-guía...")
                
                st.divider()


def show_poi_details(db, n8n, poi):
    """Muestra los detalles completos de un POI"""
    
    with st.expander(f"📍 {poi['name']}", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Imágenes
            if poi.get('image_urls') and len(poi['image_urls']) > 0:
                st.image(poi['image_urls'][0], width=600)
            else:
                st.image('https://via.placeholder.com/600x400', width=600)
            
            # Descripción completa
            st.markdown("### Descripción")
            st.write(poi.get('description', 'Sin descripción disponible'))
            
            # Información de accesibilidad
            if poi.get('accessibility_info'):
                st.info(f"♿ **Accesibilidad:** {poi['accessibility_info']}")
            
            # Horarios
            if poi.get('opening_hours'):
                st.markdown("### 🕐 Horarios")
                st.json(poi['opening_hours'])
        
        with col2:
            # Métricas
            st.metric("⭐ Rating", f"{poi.get('rating', 0):.1f}/5.0")
            st.metric("💰 Precio", f"€{poi.get('entry_price', 0):.2f}")
            st.metric("🕐 Duración", f"{poi.get('visit_duration', 0)} min")
            st.metric("📊 Dificultad", poi.get('difficulty_level', 'N/A'))
            
            # Coordenadas
            if poi.get('latitude') and poi.get('longitude'):
                st.markdown("### 📍 Ubicación")
                st.write(f"Lat: {poi['latitude']}")
                st.write(f"Lng: {poi['longitude']}")
                
                # Link a Google Maps
                maps_url = f"https://www.google.com/maps?q={poi['latitude']},{poi['longitude']}"
                st.markdown(f"[🗺️ Ver en Google Maps]({maps_url})")
            
            st.markdown("---")
            
            # Acciones
            if st.session_state.user_id:
                if st.button("🎫 Reservar", key=f"book_{poi['id']}", use_container_width=True):
                    st.info("Redirigiendo a reservas...")
                
                if st.button("✍️ Dejar Reseña", key=f"review_{poi['id']}", use_container_width=True):
                    show_review_form(db, poi)
        
        # Estadísticas
        st.markdown("---")
        st.subheader("📊 Estadísticas")
        
        visits_count = db.get_poi_visits_count(poi['id'])
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("👥 Visitas", visits_count)
        with col_b:
            st.metric("📝 Reseñas", poi.get('total_reviews', 0))
        with col_c:
            audio_guides = db.get_audio_guides(poi['id'])
            st.metric("🎧 Audio-Guías", len(audio_guides))


def show_review_form(db, poi):
    """Muestra el formulario para dejar una reseña"""
    
    st.markdown("### ✍️ Dejar una Reseña")
    
    with st.form(f"review_form_{poi['id']}"):
        rating = st.slider("Calificación", 1, 5, 5)
        review_text = st.text_area("Tu reseña", placeholder="Cuéntanos tu experiencia...")
        duration = st.number_input("Duración de tu visita (minutos)", min_value=0, value=poi.get('visit_duration', 30))
        
        submitted = st.form_submit_button("Enviar Reseña")
        
        if submitted and st.session_state.user_id:
            # Crear visita con reseña
            visit_data = {
                "user_id": st.session_state.user_id,
                "poi_id": poi['id'],
                "rating": rating,
                "review": review_text,
                "duration_minutes": duration,
                "is_completed": True
            }
            
            result = db.create_visit(visit_data)
            
            if result:
                st.success("¡Gracias por tu reseña! 🎉")
                
                # Actualizar rating del POI
                current_rating = poi.get('rating', 0)
                current_reviews = poi.get('total_reviews', 0)
                new_total = current_reviews + 1
                new_rating = ((current_rating * current_reviews) + rating) / new_total
                
                db.update_poi_rating(poi['id'], new_rating, new_total)
                
                # Registrar estadística
                db.create_usage_stat({
                    "user_id": st.session_state.user_id,
                    "action_type": "review",
                    "poi_id": poi['id']
                })
                
                st.rerun()
