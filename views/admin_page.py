"""
Página de Administración - CRUD Completo y Gráficos
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import config

def show(db, n8n):
    """Muestra la página de administración"""
    
    st.title("⚙️ Panel de Administración")
    st.markdown("---")
    
    # Tabs para diferentes módulos
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", 
        "🌍 Ciudades", 
        "📍 POIs", 
        "👥 Usuarios", 
        "🎫 Reservas", 
        "📈 Estadísticas"
    ])
    
    with tab1:
        show_dashboard(db)
    
    with tab2:
        show_cities_admin(db)
    
    with tab3:
        show_pois_admin(db)
    
    with tab4:
        show_users_admin(db)
    
    with tab5:
        show_bookings_admin(db)
    
    with tab6:
        show_statistics_admin(db)


def show_dashboard(db):
    """Dashboard principal con gráficos y métricas"""
    
    st.subheader("📊 Dashboard General")
    
    # Obtener datos
    cities = db.get_all_cities(include_inactive=True)
    pois = db.get_all_pois(include_inactive=True)
    users = db.get_all_users()
    bookings = db.get_all_bookings()
    visits = db.get_all_visits()
    
    # Métricas principales
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🌍 Ciudades", len(cities), delta=len([c for c in cities if c.get('is_active')]))
    with col2:
        st.metric("📍 POIs", len(pois), delta=len([p for p in pois if p.get('is_active')]))
    with col3:
        st.metric("👥 Usuarios", len(users))
    with col4:
        st.metric("🎫 Reservas", len(bookings))
    with col5:
        st.metric("👣 Visitas", len(visits))
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de ciudades por país
        if cities:
            df_cities = pd.DataFrame(cities)
            country_counts = df_cities['country'].value_counts()
            fig = px.pie(
                values=country_counts.values, 
                names=country_counts.index,
                title="Ciudades por País",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de POIs por categoría
        if pois:
            df_pois = pd.DataFrame(pois)
            if 'category' in df_pois.columns:
                category_counts = df_pois['category'].value_counts()
                fig = px.bar(
                    x=category_counts.index,
                    y=category_counts.values,
                    title="POIs por Categoría",
                    labels={'x': 'Categoría', 'y': 'Cantidad'},
                    color=category_counts.values,
                    color_continuous_scale='viridis'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de usuarios por suscripción
    if users:
        col1, col2 = st.columns(2)
        
        with col1:
            df_users = pd.DataFrame(users)
            if 'subscription_tier' in df_users.columns:
                sub_counts = df_users['subscription_tier'].value_counts()
                fig = px.bar(
                    x=sub_counts.index,
                    y=sub_counts.values,
                    title="Usuarios por Suscripción",
                    labels={'x': 'Tipo de Suscripción', 'y': 'Cantidad'},
                    color=sub_counts.values,
                    color_continuous_scale='blues'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de usuarios registrados por fecha
            if 'created_at' in df_users.columns:
                df_users['created_at'] = pd.to_datetime(df_users['created_at'])
                df_users['date'] = df_users['created_at'].dt.date
                daily_users = df_users.groupby('date').size().reset_index(name='count')
                fig = px.line(
                    daily_users,
                    x='date',
                    y='count',
                    title="Usuarios Registrados por Día",
                    labels={'date': 'Fecha', 'count': 'Usuarios'},
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de reservas por estado
    if bookings:
        col1, col2 = st.columns(2)
        
        with col1:
            df_bookings = pd.DataFrame(bookings)
            if 'status' in df_bookings.columns:
                status_counts = df_bookings['status'].value_counts()
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Reservas por Estado",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Ingresos por mes
            if 'booking_date' in df_bookings.columns and 'total_price' in df_bookings.columns:
                df_bookings['booking_date'] = pd.to_datetime(df_bookings['booking_date'])
                df_bookings['month'] = df_bookings['booking_date'].dt.to_period('M')
                monthly_revenue = df_bookings.groupby('month')['total_price'].sum().reset_index()
                monthly_revenue['month'] = monthly_revenue['month'].astype(str)
                fig = px.bar(
                    monthly_revenue,
                    x='month',
                    y='total_price',
                    title="Ingresos por Mes (€)",
                    labels={'month': 'Mes', 'total_price': 'Ingresos (€)'},
                    color='total_price',
                    color_continuous_scale='greens'
                )
                st.plotly_chart(fig, use_container_width=True)


def show_cities_admin(db):
    """Administración de ciudades con CRUD completo"""
    
    st.subheader("🌍 Administración de Ciudades")
    
    # Tabs para CRUD
    tab_list, tab_create, tab_edit, tab_delete = st.tabs(["📋 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"])
    
    with tab_list:
        cities = db.get_all_cities(include_inactive=True)
        if cities:
            df = pd.DataFrame(cities)
            # Seleccionar columnas relevantes
            display_cols = ['name', 'country', 'price', 'is_active', 'created_at']
            available_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[available_cols], use_container_width=True)
        else:
            st.info("No hay ciudades registradas")
    
    with tab_create:
        with st.form("create_city_form"):
            st.markdown("### ➕ Crear Nueva Ciudad")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nombre *", placeholder="Ej: Madrid")
                country = st.text_input("País *", placeholder="Ej: España")
                country_code = st.text_input("Código de País", placeholder="ES", max_chars=2)
                description = st.text_area("Descripción", placeholder="Descripción de la ciudad...")
                image_url = st.text_input("URL de Imagen", placeholder="https://...")
            
            with col2:
                price = st.number_input("Precio (€)", min_value=0.0, value=0.0, step=0.01)
                currency = st.selectbox("Moneda", ["EUR", "USD", "GBP"], index=0)
                latitude = st.number_input("Latitud", value=0.0, format="%.8f")
                longitude = st.number_input("Longitud", value=0.0, format="%.8f")
                timezone = st.text_input("Zona Horaria", placeholder="Europe/Madrid")
                language = st.text_input("Idioma", placeholder="español")
                is_active = st.checkbox("Activa", value=True)
            
            submit = st.form_submit_button("Crear Ciudad", use_container_width=True)
            
            if submit:
                if name and country:
                    city_data = {
                        "name": name,
                        "country": country,
                        "country_code": country_code if country_code else None,
                        "description": description if description else None,
                        "image_url": image_url if image_url else None,
                        "price": price,
                        "currency": currency,
                        "latitude": latitude if latitude != 0 else None,
                        "longitude": longitude if longitude != 0 else None,
                        "timezone": timezone if timezone else None,
                        "language": language if language else None,
                        "is_active": is_active
                    }
                    
                    result = db.create_city(city_data)
                    if result:
                        st.success(f"✅ Ciudad '{name}' creada exitosamente!")
                        st.rerun()
                    else:
                        st.error("❌ Error al crear la ciudad")
                else:
                    st.warning("⚠️ Por favor completa los campos obligatorios (*)")
    
    with tab_edit:
        cities = db.get_all_cities(include_inactive=True)
        if cities:
            city_options = {f"{c['name']} ({c['country']})": c['id'] for c in cities}
            selected_city_name = st.selectbox("Selecciona una ciudad para editar", list(city_options.keys()))
            
            if selected_city_name:
                city_id = city_options[selected_city_name]
                city = db.get_city_by_id(city_id)
                
                if city:
                    with st.form("edit_city_form"):
                        st.markdown("### ✏️ Editar Ciudad")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            name = st.text_input("Nombre *", value=city.get('name', ''))
                            country = st.text_input("País *", value=city.get('country', ''))
                            country_code = st.text_input("Código de País", value=city.get('country_code', ''))
                            description = st.text_area("Descripción", value=city.get('description', ''))
                            image_url = st.text_input("URL de Imagen", value=city.get('image_url', ''))
                        
                        with col2:
                            price = st.number_input("Precio (€)", min_value=0.0, value=float(city.get('price', 0)))
                            currency = st.selectbox("Moneda", ["EUR", "USD", "GBP"], 
                                                  index=["EUR", "USD", "GBP"].index(city.get('currency', 'EUR')) if city.get('currency') in ["EUR", "USD", "GBP"] else 0)
                            latitude = st.number_input("Latitud", value=float(city.get('latitude', 0)), format="%.8f")
                            longitude = st.number_input("Longitud", value=float(city.get('longitude', 0)), format="%.8f")
                            timezone = st.text_input("Zona Horaria", value=city.get('timezone', ''))
                            language = st.text_input("Idioma", value=city.get('language', ''))
                            is_active = st.checkbox("Activa", value=city.get('is_active', True))
                        
                        submit = st.form_submit_button("Actualizar Ciudad", use_container_width=True)
                        
                        if submit:
                            if name and country:
                                city_data = {
                                    "name": name,
                                    "country": country,
                                    "country_code": country_code if country_code else None,
                                    "description": description if description else None,
                                    "image_url": image_url if image_url else None,
                                    "price": price,
                                    "currency": currency,
                                    "latitude": latitude if latitude != 0 else None,
                                    "longitude": longitude if longitude != 0 else None,
                                    "timezone": timezone if timezone else None,
                                    "language": language if language else None,
                                    "is_active": is_active
                                }
                                
                                result = db.update_city(city_id, city_data)
                                if result:
                                    st.success(f"✅ Ciudad '{name}' actualizada exitosamente!")
                                    st.rerun()
                                else:
                                    st.error("❌ Error al actualizar la ciudad")
                            else:
                                st.warning("⚠️ Por favor completa los campos obligatorios (*)")
        else:
            st.info("No hay ciudades para editar")
    
    with tab_delete:
        cities = db.get_all_cities(include_inactive=False)
        if cities:
            city_options = {f"{c['name']} ({c['country']})": c['id'] for c in cities}
            selected_city_name = st.selectbox("Selecciona una ciudad para eliminar", list(city_options.keys()))
            
            if selected_city_name:
                city_id = city_options[selected_city_name]
                city = db.get_city_by_id(city_id)
                
                if city:
                    st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar '{city['name']}'?")
                    st.info("Esta acción desactivará la ciudad (soft delete)")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ Eliminar Ciudad", use_container_width=True, type="primary"):
                            if db.delete_city(city_id):
                                st.success(f"✅ Ciudad '{city['name']}' eliminada exitosamente!")
                                st.rerun()
                            else:
                                st.error("❌ Error al eliminar la ciudad")
                    with col2:
                        if st.button("Cancelar", use_container_width=True):
                            st.info("Operación cancelada")
        else:
            st.info("No hay ciudades activas para eliminar")


def show_pois_admin(db):
    """Administración de POIs con CRUD completo"""
    
    st.subheader("📍 Administración de Puntos de Interés")
    
    # Tabs para CRUD
    tab_list, tab_create, tab_edit, tab_delete = st.tabs(["📋 Listar", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"])
    
    with tab_list:
        pois = db.get_all_pois(include_inactive=True)
        if pois:
            # Preparar datos para mostrar
            pois_display = []
            for poi in pois:
                city_name = poi.get('cities', {}).get('name', 'N/A') if isinstance(poi.get('cities'), dict) else 'N/A'
                pois_display.append({
                    'name': poi.get('name', ''),
                    'city': city_name,
                    'category': poi.get('category', ''),
                    'rating': poi.get('rating', 0),
                    'price': poi.get('entry_price', 0),
                    'is_active': poi.get('is_active', True)
                })
            df = pd.DataFrame(pois_display)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay POIs registrados")
    
    with tab_create:
        cities = db.get_all_cities(include_inactive=False)
        if cities:
            with st.form("create_poi_form"):
                st.markdown("### ➕ Crear Nuevo POI")
                col1, col2 = st.columns(2)
                
                with col1:
                    city_options = {f"{c['name']} ({c['country']})": c['id'] for c in cities}
                    city_name = st.selectbox("Ciudad *", list(city_options.keys()))
                    city_id = city_options[city_name] if city_name else None
                    
                    name = st.text_input("Nombre *", placeholder="Ej: Palacio Real")
                    description = st.text_area("Descripción", placeholder="Descripción del POI...")
                    short_description = st.text_input("Descripción Corta", placeholder="Breve descripción...")
                    category = st.selectbox("Categoría", ["", *config.POI_CATEGORIES])
                
                with col2:
                    latitude = st.number_input("Latitud *", value=0.0, format="%.8f")
                    longitude = st.number_input("Longitud *", value=0.0, format="%.8f")
                    visit_duration = st.number_input("Duración de Visita (min)", min_value=0, value=30)
                    difficulty_level = st.selectbox("Nivel de Dificultad", config.DIFFICULTY_LEVELS, index=0)
                    entry_price = st.number_input("Precio de Entrada (€)", min_value=0.0, value=0.0, step=0.01)
                    is_active = st.checkbox("Activo", value=True)
                
                submit = st.form_submit_button("Crear POI", use_container_width=True)
                
                if submit:
                    if name and city_id and latitude != 0 and longitude != 0:
                        poi_data = {
                            "city_id": city_id,
                            "name": name,
                            "description": description if description else None,
                            "short_description": short_description if short_description else None,
                            "latitude": latitude,
                            "longitude": longitude,
                            "category": category if category else None,
                            "visit_duration": visit_duration,
                            "difficulty_level": difficulty_level,
                            "entry_price": entry_price,
                            "is_active": is_active
                        }
                        
                        result = db.create_poi(poi_data)
                        if result:
                            st.success(f"✅ POI '{name}' creado exitosamente!")
                            st.rerun()
                        else:
                            st.error("❌ Error al crear el POI")
                    else:
                        st.warning("⚠️ Por favor completa los campos obligatorios (*)")
        else:
            st.warning("⚠️ Primero debes crear ciudades")
    
    with tab_edit:
        pois = db.get_all_pois(include_inactive=True)
        if pois:
            poi_options = {f"{p['name']}": p['id'] for p in pois}
            selected_poi_name = st.selectbox("Selecciona un POI para editar", list(poi_options.keys()))
            
            if selected_poi_name:
                poi_id = poi_options[selected_poi_name]
                poi = db.get_poi_by_id(poi_id)
                
                if poi:
                    cities = db.get_all_cities(include_inactive=False)
                    city_options = {f"{c['name']} ({c['country']})": c['id'] for c in cities}
                    current_city_id = poi.get('city_id')
                    current_city_name = next((f"{c['name']} ({c['country']})" for c in cities if c['id'] == current_city_id), None)
                    
                    with st.form("edit_poi_form"):
                        st.markdown("### ✏️ Editar POI")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            city_name = st.selectbox("Ciudad *", list(city_options.keys()), 
                                                    index=list(city_options.keys()).index(current_city_name) if current_city_name else 0)
                            city_id = city_options[city_name] if city_name else None
                            
                            name = st.text_input("Nombre *", value=poi.get('name', ''))
                            description = st.text_area("Descripción", value=poi.get('description', ''))
                            short_description = st.text_input("Descripción Corta", value=poi.get('short_description', ''))
                            category = st.selectbox("Categoría", ["", *config.POI_CATEGORIES],
                                                   index=config.POI_CATEGORIES.index(poi.get('category', '')) + 1 if poi.get('category') in config.POI_CATEGORIES else 0)
                        
                        with col2:
                            latitude = st.number_input("Latitud *", value=float(poi.get('latitude', 0)), format="%.8f")
                            longitude = st.number_input("Longitud *", value=float(poi.get('longitude', 0)), format="%.8f")
                            visit_duration = st.number_input("Duración de Visita (min)", min_value=0, value=int(poi.get('visit_duration', 30)))
                            difficulty_level = st.selectbox("Nivel de Dificultad", config.DIFFICULTY_LEVELS,
                                                          index=config.DIFFICULTY_LEVELS.index(poi.get('difficulty_level', 'Fácil')) if poi.get('difficulty_level') in config.DIFFICULTY_LEVELS else 0)
                            entry_price = st.number_input("Precio de Entrada (€)", min_value=0.0, value=float(poi.get('entry_price', 0)), step=0.01)
                            is_active = st.checkbox("Activo", value=poi.get('is_active', True))
                        
                        submit = st.form_submit_button("Actualizar POI", use_container_width=True)
                        
                        if submit:
                            if name and city_id and latitude != 0 and longitude != 0:
                                poi_data = {
                                    "city_id": city_id,
                                    "name": name,
                                    "description": description if description else None,
                                    "short_description": short_description if short_description else None,
                                    "latitude": latitude,
                                    "longitude": longitude,
                                    "category": category if category else None,
                                    "visit_duration": visit_duration,
                                    "difficulty_level": difficulty_level,
                                    "entry_price": entry_price,
                                    "is_active": is_active
                                }
                                
                                result = db.update_poi(poi_id, poi_data)
                                if result:
                                    st.success(f"✅ POI '{name}' actualizado exitosamente!")
                                    st.rerun()
                                else:
                                    st.error("❌ Error al actualizar el POI")
                            else:
                                st.warning("⚠️ Por favor completa los campos obligatorios (*)")
        else:
            st.info("No hay POIs para editar")
    
    with tab_delete:
        pois = db.get_all_pois(include_inactive=False)
        if pois:
            poi_options = {f"{p['name']}": p['id'] for p in pois}
            selected_poi_name = st.selectbox("Selecciona un POI para eliminar", list(poi_options.keys()))
            
            if selected_poi_name:
                poi_id = poi_options[selected_poi_name]
                poi = db.get_poi_by_id(poi_id)
                
                if poi:
                    st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar '{poi['name']}'?")
                    st.info("Esta acción desactivará el POI (soft delete)")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ Eliminar POI", use_container_width=True, type="primary"):
                            if db.delete_poi(poi_id):
                                st.success(f"✅ POI '{poi['name']}' eliminado exitosamente!")
                                st.rerun()
                            else:
                                st.error("❌ Error al eliminar el POI")
                    with col2:
                        if st.button("Cancelar", use_container_width=True):
                            st.info("Operación cancelada")
        else:
            st.info("No hay POIs activos para eliminar")


def show_users_admin(db):
    """Administración de usuarios con CRUD completo"""
    
    st.subheader("👥 Administración de Usuarios")
    
    # Tabs para CRUD
    tab_list, tab_edit, tab_delete = st.tabs(["📋 Listar", "✏️ Editar", "🗑️ Eliminar"])
    
    with tab_list:
        users = db.get_all_users()
        if users:
            df = pd.DataFrame(users)
            display_cols = ['name', 'email', 'subscription_tier', 'total_points', 'level', 'created_at']
            available_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[available_cols], use_container_width=True)
        else:
            st.info("No hay usuarios registrados")
    
    with tab_edit:
        users = db.get_all_users()
        if users:
            user_options = {f"{u['name']} ({u['email']})": u['id'] for u in users}
            selected_user_name = st.selectbox("Selecciona un usuario para editar", list(user_options.keys()))
            
            if selected_user_name:
                user_id = user_options[selected_user_name]
                user = db.get_user_by_id(user_id)
                
                if user:
                    with st.form("edit_user_form"):
                        st.markdown("### ✏️ Editar Usuario")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            name = st.text_input("Nombre *", value=user.get('name', ''))
                            email = st.text_input("Email *", value=user.get('email', ''))
                            phone = st.text_input("Teléfono", value=user.get('phone', ''))
                            subscription_tier = st.selectbox("Tipo de Suscripción", 
                                                           list(config.SUBSCRIPTION_TIERS.keys()),
                                                           index=list(config.SUBSCRIPTION_TIERS.keys()).index(user.get('subscription_tier', 'free')) if user.get('subscription_tier') in config.SUBSCRIPTION_TIERS else 0)
                        
                        with col2:
                            total_points = st.number_input("Puntos Totales", min_value=0, value=int(user.get('total_points', 0)))
                            level = st.text_input("Nivel", value=user.get('level', 'Explorador Novato'))
                            avatar_url = st.text_input("URL de Avatar", value=user.get('avatar_url', ''))
                        
                        submit = st.form_submit_button("Actualizar Usuario", use_container_width=True)
                        
                        if submit:
                            if name and email:
                                user_data = {
                                    "name": name,
                                    "email": email,
                                    "phone": phone if phone else None,
                                    "subscription_tier": subscription_tier,
                                    "total_points": total_points,
                                    "level": level,
                                    "avatar_url": avatar_url if avatar_url else None
                                }
                                
                                result = db.update_user(user_id, user_data)
                                if result:
                                    st.success(f"✅ Usuario '{name}' actualizado exitosamente!")
                                    st.rerun()
                                else:
                                    st.error("❌ Error al actualizar el usuario")
                            else:
                                st.warning("⚠️ Por favor completa los campos obligatorios (*)")
        else:
            st.info("No hay usuarios para editar")
    
    with tab_delete:
        users = db.get_all_users()
        if users:
            user_options = {f"{u['name']} ({u['email']})": u['id'] for u in users}
            selected_user_name = st.selectbox("Selecciona un usuario para eliminar", list(user_options.keys()))
            
            if selected_user_name:
                user_id = user_options[selected_user_name]
                user = db.get_user_by_id(user_id)
                
                if user:
                    st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar al usuario '{user['name']}'?")
                    st.error("⚠️ Esta acción es permanente y no se puede deshacer")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🗑️ Eliminar Usuario", use_container_width=True, type="primary"):
                            if db.delete_user(user_id):
                                st.success(f"✅ Usuario '{user['name']}' eliminado exitosamente!")
                                st.rerun()
                            else:
                                st.error("❌ Error al eliminar el usuario")
                    with col2:
                        if st.button("Cancelar", use_container_width=True):
                            st.info("Operación cancelada")
        else:
            st.info("No hay usuarios para eliminar")


def show_bookings_admin(db):
    """Administración de reservas"""
    
    st.subheader("🎫 Administración de Reservas")
    
    bookings = db.get_all_bookings()
    
    if bookings:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filtrar por Estado", ["Todos", *list(config.BOOKING_STATUSES.keys())])
        with col2:
            search = st.text_input("Buscar por código de confirmación")
        
        # Aplicar filtros
        filtered_bookings = bookings
        if status_filter != "Todos":
            filtered_bookings = [b for b in filtered_bookings if b.get('status') == status_filter]
        if search:
            filtered_bookings = [b for b in filtered_bookings if search.lower() in str(b.get('confirmation_code', '')).lower()]
        
        # Mostrar reservas
        for booking in filtered_bookings:
            with st.expander(f"🎫 {booking.get('confirmation_code', 'Sin código')} - {booking.get('status', 'N/A')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Usuario:** {booking.get('users', {}).get('name', 'N/A') if isinstance(booking.get('users'), dict) else 'N/A'}")
                    st.write(f"**Email:** {booking.get('users', {}).get('email', 'N/A') if isinstance(booking.get('users'), dict) else 'N/A'}")
                    poi = booking.get('points_of_interest', {})
                    if isinstance(poi, dict):
                        st.write(f"**POI:** {poi.get('name', 'N/A')}")
                
                with col2:
                    st.write(f"**Fecha:** {booking.get('booking_date', 'N/A')}")
                    st.write(f"**Personas:** {booking.get('number_of_people', 0)}")
                    st.write(f"**Precio Total:** €{booking.get('total_price', 0):.2f}")
                
                with col3:
                    current_status = booking.get('status', 'pending')
                    new_status = st.selectbox("Cambiar Estado", list(config.BOOKING_STATUSES.keys()),
                                            index=list(config.BOOKING_STATUSES.keys()).index(current_status) if current_status in config.BOOKING_STATUSES else 0,
                                            key=f"status_{booking.get('id')}")
                    
                    if new_status != current_status:
                        if st.button("Actualizar Estado", key=f"update_{booking.get('id')}"):
                            if db.update_booking_status(booking.get('id'), new_status):
                                st.success("Estado actualizado!")
                                st.rerun()
    else:
        st.info("No hay reservas registradas")


def show_statistics_admin(db):
    """Estadísticas avanzadas"""
    
    st.subheader("📈 Estadísticas Avanzadas")
    
    # Obtener datos
    visits = db.get_all_visits()
    bookings = db.get_all_bookings()
    users = db.get_all_users()
    
    if visits:
        col1, col2 = st.columns(2)
        
        with col1:
            # Visitas por mes
            df_visits = pd.DataFrame(visits)
            if 'visit_date' in df_visits.columns:
                df_visits['visit_date'] = pd.to_datetime(df_visits['visit_date'])
                df_visits['month'] = df_visits['visit_date'].dt.to_period('M')
                monthly_visits = df_visits.groupby('month').size().reset_index(name='count')
                monthly_visits['month'] = monthly_visits['month'].astype(str)
                fig = px.line(monthly_visits, x='month', y='count', title="Visitas por Mes", markers=True)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rating promedio de visitas
            if 'rating' in df_visits.columns:
                df_visits['rating'] = pd.to_numeric(df_visits['rating'], errors='coerce')
                avg_rating = df_visits['rating'].mean()
                st.metric("Rating Promedio", f"{avg_rating:.2f}/5.0")
                
                rating_dist = df_visits['rating'].value_counts().sort_index()
                fig = px.bar(x=rating_dist.index, y=rating_dist.values, title="Distribución de Ratings")
                st.plotly_chart(fig, use_container_width=True)
    
    if bookings:
        col1, col2 = st.columns(2)
        
        with col1:
            # Ingresos totales
            df_bookings = pd.DataFrame(bookings)
            total_revenue = df_bookings['total_price'].sum() if 'total_price' in df_bookings.columns else 0
            st.metric("💰 Ingresos Totales", f"€{total_revenue:,.2f}")
        
        with col2:
            # Reservas confirmadas vs canceladas
            if 'status' in df_bookings.columns:
                status_counts = df_bookings['status'].value_counts()
                fig = px.pie(values=status_counts.values, names=status_counts.index, title="Estado de Reservas")
                st.plotly_chart(fig, use_container_width=True)

