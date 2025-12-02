"""
Página de Estadísticas
"""
from collections import Counter
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def show(db, n8n):
    """Muestra la página de estadísticas"""
    
    st.title("📊 Estadísticas y Análisis")
    st.markdown("Visualiza datos y tendencias del sistema")

    default_end = datetime.now()
    default_start = default_end - timedelta(days=30)

    date_range = st.date_input(
        "Rango de fechas",
        value=(default_start.date(), default_end.date()),
        max_value=default_end.date(),
        help="Selecciona el periodo para analizar tendencias y métricas.",
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range
        end_date = default_end.date()

    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)
    if start_dt > end_dt:
        st.warning("La fecha inicial no puede ser posterior a la fecha final.")
        return
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Tendencias", "🏆 Popularidad", "👤 Mi Actividad"])
    
    with tab1:
        show_trends(db, start_dt, end_dt)
    
    with tab2:
        show_popularity(db)
    
    with tab3:
        show_user_activity(db, start_dt, end_dt)


def show_trends(db, start_dt: datetime, end_dt: datetime):
    """Muestra tendencias generales del sistema basadas en datos reales."""

    st.subheader("📈 Tendencias generales")

    visits = db.get_visits_range(start_dt, end_dt)
    new_users = db.get_users_range(start_dt, end_dt)
    bookings = db.get_bookings_range(start_dt, end_dt)
    audio_guides = db.get_audio_guides_range(start_dt, end_dt)

    date_index = pd.date_range(start_dt.date(), end_dt.date(), freq="D")
    visits_series = aggregate_daily(visits, "visit_date").reindex(date_index, fill_value=0)
    users_series = aggregate_daily(new_users, "created_at").reindex(date_index, fill_value=0)
    bookings_series = aggregate_daily(bookings, "booking_date").reindex(date_index, fill_value=0)
    audio_series = aggregate_daily(audio_guides, "created_at").reindex(date_index, fill_value=0)

    summary_df = pd.DataFrame({
        "Fecha": date_index,
        "Visitas": visits_series.values,
        "Nuevos usuarios": users_series.values,
        "Reservas": bookings_series.values,
        "Audio-guías": audio_series.values,
    })

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📍 Total visitas", int(summary_df["Visitas"].sum()))
    with col2:
        st.metric("👥 Nuevos usuarios", int(summary_df["Nuevos usuarios"].sum()))
    with col3:
        st.metric("🎫 Reservas creadas", int(summary_df["Reservas"].sum()))
    with col4:
        st.metric("🎧 Audio-guías generadas", int(summary_df["Audio-guías"].sum()))

    st.markdown("---")

    st.subheader("📊 Evolución diaria por métrica")
    melted = summary_df.melt(id_vars="Fecha", var_name="Métrica", value_name="Cantidad")
    fig = px.line(
        melted,
        x="Fecha",
        y="Cantidad",
        color="Métrica",
        markers=True,
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_users = px.area(
            summary_df,
            x="Fecha",
            y="Nuevos usuarios",
            title="Altas de usuarios por día",
        )
        fig_users.update_layout(height=360)
        st.plotly_chart(fig_users, use_container_width=True)

    with col2:
        fig_bookings = px.bar(
            summary_df,
            x="Fecha",
            y="Reservas",
            title="Reservas por día",
        )
        fig_bookings.update_layout(height=360)
        st.plotly_chart(fig_bookings, use_container_width=True)

    st.subheader("🕐 Patrón de visitas por hora")
    hourly_counts = aggregate_hourly(visits, "visit_date")
    if hourly_counts.empty:
        st.info("No hay suficientes datos de visitas en el periodo seleccionado para mostrar el patrón horario.")
    else:
        fig_hours = px.bar(
            hourly_counts,
            x="Hora",
            y="Visitas",
            title="Distribución de visitas según la hora del día",
        )
        fig_hours.update_layout(height=360)
        st.plotly_chart(fig_hours, use_container_width=True)


def show_popularity(db):
    """Muestra estadísticas de popularidad de POIs basadas en visitas reales."""

    st.subheader("🏆 Lugares más populares")

    pois = db.get_pois(include_city=True)
    if not pois:
        st.info("No hay puntos de interés registrados en Supabase.")
        return

    visits = db.get_all_visits()
    visit_counter = Counter([visit.get("poi_id") for visit in visits if visit.get("poi_id")])

    poi_rows = []
    for poi in pois:
        poi_id = poi.get("id")
        poi_rows.append({
            "POI": poi.get("name", "Sin nombre"),
            "Visitas": visit_counter.get(poi_id, 0),
            "Rating": float(poi.get("rating") or 0),
            "Categoría": poi.get("category", "Sin categoría"),
            "Ciudad": poi.get("cities", {}).get("name") if isinstance(poi.get("cities"), dict) else None,
            "País": poi.get("cities", {}).get("country") if isinstance(poi.get("cities"), dict) else None,
        })

    df_pois = pd.DataFrame(poi_rows).sort_values("Visitas", ascending=False)
    top_pois = df_pois.head(10)

    st.subheader("📍 Top 10 lugares más visitados")
    fig_top = px.bar(
        top_pois.sort_values("Visitas"),
        y="POI",
        x="Visitas",
        orientation="h",
        color="Visitas",
        color_continuous_scale="Viridis",
    )
    fig_top.update_layout(height=480)
    st.plotly_chart(fig_top, use_container_width=True)

    st.subheader("⭐ Relación rating vs popularidad")
    col1, col2 = st.columns(2)

    with col1:
        fig_scatter = px.scatter(
            top_pois,
            x="Visitas",
            y="Rating",
            size="Visitas",
            color="Categoría",
            hover_data=["POI"],
            title="Rating vs visitas",
        )
        fig_scatter.update_layout(height=360)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        if not df_pois.empty:
            category_counts = df_pois["Categoría"].value_counts()
            fig_categories = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Distribución por categoría",
                hole=0.35,
            )
            fig_categories.update_layout(height=360)
            st.plotly_chart(fig_categories, use_container_width=True)
        else:
            st.info("No hay suficientes datos de categorías para mostrar la distribución.")

    st.subheader("📋 Tabla detallada")
    st.dataframe(df_pois, use_container_width=True, hide_index=True)

    st.subheader("🌍 Estadísticas por ciudad")
    cities = db.get_cities()
    if not cities:
        st.info("No hay ciudades registradas en Supabase.")
        return

    city_visit_counter = Counter(
        visit.get("points_of_interest", {}).get("city_id")
        for visit in visits
        if isinstance(visit.get("points_of_interest"), dict)
    )

    city_stats = []
    poi_city_counter = Counter([poi.get("city_id") for poi in pois if poi.get("city_id")])

    for city in cities:
        city_id = city.get("id")
        city_stats.append({
            "Ciudad": city.get("name"),
            "País": city.get("country"),
            "POIs": poi_city_counter.get(city_id, 0),
            "Visitas": city_visit_counter.get(city_id, 0),
            "Precio medio (€)": float(city.get("price") or 0),
        })

    df_cities = pd.DataFrame(city_stats).sort_values("Visitas", ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        fig_pois_city = px.bar(
            df_cities,
            x="Ciudad",
            y="POIs",
            color="POIs",
            color_continuous_scale="Blues",
            title="Puntos de interés por ciudad",
        )
        fig_pois_city.update_layout(height=360)
        st.plotly_chart(fig_pois_city, use_container_width=True)

    with col2:
        fig_popularity = px.scatter(
            df_cities,
            x="Precio medio (€)",
            y="Visitas",
            size="POIs",
            color="País",
            hover_data=["Ciudad"],
            title="Precio promedio vs visitas",
        )
        fig_popularity.update_layout(height=360)
        st.plotly_chart(fig_popularity, use_container_width=True)


def show_user_activity(db, start_dt: datetime, end_dt: datetime):
    """Muestra la actividad del usuario actual filtrada por rango de fechas."""

    st.subheader("👤 Mi actividad")

    user_id = getattr(st.session_state, "user_id", None)
    if not user_id:
        st.warning("⚠️ Debes iniciar sesión para ver tu actividad.")
        return

    visits = db.get_user_visits(user_id)
    bookings = db.get_user_bookings(user_id)
    favorites = db.get_user_favorites(user_id)
    achievements = db.get_user_achievements(user_id)

    visits = [
        visit for visit in visits
        if is_between(parse_iso_datetime(visit.get("visit_date")), start_dt, end_dt)
    ]
    bookings = [
        booking for booking in bookings
        if is_between(parse_iso_datetime(booking.get("booking_date")), start_dt, end_dt)
    ]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🗺️ Lugares visitados", len(visits))
    with col2:
        st.metric("🎫 Reservas en periodo", len(bookings))
    with col3:
        st.metric("❤️ Favoritos guardados", len(favorites))
    with col4:
        st.metric("🏆 Logros acumulados", len(achievements))

    st.markdown("---")

    if visits:
        st.subheader("📊 Visitas por categoría")
        category_counter: Dict[str, int] = {}
        for visit in visits:
            poi = visit.get("points_of_interest", {})
            category = poi.get("category", "Sin categoría")
            category_counter[category] = category_counter.get(category, 0) + 1

        df_categories = pd.DataFrame({
            "Categoría": list(category_counter.keys()),
            "Visitas": list(category_counter.values()),
        }).sort_values("Visitas", ascending=False)

        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(
                df_categories,
                names="Categoría",
                values="Visitas",
                title="Distribución de visitas por categoría",
                hole=0.4,
            )
            fig_pie.update_layout(height=320)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            fig_bar = px.bar(
                df_categories,
                x="Categoría",
                y="Visitas",
                color="Visitas",
                color_continuous_scale="Purples",
                title="Visitas por categoría",
            )
            fig_bar.update_layout(height=320)
            st.plotly_chart(fig_bar, use_container_width=True)

    if visits or bookings:
        st.subheader("📅 Últimas actividades")
        timeline_records = []

        for visit in visits:
            visit_date = parse_iso_datetime(visit.get("visit_date"))
            if visit_date:
                timeline_records.append({
                    "Fecha": visit_date,
                    "Tipo": "Visita",
                    "Lugar": visit.get("points_of_interest", {}).get("name", "Sin nombre"),
                })

        for booking in bookings:
            booking_date = parse_iso_datetime(booking.get("booking_date"))
            if booking_date:
                timeline_records.append({
                    "Fecha": booking_date,
                    "Tipo": "Reserva",
                    "Lugar": booking.get("points_of_interest", {}).get("name", "Sin nombre"),
                })

        if timeline_records:
            df_timeline = pd.DataFrame(timeline_records).sort_values("Fecha", ascending=False)
            st.dataframe(df_timeline.head(10), use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros de actividad en el periodo seleccionado.")

    if visits:
        st.subheader("⭐ Tus calificaciones")
        ratings = [visit.get("rating") for visit in visits if visit.get("rating") is not None]
        if ratings:
            col1, col2, col3 = st.columns(3)
            with col1:
                average = sum(ratings) / len(ratings)
                st.metric("Promedio otorgado", f"{average:.1f}/5.0")
            with col2:
                st.metric("Total de reseñas", len(ratings))
            with col3:
                st.metric("Calificación máxima", f"{max(ratings):.1f}/5.0")

            rating_counts = pd.Series(ratings).value_counts().sort_index()
            fig_ratings = px.bar(
                x=rating_counts.index,
                y=rating_counts.values,
                labels={"x": "Rating", "y": "Cantidad"},
                title="Distribución de calificaciones",
            )
            fig_ratings.update_traces(marker_color="#f093fb")
            fig_ratings.update_layout(height=300)
            st.plotly_chart(fig_ratings, use_container_width=True)
        else:
            st.info("Aún no has registrado calificaciones en el periodo seleccionado.")

    if bookings:
        st.subheader("💰 Evolución de gastos")
        total_spent = sum(float(booking.get("total_price") or 0) for booking in bookings)
        average_booking = total_spent / len(bookings) if bookings else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total gastado", f"€{total_spent:.2f}")
        with col2:
            st.metric("Promedio por reserva", f"€{average_booking:.2f}")
        with col3:
            st.metric("Reservas realizadas", len(bookings))

        df_bookings = pd.DataFrame(bookings)
        if not df_bookings.empty and "booking_date" in df_bookings and "total_price" in df_bookings:
            df_bookings["booking_date"] = pd.to_datetime(df_bookings["booking_date"], errors="coerce")
            df_bookings = df_bookings.dropna(subset=["booking_date"])
            df_bookings["Mes"] = df_bookings["booking_date"].dt.to_period("M")
            monthly_spending = df_bookings.groupby("Mes")["total_price"].sum().reset_index()
            monthly_spending["Mes"] = monthly_spending["Mes"].astype(str)

            fig_spending = px.line(
                monthly_spending,
                x="Mes",
                y="total_price",
                labels={"total_price": "Gasto (€)"},
                title="Gasto mensual",
            )
            fig_spending.update_traces(line_color="#43e97b", line_width=3)
            fig_spending.update_layout(height=300)
            st.plotly_chart(fig_spending, use_container_width=True)
    else:
        st.info("No se registran reservas en el periodo seleccionado.")

    if achievements:
        st.subheader("🏆 Progreso de logros")
        total_points = sum(achievement.get("points", 0) for achievement in achievements)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Puntos obtenidos", total_points)

            type_counter: Dict[str, int] = {}
            for achievement in achievements:
                type_key = achievement.get("achievement_type", "otros")
                type_counter[type_key] = type_counter.get(type_key, 0) + 1

            df_types = pd.DataFrame({
                "Tipo": list(type_counter.keys()),
                "Cantidad": list(type_counter.values()),
            })
            fig_types = px.bar(
                df_types,
                x="Tipo",
                y="Cantidad",
                color="Cantidad",
                color_continuous_scale="Sunset",
                title="Logros por tipo",
            )
            fig_types.update_layout(height=300)
            st.plotly_chart(fig_types, use_container_width=True)

        with col2:
            st.write("**Últimos logros desbloqueados**")
            for achievement in achievements[:5]:
                earned_at = parse_iso_datetime(achievement.get("earned_at"))
                icon = achievement.get("badge_icon", "🏆")
                name = achievement.get("achievement_name", "Sin nombre")
                points = achievement.get("points", 0)
                st.write(f"{icon} **{name}** (+{points} pts)")
                if earned_at:
                    st.caption(f"📅 {earned_at.strftime('%d/%m/%Y')}")
                st.divider()


def aggregate_daily(records: List[Dict], field: str) -> pd.Series:
    """Agrupa registros por día según el campo de fecha especificado."""
    if not records:
        return pd.Series(dtype="int64")
    df = pd.DataFrame(records)
    if field not in df:
        return pd.Series(dtype="int64")
    df[field] = pd.to_datetime(df[field], errors="coerce")
    df = df.dropna(subset=[field])
    if df.empty:
        return pd.Series(dtype="int64")
    df["date"] = df[field].dt.normalize()
    return df.groupby("date").size()


def aggregate_hourly(records: List[Dict], field: str) -> pd.DataFrame:
    """Cuenta registros por hora del día."""
    if not records:
        return pd.DataFrame(columns=["Hora", "Visitas"])
    df = pd.DataFrame(records)
    if field not in df:
        return pd.DataFrame(columns=["Hora", "Visitas"])
    df[field] = pd.to_datetime(df[field], errors="coerce")
    df = df.dropna(subset=[field])
    if df.empty:
        return pd.DataFrame(columns=["Hora", "Visitas"])
    df["Hora"] = df[field].dt.hour
    hourly = df.groupby("Hora").size().reset_index(name="Visitas")
    return hourly


def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    """Convierte un string ISO8601 a datetime."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def is_between(date_value: Optional[datetime], start_dt: datetime, end_dt: datetime) -> bool:
    """Verifica si una fecha está dentro del rango indicado."""
    if not date_value:
        return False
    return start_dt <= date_value <= end_dt
