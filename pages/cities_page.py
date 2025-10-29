"""
Página de Exploración de Ciudades
"""
import streamlit as st
import config

def show(db, n8n):
    """Muestra la página de ciudades"""
    
    st.title("🌍 Explorar Ciudades")
    st.markdown("Descubre destinos increíbles alrededor del mundo")
    
    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Buscar ciudad", placeholder="Ej: Madrid, París...")
    
    with col2:
        country_filter = st.selectbox("País", ["Todos"] + ["España", "Francia", "Italia", "Alemania"])
    
    with col3:
        sort_by = st.selectbox("Ordenar por", ["Nombre", "Precio", "Popularidad"])
    
    st.markdown("---")
    
    # Obtener ciudades
    cities = db.get_cities()
    
    # Aplicar filtros
    if search_query:
        cities = [c for c in cities if search_query.lower() in c['name'].lower()]
    
    if country_filter != "Todos":
        cities = [c for c in cities if c['country'] == country_filter]
    
    # Mostrar ciudades
    if not cities:
        st.info("No se encontraron ciudades con los filtros aplicados")
    else:
        # Grid de ciudades
        cols_per_row = 3
        for i in range(0, len(cities), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(cities):
                    city = cities[i + j]
                    with col:
                        # Card de ciudad
                        st.image(
                            city.get('image_url', 'https://via.placeholder.com/400x300'),
                            width=400
                        )
                        
                        st.subheader(city['name'])
                        st.caption(f"📍 {city['country']}")
                        
                        if city.get('description'):
                            st.write(city['description'][:100] + "...")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Precio", f"€{city['price']}")
                        with col_b:
                            # Contar POIs de esta ciudad
                            pois_count = len(db.get_pois(city_id=city['id']))
                            st.metric("POIs", pois_count)
                        
                        if st.button("Ver Detalles", key=f"city_btn_{city['id']}", use_container_width=True):
                            st.session_state.selected_city = city['id']
                            show_city_details(db, n8n, city)
    
    # Estadísticas
    st.markdown("---")
    st.subheader("📊 Estadísticas de Ciudades")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Ciudades", len(cities))
    with col2:
        avg_price = sum(c['price'] for c in cities) / len(cities) if cities else 0
        st.metric("Precio Promedio", f"€{avg_price:.2f}")
    with col3:
        total_pois = len(db.get_pois())
        st.metric("Total POIs", total_pois)


def show_city_details(db, n8n, city):
    """Muestra los detalles de una ciudad en un modal"""
    
    with st.expander(f"📍 Detalles de {city['name']}", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(city.get('image_url', 'https://via.placeholder.com/600x400'))
            
            st.markdown(f"### {city['name']}, {city['country']}")
            st.write(city.get('description', 'Sin descripción disponible'))
            
            # Información adicional
            if city.get('language'):
                st.info(f"🗣️ Idioma: {city['language']}")
            
            if city.get('timezone'):
                st.info(f"🕐 Zona horaria: {city['timezone']}")
        
        with col2:
            st.metric("💰 Precio", f"€{city['price']}")
            st.metric("🌐 País", city['country'])
            
            # Coordenadas
            if city.get('latitude') and city.get('longitude'):
                st.write(f"📍 **Coordenadas:**")
                st.write(f"Lat: {city['latitude']}")
                st.write(f"Lng: {city['longitude']}")
            
            # Botones de acción
            st.markdown("---")
            
            if st.button("🎧 Ver Audio-Guías", key=f"audio_{city['id']}", use_container_width=True):
                st.info("Redirigiendo a audio-guías...")
            
            if st.button("📍 Ver Puntos de Interés", key=f"pois_{city['id']}", use_container_width=True):
                st.session_state.selected_city = city['id']
                st.info("Redirigiendo a POIs...")
        
        # POIs de la ciudad
        st.markdown("---")
        st.subheader("📍 Puntos de Interés")
        
        pois = db.get_pois(city_id=city['id'])
        
        if pois:
            for poi in pois[:5]:  # Mostrar solo los primeros 5
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    
                    with col_a:
                        st.write(f"**{poi['name']}**")
                        st.caption(f"{poi.get('category', 'Sin categoría')} • {poi.get('visit_duration', 0)} min")
                    
                    with col_b:
                        rating = poi.get('rating', 0)
                        st.write(f"⭐ {rating:.1f}")
                    
                    with col_c:
                        if st.button("Ver", key=f"poi_detail_{poi['id']}"):
                            st.session_state.selected_poi = poi['id']
                    
                    st.divider()
            
            if len(pois) > 5:
                st.info(f"Y {len(pois) - 5} puntos de interés más...")
        else:
            st.warning("No hay puntos de interés disponibles para esta ciudad")
