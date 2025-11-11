"""
Página de Gamificación y Logros
"""
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st

import config


def show(db, n8n):
    """Muestra la página de gamificación"""

    st.title("🎮 Sistema de Gamificación")
    st.markdown("Gana puntos y desbloquea logros mientras exploras el mundo.")

    user_id = getattr(st.session_state, "user_id", None)
    if not user_id:
        st.warning("⚠️ Debes iniciar sesión para ver tus logros.")
        return

    user_data = getattr(st.session_state, "user_data", None)
    if not user_data:
        user_data = db.get_user_by_id(user_id)
        if not user_data:
            st.error("No fue posible cargar la información del usuario desde Supabase.")
            return
        st.session_state.user_data = user_data

    achievements = db.get_user_achievements(user_id)
    all_users = db.get_all_users()

    total_points = user_data.get("total_points") or 0
    level = user_data.get("level", "Explorador Novato")
    total_logros = len(achievements)
    ranking, progress_pct, leader_points = compute_user_position(total_points, all_users, user_id)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏆 Puntos totales", total_points)
    with col2:
        st.metric("🎖️ Nivel actual", level)
    with col3:
        st.metric("⭐ Logros obtenidos", total_logros)
    with col4:
        ranking_text = f"#{ranking}" if ranking else "—"
        total_users = len(all_users)
        st.metric("🏅 Ranking global", ranking_text, help=f"Entre {total_users} usuarios registrados" if total_users else None)

    if leader_points > 0:
        st.progress(progress_pct / 100)
        if ranking and ranking > 1:
            st.caption(f"Te faltan {max(leader_points - total_points, 0)} puntos para alcanzar al líder.")
        else:
            st.caption("¡Eres el usuario con más puntos del sistema!")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🏆 Mis logros", "🎯 Oportunidades", "📊 Estadísticas"])

    with tab1:
        show_user_achievements(achievements)

    with tab2:
        show_available_achievements(db, achievements)

    with tab3:
        show_gamification_stats(db, user_data, achievements, all_users)


def show_user_achievements(achievements: List[Dict]):
    """Muestra los logros desbloqueados del usuario"""

    st.subheader("🏆 Logros desbloqueados")

    if not achievements:
        st.info("Aún no has desbloqueado ningún logro. Explora y participa para comenzar a sumar puntos.")
        return

    achievements_by_type: Dict[str, List[Dict]] = {}
    for achievement in achievements:
        achievement_type = achievement.get("achievement_type", "otros")
        achievements_by_type.setdefault(achievement_type, []).append(achievement)

    for achievement_type, group in achievements_by_type.items():
        type_name = config.ACHIEVEMENT_TYPES.get(achievement_type, achievement_type.title())

        with st.expander(f"📁 {type_name} ({len(group)})", expanded=True):
            for achievement in group:
                col1, col2 = st.columns([3, 1])

                with col1:
                    badge_icon = achievement.get("badge_icon", "🏆")
                    st.markdown(f"### {badge_icon} {achievement.get('achievement_name', 'Logro sin nombre')}")

                    description = achievement.get("achievement_description")
                    if description:
                        st.write(description)

                    earned_at = format_datetime(achievement.get("earned_at"))
                    if earned_at:
                        st.caption(f"🗓️ Desbloqueado el {earned_at.strftime('%d/%m/%Y')}")

                with col2:
                    points = achievement.get("points", 0)
                    st.metric("Puntos", f"+{points}")

                    badge_color = achievement.get("badge_color") or "#1d4ed8"
                    st.markdown(
                        f"<div style='background-color: {badge_color}; padding: 10px; border-radius: 5px; text-align: center; color: white;'>✓ Completado</div>",
                        unsafe_allow_html=True,
                    )

                st.divider()


def show_available_achievements(db, user_achievements: List[Dict]):
    """Muestra los logros que aún puede desbloquear el usuario."""

    st.subheader("🎯 Oportunidades de logros")

    unlocked_names = {item.get("achievement_name") for item in user_achievements}

    catalog = db.get_all_achievements()
    unique_catalog: Dict[str, Dict] = {}
    for achievement in catalog:
        name = achievement.get("achievement_name")
        if name and name not in unique_catalog:
            unique_catalog[name] = achievement

    available = [data for name, data in unique_catalog.items() if name not in unlocked_names]

    if not available:
        st.success("🎉 ¡Felicidades! Has alcanzado todos los logros disponibles hasta el momento.")
        return

    st.write(f"Tienes **{len(available)}** logros pendientes por desbloquear.")
    st.markdown("---")

    for achievement in available:
        col1, col2 = st.columns([3, 1])

        with col1:
            icon = achievement.get("badge_icon", "🎯")
            name = achievement.get("achievement_name", "Logro sin nombre")
            st.markdown(f"### {icon} {name}")

            description = achievement.get("achievement_description")
            if description:
                st.write(description)

            achievement_type = achievement.get("achievement_type")
            if achievement_type:
                type_label = config.ACHIEVEMENT_TYPES.get(achievement_type, achievement_type.title())
                st.caption(f"Tipo: {type_label}")

        with col2:
            points = achievement.get("points", 0)
            st.metric("Puntos potenciales", f"+{points}")

            last_time = format_datetime(achievement.get("earned_at"))
            if last_time:
                st.caption(f"Última vez otorgado: {last_time.strftime('%d/%m/%Y')}")

        st.divider()


