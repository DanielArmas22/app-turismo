"""
Página de Gamificación y Logros
"""
import streamlit as st
import config

def show(db, n8n):
    """Muestra la página de gamificación"""
    
    st.title("🎮 Sistema de Gamificación")
    st.markdown("Gana puntos y desbloquea logros mientras exploras el mundo")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Debes iniciar sesión para ver tus logros")
        return
    
    # Obtener datos del usuario
    user_data = st.session_state.user_data
    achievements = db.get_user_achievements(st.session_state.user_id)
    
    # Header con información del usuario
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏆 Puntos Totales", user_data.get('total_points', 0))
    with col2:
        st.metric("🎖️ Nivel", user_data.get('level', 'Explorador Novato'))
    with col3:
        st.metric("⭐ Logros", len(achievements))
    with col4:
        # Calcular progreso al siguiente nivel
        current_points = user_data.get('total_points', 0)
        next_level_points = 1000
        progress = min(100, int((current_points / next_level_points) * 100))
        st.metric("📊 Progreso", f"{progress}%")
    
    # Barra de progreso
    st.progress(progress / 100)
    st.caption(f"Faltan {next_level_points - current_points} puntos para el siguiente nivel")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏆 Mis Logros", "🎯 Logros Disponibles", "📊 Estadísticas"])
    
    with tab1:
        show_user_achievements(db, achievements)
    
    with tab2:
        show_available_achievements(db, achievements)
    
    with tab3:
        show_gamification_stats(db, user_data, achievements)


def show_user_achievements(db, achievements):
    """Muestra los logros desbloqueados del usuario"""
    
    st.subheader("🏆 Logros Desbloqueados")
    
    if not achievements:
        st.info("Aún no has desbloqueado ningún logro. ¡Comienza a explorar para ganar tus primeros logros!")
        return
    
    # Agrupar por tipo
    achievements_by_type = {}
    for achievement in achievements:
        achievement_type = achievement.get('achievement_type', 'otros')
        if achievement_type not in achievements_by_type:
            achievements_by_type[achievement_type] = []
        achievements_by_type[achievement_type].append(achievement)
    
    # Mostrar por categoría
    for achievement_type, type_achievements in achievements_by_type.items():
        type_name = config.ACHIEVEMENT_TYPES.get(achievement_type, achievement_type.title())
        
        with st.expander(f"📁 {type_name} ({len(type_achievements)})", expanded=True):
            for achievement in type_achievements:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    badge_icon = achievement.get('badge_icon', '🏆')
                    st.markdown(f"### {badge_icon} {achievement['achievement_name']}")
                    
                    if achievement.get('achievement_description'):
                        st.write(achievement['achievement_description'])
                    
                    # Fecha de obtención
                    earned_at = achievement.get('earned_at', '')
                    if earned_at:
                        from datetime import datetime
                        date = datetime.fromisoformat(earned_at.replace('Z', '+00:00'))
                        st.caption(f"🗓️ Desbloqueado el {date.strftime('%d/%m/%Y')}")
                
                with col2:
                    points = achievement.get('points', 0)
                    st.metric("Puntos", f"+{points}")
                    
                    badge_color = achievement.get('badge_color', 'blue')
                    st.markdown(f"<div style='background-color: {badge_color}; padding: 10px; border-radius: 5px; text-align: center; color: white;'>✓ Completado</div>", unsafe_allow_html=True)
                
                st.divider()


