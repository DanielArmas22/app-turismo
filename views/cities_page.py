"""
Página de Exploración de Ciudades
"""
import streamlit as st
import math
from collections import Counter
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

import config
from .bookings_page import create_booking as bookings_create_booking
from .audio_page import generate_audio_guide as audio_generate

def show(db, n8n):
    """Muestra la página de ciudades"""
    
    st.title("🌍 Explorar Ciudades")
    st.caption("Descubre destinos únicos y accede rápidamente a sus principales atracciones.")

    cities = db.get_cities()
    if not cities:
        st.info("Aún no hay ciudades registradas en Supabase.")
        return

    selected_city_id = st.session_state.get("selected_city") if st.session_state.get("show_city_detail") else None
    if selected_city_id:
        city_detail = db.get_city(selected_city_id)
        if city_detail:
            render_city_detail(db, n8n, city_detail)
            st.markdown("---")
        else:
            st.session_state.show_city_detail = False

    pois = db.get_pois(include_city=False)
    pois_by_city = Counter([poi.get("city_id") for poi in pois if poi.get("city_id")])

    countries = sorted({city.get("country") for city in cities if city.get("country")})
    languages = sorted({city.get("language") for city in cities if city.get("language")})
    currencies = sorted({city.get("currency") for city in cities if city.get("currency")})

    prices = [float(city.get("price", 0) or 0) for city in cities if city.get("price") is not None]
    min_price = math.floor(min(prices)) if prices else 0
    max_price = math.ceil(max(prices)) if prices else 0

    with st.container():
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([2, 1.2, 1.2, 1.2])

        with filter_col1:
            search_query = st.text_input("🔍 Buscar ciudad", placeholder="Ej: Madrid, París, Roma...")

        with filter_col2:
            selected_countries = st.multiselect("País", countries, default=[])

        with filter_col3:
            selected_languages = st.multiselect("Idioma", languages, default=[])

        with filter_col4:
            currency_filter = st.multiselect("Moneda", currencies, default=[])

    if prices:
        price_range = st.slider(
            "Precio (€)",
            min_value=min_price,
            max_value=max_price if max_price > min_price else min_price + 1,
            value=(min_price, max_price if max_price > min_price else min_price + 1),
        )
    else:
        price_range = (0, 0)

    sort_col1, sort_col2 = st.columns([1, 1])
    with sort_col1:
        sort_option = st.selectbox(
            "Ordenar por",
            ["Nombre A-Z", "Nombre Z-A", "Precio (menor a mayor)", "Precio (mayor a menor)", "Últimas ciudades"],
        )
    with sort_col2:
        view_mode = st.radio("Vista", ["Tarjetas", "Tabla"], horizontal=True, index=0)

    # Aplicar filtros
    filtered_cities = cities

    if search_query:
        query = search_query.strip().lower()
        filtered_cities = [
            city for city in filtered_cities
            if query in city.get("name", "").lower()
            or query in (city.get("description") or "").lower()
        ]

    if selected_countries:
        filtered_cities = [city for city in filtered_cities if city.get("country") in selected_countries]

    if selected_languages:
        filtered_cities = [city for city in filtered_cities if city.get("language") in selected_languages]

    if currency_filter:
        filtered_cities = [city for city in filtered_cities if city.get("currency") in currency_filter]

    if prices:
        min_selected, max_selected = price_range
        filtered_cities = [
            city for city in filtered_cities
            if city.get("price") is not None and min_selected <= float(city["price"]) <= max_selected
        ]

    # Ordenar
    if sort_option == "Nombre A-Z":
        filtered_cities = sorted(filtered_cities, key=lambda x: x.get("name", ""))
    elif sort_option == "Nombre Z-A":
        filtered_cities = sorted(filtered_cities, key=lambda x: x.get("name", ""), reverse=True)
    elif sort_option == "Precio (menor a mayor)":
        filtered_cities = sorted(filtered_cities, key=lambda x: float(x.get("price") or 0))
    elif sort_option == "Precio (mayor a menor)":
        filtered_cities = sorted(filtered_cities, key=lambda x: float(x.get("price") or 0), reverse=True)
    elif sort_option == "Últimas ciudades":
        filtered_cities = sorted(filtered_cities, key=lambda x: x.get("created_at", ""), reverse=True)

    st.markdown(f"**Se muestran {len(filtered_cities)} ciudades de un total de {len(cities)} disponibles.**")
    st.markdown("---")

    if not filtered_cities:
        st.info("No se encontraron ciudades con los filtros seleccionados.")
    else:
        if view_mode == "Tarjetas":
            columns_per_row = 3
            for idx in range(0, len(filtered_cities), columns_per_row):
                row_cities = filtered_cities[idx: idx + columns_per_row]
                cols = st.columns(columns_per_row)
                for col, city in zip(cols, row_cities):
                    with col:
                        render_city_card(db, n8n, city, pois_by_city)
        else:
            dataframe = build_cities_dataframe(filtered_cities, pois_by_city)
            st.dataframe(
                dataframe,
                use_container_width=True,
                hide_index=True,
            )

    # Estadísticas
    st.markdown("---")
    st.subheader("📊 Resumen de Ciudades")

    total_pois = sum(pois_by_city.values())
    avg_price = (sum(float(c.get("price") or 0) for c in filtered_cities) / len(filtered_cities)) if filtered_cities else 0

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.metric("Ciudades filtradas", len(filtered_cities))
    with stat_col2:
        st.metric("Precio promedio", f"€{avg_price:.2f}")
    with stat_col3:
        st.metric("POIs activos", total_pois)


