"""
Página de Puntos de Interés
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
import config.config as config

def show(db, n8n):
    """Muestra la página de puntos de interés"""
    
    st.title("📍 Puntos de Interés")
    st.markdown("Explora lugares increíbles y planifica tu visita")
    
    pois = db.get_pois(include_city=True)
    if not pois:
        st.info("No hay puntos de interés registrados en Supabase.")
        return

    cities = db.get_cities()
    categories = db.get_poi_categories() or config.POI_CATEGORIES
    difficulties = db.get_poi_difficulties() or config.DIFFICULTY_LEVELS

    city_options = {"Todas": None}
    for city in cities:
        city_options[f"{city.get('name', 'Sin nombre')} ({city.get('country', 'N/A')})"] = city.get("id")

    prices = [float(poi.get("entry_price") or 0) for poi in pois if poi.get("entry_price") is not None]
    min_price = min(prices) if prices else 0.0
    max_price = max(prices) if prices else 0.0

    ratings = [float(poi.get("rating") or 0) for poi in pois if poi.get("rating") is not None]
    max_rating = max(ratings) if ratings else 5.0

    with st.container():
        col_filters_1, col_filters_2, col_filters_3 = st.columns([2, 1.5, 1.5])

        with col_filters_1:
            selected_city_label = st.selectbox("Ciudad", list(city_options.keys()))
            selected_city_id = city_options[selected_city_label]

            search_query = st.text_input("🔍 Buscar", placeholder="Ej: museo, plaza, parque...")

        with col_filters_2:
            selected_categories = st.multiselect("Categorías", categories, default=[])
            selected_difficulties = st.multiselect("Dificultad", difficulties, default=[])

        with col_filters_3:
            if prices:
                price_range = st.slider(
                    "Rango de precio (€)",
                    min_value=float(min_price),
                    max_value=float(max_price) if max_price > min_price else float(min_price + 1),
                    value=(float(min_price), float(max_price) if max_price > min_price else float(min_price + 1)),
                )
            else:
                price_range = (0.0, 0.0)

            min_rating_selected = st.slider(
                "Rating mínimo",
                min_value=0.0,
                max_value=max(5.0, max_rating),
                value=3.5 if max_rating >= 3.5 else max_rating,
                step=0.5,
            )

    sort_col, view_col = st.columns([1, 1])
    with sort_col:
        sort_option = st.selectbox(
            "Ordenar por",
            ["Nombre A-Z", "Rating", "Duración", "Precio (menor a mayor)", "Precio (mayor a menor)", "Más recientes"],
        )
    with view_col:
        view_mode = st.radio("Vista", ["Lista", "Tarjetas", "Tabla"], horizontal=True, index=0)

    filtered_pois = apply_poi_filters(
        pois=pois,
        search_query=search_query,
        city_id=selected_city_id,
        categories=selected_categories,
        difficulties=selected_difficulties,
        price_range=price_range,
        min_rating=min_rating_selected,
    )

    filtered_pois = sort_pois(filtered_pois, sort_option)

    st.markdown(f"**Se encontraron {len(filtered_pois)} puntos de interés.**")
    st.markdown("---")

    if not filtered_pois:
        st.info("No hay coincidencias con los criterios seleccionados.")
        return

    favorites_ids = set()
    user_id = getattr(st.session_state, "user_id", None)
    if user_id:
        favorites = db.get_user_favorites(user_id)
        favorites_ids = {fav.get("poi_id") for fav in favorites if fav.get("poi_id")}

    if view_mode == "Tabla":
        df = build_pois_dataframe(filtered_pois)
        st.dataframe(df, use_container_width=True, hide_index=True)
        return

    if view_mode == "Tarjetas":
        columns_per_row = 2
        for idx in range(0, len(filtered_pois), columns_per_row):
            row_pois = filtered_pois[idx: idx + columns_per_row]
            cols = st.columns(columns_per_row)
            for col, poi in zip(cols, row_pois):
                with col:
                    render_poi_card(db, n8n, poi, user_id, favorites_ids)
    else:
        for poi in filtered_pois:
            render_poi_list_item(db, n8n, poi, user_id, favorites_ids)


def apply_poi_filters(
    pois: List[Dict],
    search_query: Optional[str],
    city_id: Optional[str],
    categories: List[str],
    difficulties: List[str],
    price_range: tuple,
    min_rating: float,
) -> List[Dict]:
    """Aplica los filtros seleccionados a la lista de POIs."""
    filtered = pois

    if city_id:
        filtered = [poi for poi in filtered if poi.get("city_id") == city_id]

    if categories:
        filtered = [poi for poi in filtered if poi.get("category") in categories]

    if difficulties:
        filtered = [poi for poi in filtered if poi.get("difficulty_level") in difficulties]

    if price_range and price_range != (0.0, 0.0):
        min_price, max_price = price_range
        filtered = [
            poi for poi in filtered
            if poi.get("entry_price") is not None and min_price <= float(poi["entry_price"]) <= max_price
        ]

    if min_rating:
        filtered = [
            poi for poi in filtered
            if poi.get("rating") is not None and float(poi["rating"]) >= min_rating
        ]

    if search_query:
        query = search_query.lower().strip()
        filtered = [
            poi for poi in filtered
            if query in poi.get("name", "").lower()
            or query in (poi.get("description") or "").lower()
            or query in (poi.get("short_description") or "").lower()
        ]

    return filtered


def sort_pois(pois: List[Dict], sort_option: str) -> List[Dict]:
    """Ordena la lista de POIs según la opción seleccionada."""
    if sort_option == "Nombre A-Z":
        return sorted(pois, key=lambda x: x.get("name", ""))
    if sort_option == "Rating":
        return sorted(pois, key=lambda x: float(x.get("rating") or 0), reverse=True)
    if sort_option == "Duración":
        return sorted(pois, key=lambda x: x.get("visit_duration") or 0)
    if sort_option == "Precio (menor a mayor)":
        return sorted(pois, key=lambda x: float(x.get("entry_price") or 0))
    if sort_option == "Precio (mayor a menor)":
        return sorted(pois, key=lambda x: float(x.get("entry_price") or 0), reverse=True)
    if sort_option == "Más recientes":
        return sorted(pois, key=lambda x: x.get("created_at", ""), reverse=True)
    return pois


def render_poi_card(db, n8n, poi: Dict, user_id: Optional[str], favorites_ids: set):
    """Muestra un POI en formato tarjeta."""
    st.markdown(f"### {poi.get('name', 'Sin nombre')}")
    info_cols = st.columns([1, 1, 1])
    with info_cols[0]:
        st.caption(f"📌 {poi.get('category', 'Sin categoría')}")
    with info_cols[1]:
        st.caption(f"⭐ {float(poi.get('rating') or 0):.1f}")
    with info_cols[2]:
        st.caption(f"💰 €{float(poi.get('entry_price') or 0):.2f}")

    if poi.get("short_description"):
        st.write(poi["short_description"])
    elif poi.get("description"):
        st.write(poi["description"][:160] + ("..." if len(poi["description"]) > 160 else ""))

    if poi.get("cities"):
        st.caption(f"📍 {poi['cities'].get('name', 'Ciudad desconocida')}, {poi['cities'].get('country', '')}")

    action_cols = st.columns([1, 1, 1])
    with action_cols[0]:
        with st.expander("Detalles", expanded=False):
            show_poi_details(db, n8n, poi)
    with action_cols[1]:
        if user_id:
            render_favorite_button(db, poi, user_id, favorites_ids)
    with action_cols[2]:
        if st.button("🎧 Generar audio-guía", key=f"audio_card_{poi['id']}", use_container_width=True):
            st.session_state.selected_poi = poi['id']
            st.info("Conectando con el generador de audio-guías...")

    st.divider()


def render_poi_list_item(db, n8n, poi: Dict, user_id: Optional[str], favorites_ids: set):
    """Muestra un POI en formato lista detallada."""
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"### {poi.get('name', 'Sin nombre')}")
            info_cols = st.columns(4)
            with info_cols[0]:
                st.caption(f"📌 {poi.get('category', 'Sin categoría')}")
            with info_cols[1]:
                st.caption(f"⭐ {float(poi.get('rating') or 0):.1f} ({poi.get('total_reviews', 0)} reseñas)")
            with info_cols[2]:
                st.caption(f"🕐 {poi.get('visit_duration', 0)} min")
            with info_cols[3]:
                st.caption(f"💰 €{float(poi.get('entry_price') or 0):.2f}")

            if poi.get("short_description"):
                st.write(poi["short_description"])
            elif poi.get("description"):
                st.write(poi["description"][:180] + ("..." if len(poi["description"]) > 180 else ""))

            if poi.get("cities"):
                st.caption(f"📍 {poi['cities'].get('name', 'Ciudad desconocida')}, {poi['cities'].get('country', '')}")

        with col2:
            if st.button("👁️ Ver detalles", key=f"view_{poi['id']}", use_container_width=True):
                show_poi_details(db, n8n, poi)

            if user_id:
                render_favorite_button(db, poi, user_id, favorites_ids)

            if st.button("🎧 Audio-Guía", key=f"audio_{poi['id']}", use_container_width=True):
                st.session_state.selected_poi = poi['id']
                st.info("Conectando con el generador de audio-guías...")

        st.divider()


def render_favorite_button(db, poi: Dict, user_id: str, favorites_ids: set):
    """Renderiza el botón de favoritos evitando consultas repetidas."""
    is_favorite = poi.get("id") in favorites_ids
    label = "💔 Quitar" if is_favorite else "❤️ Favorito"
    if st.button(label, key=f"fav_{poi['id']}", use_container_width=True):
        if is_favorite:
            db.remove_favorite(user_id, poi['id'])
            st.success("Eliminado de favoritos")
        else:
            db.add_favorite(user_id, poi['id'])
            st.success("Añadido a favoritos")
        st.rerun()


def build_pois_dataframe(pois: List[Dict]) -> pd.DataFrame:
    """Construye un dataframe con los POIs filtrados."""
    rows = []
    for poi in pois:
        rows.append({
            "Nombre": poi.get("name"),
            "Categoría": poi.get("category"),
            "Rating": float(poi.get("rating") or 0),
            "Reseñas": poi.get("total_reviews", 0),
            "Duración (min)": poi.get("visit_duration"),
            "Precio (€)": float(poi.get("entry_price") or 0),
            "Dificultad": poi.get("difficulty_level"),
            "Ciudad": poi.get("cities", {}).get("name") if isinstance(poi.get("cities"), dict) else None,
            "País": poi.get("cities", {}).get("country") if isinstance(poi.get("cities"), dict) else None,
        })
    return pd.DataFrame(rows)


def show_poi_details(db, n8n, poi):
    """Muestra los detalles completos de un POI"""
    
    with st.expander(f"📍 {poi['name']}", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Imágenes
            if poi.get('image_urls') and len(poi['image_urls']) > 0:
                image_url = poi['image_urls'][0]
                try:
                    if image_url and image_url.strip():
                        st.image(image_url, width=600)
                    else:
                        st.image('https://via.placeholder.com/600x400', width=600)
                except Exception:
                    st.image('https://via.placeholder.com/600x400', width=600)
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
