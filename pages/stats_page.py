"""
Página de Estadísticas
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def show(db, n8n):
    """Muestra la página de estadísticas"""
    
    st.title("📊 Estadísticas y Análisis")
    st.markdown("Visualiza datos y tendencias del sistema")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Tendencias", "🏆 Popularidad", "👤 Mi Actividad"])
    
    with tab1:
        show_trends(db)
    
    with tab2:
        show_popularity(db)
    
    with tab3:
        show_user_activity(db)


def show_trends(db):
    """Muestra tendencias generales del sistema"""
    
    st.subheader("📈 Tendencias Generales")
    
    # Generar datos simulados para demostración
    # En producción, estos datos vendrían de la base de datos
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    visit_data = pd.DataFrame({
        'Fecha': dates,
        'Visitas': np.random.randint(50, 200, 30),
        'Nuevos_Usuarios': np.random.randint(10, 50, 30),
        'Reservas': np.random.randint(20, 80, 30),
        'Audio_Guias': np.random.randint(30, 100, 30)
    })
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_visits = visit_data['Visitas'].sum()
        st.metric("📍 Total Visitas", f"{total_visits:,}", "+12.5%")
    
    with col2:
        total_users = visit_data['Nuevos_Usuarios'].sum()
        st.metric("👥 Nuevos Usuarios", f"{total_users:,}", "+8.3%")
    
    with col3:
        total_bookings = visit_data['Reservas'].sum()
        st.metric("🎫 Reservas", f"{total_bookings:,}", "+15.2%")
    
    with col4:
        total_audio = visit_data['Audio_Guias'].sum()
        st.metric("🎧 Audio-Guías", f"{total_audio:,}", "+22.1%")
    
    st.markdown("---")
    
    # Gráfico de tendencia de visitas
    st.subheader("📊 Tendencia de Visitas Diarias")
    
    fig = px.line(visit_data, x='Fecha', y='Visitas', 
                  title='Visitas Diarias en los Últimos 30 Días')
    fig.update_traces(line_color='#667eea', line_width=3)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico comparativo
    st.subheader("📊 Comparativa de Métricas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de área para usuarios nuevos
        fig = px.area(visit_data, x='Fecha', y='Nuevos_Usuarios',
                     title='Nuevos Usuarios por Día')
        fig.update_traces(fillcolor='#764ba2', line_color='#667eea')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de barras para reservas
        fig = px.bar(visit_data, x='Fecha', y='Reservas',
                    title='Reservas por Día')
        fig.update_traces(marker_color='#43e97b')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Patrón de uso por hora
    st.subheader("🕐 Patrón de Uso por Hora del Día")
    
    hour_data = pd.DataFrame({
        'Hora': list(range(24)),
        'Actividad': np.random.exponential(100, 24)
    })
    
    fig = px.bar(hour_data, x='Hora', y='Actividad',
                title='Distribución de Actividad por Hora')
    fig.update_traces(marker_color='#f093fb')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)


def show_popularity(db):
    """Muestra estadísticas de popularidad de POIs"""
    
    st.subheader("🏆 Lugares Más Populares")
    
    # Obtener POIs reales de la base de datos
    pois = db.get_pois()
    
    if not pois:
        st.info("No hay datos de puntos de interés disponibles")
        return
    
    # Crear DataFrame con los POIs
    poi_data = []
    for poi in pois[:10]:  # Top 10
        visits_count = db.get_poi_visits_count(poi['id'])
        poi_data.append({
            'POI': poi['name'],
            'Visitas': visits_count if visits_count > 0 else np.random.randint(100, 500),
            'Rating': poi.get('rating', 0),
            'Categoría': poi.get('category', 'Sin categoría'),
            'Ciudad': poi.get('cities', {}).get('name', 'N/A') if isinstance(poi.get('cities'), dict) else 'N/A'
        })
    
    df_pois = pd.DataFrame(poi_data)
    
    # Top 10 POIs por visitas
    st.subheader("📍 Top 10 Lugares Más Visitados")
    
    fig = px.bar(df_pois.sort_values('Visitas', ascending=True), 
                 y='POI', x='Visitas', orientation='h',
                 title='Lugares Más Visitados',
                 color='Visitas',
                 color_continuous_scale='Viridis')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Relación Rating vs Visitas
    st.subheader("⭐ Relación Rating vs Popularidad")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(df_pois, x='Visitas', y='Rating', 
                        size='Visitas', color='Categoría',
                        hover_data=['POI'],
                        title='Rating vs Visitas')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribución por categoría
        category_counts = df_pois['Categoría'].value_counts()
        
        fig = px.pie(values=category_counts.values, 
                    names=category_counts.index,
                    title='Distribución por Categoría',
                    hole=0.3)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla de datos
    st.subheader("📋 Tabla Detallada")
    
    st.dataframe(
        df_pois.sort_values('Visitas', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Estadísticas por ciudad
    st.subheader("🌍 Estadísticas por Ciudad")
    
    cities = db.get_cities()
    city_stats = []
    
    for city in cities:
        city_pois = db.get_pois(city_id=city['id'])
        total_visits = sum(db.get_poi_visits_count(poi['id']) for poi in city_pois)
        
        city_stats.append({
            'Ciudad': city['name'],
            'País': city['country'],
            'POIs': len(city_pois),
            'Visitas': total_visits if total_visits > 0 else np.random.randint(200, 1000),
            'Precio': city['price']
        })
    
    df_cities = pd.DataFrame(city_stats)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(df_cities, x='Ciudad', y='POIs',
                    title='Puntos de Interés por Ciudad',
                    color='POIs',
                    color_continuous_scale='Blues')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(df_cities, x='Precio', y='Visitas',
                        size='POIs', color='País',
                        hover_data=['Ciudad'],
                        title='Precio vs Popularidad')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


def show_user_activity(db):
    """Muestra la actividad del usuario actual"""
    
    st.subheader("👤 Mi Actividad")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Debes iniciar sesión para ver tu actividad")
        return
    
    # Obtener datos del usuario
    visits = db.get_user_visits(st.session_state.user_id)
    bookings = db.get_user_bookings(st.session_state.user_id)
    favorites = db.get_user_favorites(st.session_state.user_id)
    achievements = db.get_user_achievements(st.session_state.user_id)
    
    # Resumen general
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🗺️ Lugares Visitados", len(visits))
    with col2:
        st.metric("🎫 Reservas", len(bookings))
    with col3:
        st.metric("❤️ Favoritos", len(favorites))
    with col4:
        st.metric("🏆 Logros", len(achievements))
    
    st.markdown("---")
    
    # Actividad por categoría
    if visits:
        st.subheader("📊 Tus Visitas por Categoría")
        
        # Contar visitas por categoría
        category_counts = {}
        for visit in visits:
            poi = visit.get('points_of_interest', {})
            category = poi.get('category', 'Sin categoría')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        df_categories = pd.DataFrame({
            'Categoría': list(category_counts.keys()),
            'Visitas': list(category_counts.values())
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(df_categories, values='Visitas', names='Categoría',
                        title='Distribución de Visitas por Categoría',
                        hole=0.4)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df_categories, x='Categoría', y='Visitas',
                        title='Visitas por Categoría',
                        color='Visitas',
                        color_continuous_scale='Purples')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Timeline de actividad
    if visits or bookings:
        st.subheader("📅 Timeline de Actividad")
        
        # Combinar visitas y reservas en un timeline
        timeline_data = []
        
        for visit in visits:
            timeline_data.append({
                'Fecha': datetime.fromisoformat(visit['visit_date'].replace('Z', '+00:00')),
                'Tipo': 'Visita',
                'Lugar': visit.get('points_of_interest', {}).get('name', 'N/A')
            })
        
        for booking in bookings:
            timeline_data.append({
                'Fecha': datetime.fromisoformat(booking['booking_date'].replace('Z', '+00:00')),
                'Tipo': 'Reserva',
                'Lugar': booking.get('points_of_interest', {}).get('name', 'N/A')
            })
        
        df_timeline = pd.DataFrame(timeline_data).sort_values('Fecha', ascending=False)
        
        # Mostrar últimas 10 actividades
        st.dataframe(
            df_timeline.head(10),
            use_container_width=True,
            hide_index=True
        )
    
    # Ratings dados
    if visits:
        st.subheader("⭐ Tus Calificaciones")
        
        ratings = [v.get('rating') for v in visits if v.get('rating')]
        
        if ratings:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_rating = sum(ratings) / len(ratings)
                st.metric("Promedio", f"{avg_rating:.1f}/5.0")
            
            with col2:
                st.metric("Total Reseñas", len(ratings))
            
            with col3:
                max_rating = max(ratings)
                st.metric("Mejor Rating", f"{max_rating}/5.0")
            
            # Distribución de ratings
            rating_counts = pd.Series(ratings).value_counts().sort_index()
            
            fig = px.bar(x=rating_counts.index, y=rating_counts.values,
                        labels={'x': 'Rating', 'y': 'Cantidad'},
                        title='Distribución de tus Calificaciones')
            fig.update_traces(marker_color='#f093fb')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Gastos
    if bookings:
        st.subheader("💰 Análisis de Gastos")
        
        total_spent = sum(b['total_price'] for b in bookings)
        avg_booking = total_spent / len(bookings) if bookings else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Gastado", f"€{total_spent:.2f}")
        with col2:
            st.metric("Promedio por Reserva", f"€{avg_booking:.2f}")
        with col3:
            st.metric("Reservas Realizadas", len(bookings))
        
        # Gastos por mes (simulado)
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        spending = [np.random.uniform(50, 200) for _ in months]
        
        fig = px.line(x=months, y=spending,
                     labels={'x': 'Mes', 'y': 'Gasto (€)'},
                     title='Evolución de Gastos Mensuales')
        fig.update_traces(line_color='#43e97b', line_width=3)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Progreso de logros
    if achievements:
        st.subheader("🏆 Progreso de Logros")
        
        total_points = sum(a.get('points', 0) for a in achievements)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Puntos de Logros", total_points)
            
            # Logros por tipo
            type_counts = {}
            for achievement in achievements:
                achievement_type = achievement.get('achievement_type', 'otros')
                type_counts[achievement_type] = type_counts.get(achievement_type, 0) + 1
            
            df_types = pd.DataFrame({
                'Tipo': list(type_counts.keys()),
                'Cantidad': list(type_counts.values())
            })
            
            fig = px.bar(df_types, x='Tipo', y='Cantidad',
                        title='Logros por Tipo',
                        color='Cantidad',
                        color_continuous_scale='Sunset')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Timeline de logros
            st.write("**Últimos Logros Desbloqueados**")
            
            for achievement in achievements[:5]:
                earned_at = achievement.get('earned_at', '')
                if earned_at:
                    date = datetime.fromisoformat(earned_at.replace('Z', '+00:00'))
                    icon = achievement.get('badge_icon', '🏆')
                    name = achievement['achievement_name']
                    points = achievement.get('points', 0)
                    
                    st.write(f"{icon} **{name}** (+{points} pts)")
                    st.caption(f"📅 {date.strftime('%d/%m/%Y')}")
                    st.divider()