def render_city_card(db, n8n, city, pois_by_city: Counter):
    """Renderiza una tarjeta informativa para una ciudad."""
    placeholder_image = "https://images.unsplash.com/photo-1505761671935-60b3a7427bad?auto=format&fit=crop&w=600&q=80"
    raw_url = city.get("image_url") or placeholder_image
    image_url = raw_url.replace("'", "%27")

    st.markdown(f"""
    <div class="city-card fade-in" style="background-image: url('{image_url}'); margin-bottom:0.75rem;">
        <div class="city-overlay">
            <h4>{city.get('name', 'Sin nombre')}</h4>
            <div class="city-meta">{city.get('country', 'N/A')} • €{float(city.get('price') or 0):.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    description = city.get("short_description") or city.get("description")
    if description:
        st.caption(description[:150] + ("..." if len(description) > 150 else ""))

    col_left, col_right = st.columns(2)
    with col_left:
        st.metric("Precio medio", f"€{float(city.get('price') or 0):.2f}")
    with col_right:
        st.metric("POIs activos", pois_by_city.get(city.get("id"), 0))

    if st.button("Ver ciudad", key=f"open_city_{city['id']}", use_container_width=True):
        st.session_state.selected_city = city["id"]
        st.session_state.show_city_detail = True
        st.rerun()


def build_cities_dataframe(cities: List[Dict], pois_by_city: Counter) -> pd.DataFrame:
    """Construye un dataframe con información relevante de ciudades."""
    rows = []
    for city in cities:
        rows.append({
            "Ciudad": city.get("name"),
            "País": city.get("country"),
            "Precio (€)": float(city.get("price") or 0),
            "Idioma": city.get("language"),
            "Zona horaria": city.get("timezone"),
            "POIs activos": pois_by_city.get(city.get("id"), 0),
            "Última actualización": city.get("updated_at"),
        })
    return pd.DataFrame(rows)


def render_city_detail(db, n8n, city: Dict):
    """Muestra una vista enriquecida con los detalles de una ciudad."""
    st.markdown(f"## 🏙️ {city.get('name', 'Ciudad desconocida')}")
    st.caption(f"{city.get('country', 'País no disponible')} • Idioma: {city.get('language', 'N/D')}")

    pois = db.get_pois(city_id=city['id'])
    poi_count = len(pois)
    avg_rating = (
        sum(float(poi.get('rating') or 0) for poi in pois) / poi_count
        if poi_count else 0
    )

    hero_col, info_col = st.columns([2, 1])
    with hero_col:
        image_url = city.get('image_url') or "https://images.unsplash.com/photo-1491557345352-5929e343eb89?auto=format&fit=crop&w=1200&q=80"
        st.image(image_url, use_container_width=True)

        description = city.get('description') or "Sin descripción disponible."
        st.markdown(f"**Descripción**\n\n{description}")

        tag_cols = st.columns(3)
        if city.get('timezone'):
            tag_cols[0].info(f"🕐 Zona horaria\n\n{city['timezone']}")
        if city.get('currency'):
            tag_cols[1].info(f"💱 Moneda\n\n{city['currency']}")
        if city.get('language'):
            tag_cols[2].info(f"🗣️ Idioma\n\n{city['language']}")

    with info_col:
        st.metric("Precio medio", f"€{float(city.get('price') or 0):.2f}")
        st.metric("POIs registrados", poi_count)
        st.metric("Rating promedio", f"{avg_rating:.2f}")

        if city.get('latitude') and city.get('longitude'):
            map_df = pd.DataFrame([{
                "lat": float(city['latitude']),
                "lon": float(city['longitude'])
            }])
            st.map(map_df, zoom=12)

    st.markdown("### 📍 Puntos de interés destacados")
    if pois:
        top_pois = sorted(pois, key=lambda poi: poi.get('rating', 0), reverse=True)[:3]
        cols = st.columns(len(top_pois))
        for col, poi in zip(cols, top_pois):
            with col:
                st.markdown(f"**{poi.get('name', 'Sin nombre')}**")
                st.caption(f"{poi.get('category', 'Sin categoría')} • ⭐ {poi.get('rating', 0):.1f} • 💰 €{float(poi.get('entry_price') or 0):.2f}")
                snippet = poi.get('short_description') or poi.get('description', '')
                if snippet:
                    st.write(snippet[:120] + ("..." if len(snippet) > 120 else ""))
    else:
        st.info("Todavía no se han registrado puntos de interés para esta ciudad.")

    st.markdown("### ✨ Acciones disponibles")
    tab_booking, tab_audio = st.tabs(["🎫 Reservar experiencia", "🎧 Generar audio-guía"])

    with tab_booking:
        render_booking_form(db, n8n, city, pois)

    with tab_audio:
        render_audio_form(db, n8n, city, pois)

    if st.button("← Volver al listado de ciudades", use_container_width=True, type="secondary"):
        st.session_state.show_city_detail = False
        st.session_state.selected_city = None
        st.rerun()


def render_booking_form(db, n8n, city: Dict, pois: List[Dict]):
    """Formulario compacto para crear una reserva desde la vista de ciudad."""
    if not st.session_state.user_id:
        st.warning("Debes iniciar sesión para crear una reserva.")
        return

    if not pois:
        st.info("No hay puntos de interés disponibles para reservar en esta ciudad.")
        return

    poi_options = {
        f"{poi.get('name')} • €{float(poi.get('entry_price') or city.get('price') or 0):.2f}": poi
        for poi in pois
    }

    with st.form(f"booking_city_form_{city['id']}"):
        selected_option = st.selectbox("Selecciona el punto de interés", list(poi_options.keys()))
        selected_poi = poi_options[selected_option]

        today = datetime.now().date()
        default_time = datetime.now().replace(second=0, microsecond=0)

        booking_date = st.date_input("Fecha", value=today, min_value=today)
        booking_time = st.time_input("Hora", value=default_time.time())
        number_of_people = st.number_input("Número de personas", min_value=1, max_value=10, value=2)

        special_requirements = st.text_area("Requerimientos especiales", placeholder="Dietas, accesibilidad, notas para el guía...", height=80)
        contact_phone = st.text_input("Teléfono de contacto", value=(st.session_state.user_data or {}).get('phone', ""))

        contact_email_default = st.session_state.user_email or (st.session_state.user_data or {}).get('email', "")
        contact_email = st.text_input("Email de contacto", value=contact_email_default)

        payment_method = st.selectbox("Método de pago", ["stripe", "paypal", "transferencia"], index=0)

        price_per_person = float(selected_poi.get('entry_price') or city.get('price') or 0)
        total_price = price_per_person * number_of_people
        st.caption(f"💶 Total estimado: €{total_price:.2f}")

        submitted = st.form_submit_button("Confirmar reserva", use_container_width=True)
        if submitted:
            if not contact_email:
                st.warning("Por favor indica un correo electrónico de contacto.")
                return
            st.session_state.user_email = contact_email
            bookings_create_booking(
                db,
                n8n,
                selected_poi,
                booking_date,
                booking_time,
                number_of_people,
                total_price,
                payment_method,
                special_requirements,
                contact_phone
            )


def render_audio_form(db, n8n, city: Dict, pois: List[Dict]):
    """Formulario reducido para solicitar una audio-guía desde la vista de ciudad."""
    if not st.session_state.user_id:
        st.warning("Debes iniciar sesión para generar audio-guías personalizadas.")
        return

    if not pois:
        st.info("Aún no hay puntos de interés con contenido disponible para esta ciudad.")
        return

    poi_options = {poi.get('name', 'Sin nombre'): poi for poi in pois}

    with st.form(f"audio_city_form_{city['id']}"):
        selected_name = st.selectbox("Selecciona el punto de interés", list(poi_options.keys()))
        selected_poi = poi_options[selected_name]

        additional_context = st.text_area(
            "Contexto adicional para la narración",
            placeholder="Describe el tono deseado, idioma alternativo o datos que quieras destacar...",
            height=100
        )

        voice_labels = list(config.AUDIO_VOICES.keys())
        default_voice = "Echo" if "Echo" in config.AUDIO_VOICES else voice_labels[0]
        selected_voice = st.selectbox("Voz IA", voice_labels, index=voice_labels.index(default_voice))
        custom_voice = st.text_input("Voz personalizada (opcional)")
        voice_id = custom_voice.strip() or config.AUDIO_VOICES[selected_voice]

        submitted = st.form_submit_button("Generar audio-guía", use_container_width=True)
        if submitted:
            audio_generate(db, n8n, selected_poi, additional_context, voice_id)