def show_gamification_stats(db, user_data: Dict, achievements: List[Dict], all_users: List[Dict]):
    """Muestra estadísticas basadas en datos reales del sistema."""

    st.subheader("📊 Resumen de actividad")

    user_id = user_data.get("id") or getattr(st.session_state, "user_id")

    visits = db.get_user_visits(user_id)
    bookings = db.get_user_bookings(user_id)
    favorites = db.get_user_favorites(user_id)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🗺️ Visitas registradas", len(visits))
    with col2:
        st.metric("🎫 Reservas realizadas", len(bookings))
    with col3:
        st.metric("❤️ Lugares en favoritos", len(favorites))
    with col4:
        reviews_count = len([visit for visit in visits if visit.get("review")])
        st.metric("📝 Reseñas enviadas", reviews_count)

    st.markdown("---")

    if visits:
        st.subheader("📈 Categorías más visitadas")
        category_counts: Dict[str, int] = {}
        for visit in visits:
            poi = visit.get("points_of_interest", {})
            category = poi.get("category", "Sin categoría")
            category_counts[category] = category_counts.get(category, 0) + 1

        df_categories = pd.DataFrame(
            {"Categoría": list(category_counts.keys()), "Visitas": list(category_counts.values())}
        ).sort_values("Visitas", ascending=False)

        fig = px.bar(
            df_categories,
            x="Categoría",
            y="Visitas",
            text_auto=True,
            color="Visitas",
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aún no registras visitas para analizar tus preferencias.")

    st.markdown("---")

    st.subheader("🏆 Distribución de logros")
    if achievements:
        type_counts: Dict[str, int] = {}
        for achievement in achievements:
            achievement_type = achievement.get("achievement_type", "otros")
            label = config.ACHIEVEMENT_TYPES.get(achievement_type, achievement_type.title())
            type_counts[label] = type_counts.get(label, 0) + 1

        df_types = pd.DataFrame(
            {"Tipo": list(type_counts.keys()), "Cantidad": list(type_counts.values())}
        )
        fig = px.pie(df_types, names="Tipo", values="Cantidad", hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Todavía no hay logros para mostrar una distribución por tipo.")

    st.markdown("---")

    st.subheader("🏅 Ranking global")
    if not all_users:
        st.info("No hay suficientes datos de otros usuarios para generar un ranking.")
        return

    sorted_users = sorted(all_users, key=lambda user: user.get("total_points") or 0, reverse=True)
    top_users = sorted_users[:5]

    for position, user in enumerate(top_users, start=1):
        col1, col2, col3 = st.columns([1, 3, 2])

        with col1:
            medal = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else f"#{position}"
            st.markdown(f"### {medal}")

        with col2:
            st.write(f"**{user.get('name', 'Usuario sin nombre')}**")
            st.caption(f"Nivel: {user.get('level', 'Sin nivel')}")

        with col3:
            st.metric("Puntos", user.get("total_points", 0))

        st.divider()


def compute_user_position(total_points: int, all_users: List[Dict], user_id: str) -> Tuple[Optional[int], float, int]:
    """Calcula la posición del usuario y la proporción frente al líder."""
    if not all_users:
        return None, 0.0, 0

    sorted_users = sorted(all_users, key=lambda user: user.get("total_points") or 0, reverse=True)
    leader_points = sorted_users[0].get("total_points") or 0

    ranking = next((index + 1 for index, user in enumerate(sorted_users) if user.get("id") == user_id), None)

    if leader_points == 0:
        return ranking, 0.0, leader_points

    progress_pct = min(100.0, (total_points / leader_points) * 100) if leader_points else 0.0
    return ranking, progress_pct, leader_points


def format_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Convierte una cadena ISO en objeto datetime."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except Exception:
        return None