def show_available_achievements(db, user_achievements):
    """Muestra los logros disponibles para desbloquear"""
    
    st.subheader("🎯 Logros Disponibles")
    
    # Logros predefinidos del sistema
    all_achievements = [
        {
            "name": "Primera Visita",
            "description": "Visita tu primer punto de interés",
            "type": "visitas",
            "points": 50,
            "icon": "🎯",
            "color": "green",
            "requirement": "Visita 1 POI"
        },
        {
            "name": "Explorador Novato",
            "description": "Visita 5 puntos de interés diferentes",
            "type": "explorador",
            "points": 150,
            "icon": "🗺️",
            "color": "blue",
            "requirement": "Visita 5 POIs"
        },
        {
            "name": "Coleccionista Cultural",
            "description": "Visita 5 museos diferentes",
            "type": "coleccionista",
            "points": 250,
            "icon": "🏛️",
            "color": "purple",
            "requirement": "Visita 5 museos"
        },
        {
            "name": "Primera Audio-Guía",
            "description": "Genera tu primera audio-guía",
            "type": "visitas",
            "points": 50,
            "icon": "🎧",
            "color": "blue",
            "requirement": "Genera 1 audio-guía"
        },
        {
            "name": "Coleccionista de Audio",
            "description": "Genera 10 audio-guías",
            "type": "coleccionista",
            "points": 200,
            "icon": "🎵",
            "color": "purple",
            "requirement": "Genera 10 audio-guías"
        },
        {
            "name": "Primera Reserva",
            "description": "Realiza tu primera reserva",
            "type": "visitas",
            "points": 100,
            "icon": "🎫",
            "color": "green",
            "requirement": "Realiza 1 reserva"
        },
        {
            "name": "Viajero Frecuente",
            "description": "Realiza 5 reservas",
            "type": "explorador",
            "points": 250,
            "icon": "✈️",
            "color": "blue",
            "requirement": "Realiza 5 reservas"
        },
        {
            "name": "Crítico Experto",
            "description": "Deja 10 reseñas",
            "type": "social",
            "points": 200,
            "icon": "⭐",
            "color": "gold",
            "requirement": "Deja 10 reseñas"
        },
        {
            "name": "Fotógrafo Profesional",
            "description": "Visita 10 puntos diferentes",
            "type": "experto",
            "points": 300,
            "icon": "📸",
            "color": "orange",
            "requirement": "Visita 10 POIs"
        },
        {
            "name": "Maestro Explorador",
            "description": "Alcanza 1000 puntos",
            "type": "especial",
            "points": 500,
            "icon": "👑",
            "color": "gold",
            "requirement": "1000 puntos totales"
        }
    ]
    
    # Filtrar logros ya desbloqueados
    unlocked_names = [a['achievement_name'] for a in user_achievements]
    available = [a for a in all_achievements if a['name'] not in unlocked_names]
    
    if not available:
        st.success("🎉 ¡Felicidades! Has desbloqueado todos los logros disponibles.")
        return
    
    st.write(f"**{len(available)} logros por desbloquear**")
    st.markdown("---")
    
    # Mostrar logros disponibles
    for achievement in available:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {achievement['icon']} {achievement['name']}")
            st.write(achievement['description'])
            st.caption(f"📋 Requisito: {achievement['requirement']}")
        
        with col2:
            st.metric("Puntos", f"+{achievement['points']}")
            
            # Barra de progreso simulada
            progress = 0  # En una implementación real, calcular el progreso real
            st.progress(progress / 100)
            st.caption(f"{progress}% completado")
        
        st.divider()


def show_gamification_stats(db, user_data, achievements):
    """Muestra estadísticas de gamificación"""
    
    st.subheader("📊 Tus Estadísticas")
    
    # Obtener estadísticas del usuario
    visits = db.get_user_visits(st.session_state.user_id)
    bookings = db.get_user_bookings(st.session_state.user_id)
    favorites = db.get_user_favorites(st.session_state.user_id)
    
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🗺️ Lugares Visitados", len(visits))
    with col2:
        st.metric("🎫 Reservas Realizadas", len(bookings))
    with col3:
        st.metric("❤️ Favoritos", len(favorites))
    with col4:
        total_reviews = len([v for v in visits if v.get('review')])
        st.metric("📝 Reseñas", total_reviews)
    
    st.markdown("---")
    
    # Progreso por categoría
    st.subheader("📈 Progreso por Categoría")
    
    # Simular datos de progreso
    import plotly.graph_objects as go
    
    categories = ['Cultural', 'Histórico', 'Gastronómico', 'Natural', 'Arquitectónico']
    progress_values = [75, 60, 30, 45, 85]  # En una implementación real, calcular desde la BD
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=progress_values,
            marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
        )
    ])
    
    fig.update_layout(
        title="Progreso por Categoría de POI",
        xaxis_title="Categoría",
        yaxis_title="Progreso (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Distribución de logros
    st.subheader("🏆 Distribución de Logros")
    
    if achievements:
        # Contar por tipo
        type_counts = {}
        for achievement in achievements:
            achievement_type = achievement.get('achievement_type', 'otros')
            type_name = config.ACHIEVEMENT_TYPES.get(achievement_type, achievement_type.title())
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        # Gráfico de pastel
        fig = go.Figure(data=[go.Pie(
            labels=list(type_counts.keys()),
            values=list(type_counts.values()),
            hole=.3
        )])
        
        fig.update_layout(
            title="Logros por Tipo",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aún no tienes logros para mostrar estadísticas")
    
    st.markdown("---")
    
    # Ranking (simulado)
    st.subheader("🏅 Ranking Global")
    
    st.info("🎯 Tu posición: #42 de 5,892 usuarios")
    
    # Top 5 usuarios (simulado)
    top_users = [
        {"rank": 1, "name": "María G.", "points": 2450, "level": "Maestro"},
        {"rank": 2, "name": "Carlos R.", "points": 2380, "level": "Maestro"},
        {"rank": 3, "name": "Ana M.", "points": 2150, "level": "Experto"},
        {"rank": 4, "name": "Luis P.", "points": 1980, "level": "Experto"},
        {"rank": 5, "name": "Sofia L.", "points": 1850, "level": "Experto"}
    ]
    
    for user in top_users:
        col1, col2, col3 = st.columns([1, 3, 2])
        
        with col1:
            medal = "🥇" if user['rank'] == 1 else "🥈" if user['rank'] == 2 else "🥉" if user['rank'] == 3 else f"#{user['rank']}"
            st.markdown(f"### {medal}")
        
        with col2:
            st.write(f"**{user['name']}**")
            st.caption(f"Nivel: {user['level']}")
        
        with col3:
            st.metric("Puntos", user['points'])
