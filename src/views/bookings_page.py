"""
Página de Reservas
"""
import streamlit as st
from datetime import datetime, timedelta
import config.config as config

def show(db, n8n):
    """Muestra la página de reservas"""
    
    st.title("🎫 Sistema de Reservas")
    st.markdown("Reserva tu visita a los mejores lugares turísticos")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Debes iniciar sesión para realizar reservas")
        return
    
    # Tabs
    tab1, tab2 = st.tabs(["🆕 Nueva Reserva", "📋 Mis Reservas"])
    
    with tab1:
        show_new_booking(db, n8n)
    
    with tab2:
        show_my_bookings(db, n8n)


def show_new_booking(db, n8n):
    """Muestra el formulario para crear una nueva reserva"""
    
    st.subheader("🆕 Crear Nueva Reserva")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selección de ciudad
        cities = db.get_cities()
        city_options = {c['name']: c['id'] for c in cities}
        selected_city_name = st.selectbox("Ciudad", list(city_options.keys()))
        selected_city_id = city_options[selected_city_name]
        
        # Selección de POI
        pois = db.get_pois(city_id=selected_city_id)
        
        if not pois:
            st.warning("No hay puntos de interés disponibles para esta ciudad")
            return
        
        poi_options = {f"{p['name']} - €{p.get('entry_price', 0):.2f}": p for p in pois}
        selected_poi_name = st.selectbox("Punto de interés", list(poi_options.keys()))
        selected_poi = poi_options[selected_poi_name]
        
        # Fecha y hora
        col_a, col_b = st.columns(2)
        with col_a:
            booking_date = st.date_input(
                "Fecha de visita",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=1)
            )
        with col_b:
            booking_time = st.time_input("Hora de visita", value=datetime.now().replace(hour=10, minute=0).time())
        
        # Número de personas
        number_of_people = st.number_input(
            "Número de personas",
            min_value=1,
            max_value=20,
            value=2
        )
        
        # Información de contacto
        contact_phone = st.text_input(
            "Teléfono de contacto",
            placeholder="+34 600 000 000",
            help="Introduce tu número de teléfono para confirmaciones"
        )
        
        # Notas especiales
        special_requirements = st.text_area(
            "Requisitos especiales (opcional)",
            placeholder="Ej: Necesito acceso para silla de ruedas, tengo niños pequeños, etc."
        )
    
    with col2:
        st.markdown("### 💰 Resumen de Reserva")
        
        # Calcular precio
        base_price = selected_poi.get('entry_price', 15.00)
        total_price = base_price * number_of_people
        
        # Información del POI
        st.info(f"**{selected_poi['name']}**")
        st.write(f"📍 {selected_city_name}")
        st.write(f"📅 {booking_date.strftime('%d/%m/%Y')}")
        st.write(f"🕐 {booking_time.strftime('%H:%M')}")
        st.write(f"👥 {number_of_people} persona(s)")
        
        st.markdown("---")
        
        # Desglose de precio
        st.write(f"**Precio por persona:** €{base_price:.2f}")
        st.write(f"**Cantidad:** {number_of_people}")
        st.markdown(f"### **Total: €{total_price:.2f}**")
        
        st.markdown("---")
        
        # Método de pago
        payment_method = st.selectbox("Método de pago", ["Tarjeta de Crédito", "PayPal", "Transferencia"])
    
    # Vista previa del POI
    with st.expander("👁️ Información del Lugar", expanded=False):
        if selected_poi.get('description'):
            st.write(selected_poi['description'])
        
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            st.metric("⭐ Rating", f"{selected_poi.get('rating', 0):.1f}")
        with col_y:
            st.metric("🕐 Duración", f"{selected_poi.get('visit_duration', 0)} min")
        with col_z:
            st.metric("📊 Dificultad", selected_poi.get('difficulty_level', 'N/A'))
    
    # Botón de confirmación
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🎫 Confirmar Reserva", type="primary", use_container_width=True):
            create_booking(db, n8n, selected_poi, booking_date, booking_time, 
                          number_of_people, total_price, payment_method, special_requirements, contact_phone)
    
    with col_btn2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.info("Reserva cancelada")


def create_booking(db, n8n, poi, date, time, people, price, payment_method, requirements, contact_phone):
    """Crea una nueva reserva"""
    
    with st.spinner("💳 Procesando reserva..."):
        # Combinar fecha y hora
        booking_datetime = datetime.combine(date, time)
        
        # Llamar a n8n para crear la reserva
        n8n_result = None
        try:
            n8n_result = n8n.create_booking(
                poi_id=poi['id'],
                poi_name=poi['name'],
                booking_date=booking_datetime,
                number_of_people=people,
                total_price=price,
                user_id=st.session_state.user_id,
                contact_email=st.session_state.user_email,
                contact_phone=contact_phone,
                currency="EUR"
            )
        except Exception as e:
            # Si n8n no está disponible, continuar con la creación local
            st.warning(f"⚠️ No se pudo procesar la reserva en n8n: {str(e)}")
            pass
        
        # Crear reserva en la base de datos
        booking_data = {
            "user_id": st.session_state.user_id,
            "poi_id": poi['id'],
            "booking_date": booking_datetime.isoformat(),
            "number_of_people": people,
            "total_price": price,
            "currency": "EUR",
            "status": "confirmed" if n8n_result else "pending",
            "payment_method": payment_method,
            "payment_id": n8n_result.get('booking_id') if n8n_result else None,
            "special_requirements": requirements,
            "contact_email": st.session_state.user_email,
            "contact_phone": contact_phone
        }
        
        result = db.create_booking(booking_data)
        
        if result:
            st.success("✅ ¡Reserva confirmada exitosamente!")
            
            # Mostrar código de confirmación
            confirmation_code = result.get('confirmation_code', 'N/A')
            
            st.balloons()
            
            # Mostrar detalles
            st.markdown("### 🎉 Detalles de tu Reserva")
            st.info(f"""
            **Código de Confirmación:** `{confirmation_code}`
            
            **Lugar:** {poi['name']}
            **Fecha:** {date.strftime('%d/%m/%Y')} a las {time.strftime('%H:%M')}
            **Personas:** {people}
            **Total Pagado:** €{price:.2f}
            
            Hemos enviado un correo de confirmación a {st.session_state.user_email}
            """)
            
            # Registrar estadística
            db.create_usage_stat({
                "user_id": st.session_state.user_id,
                "action_type": "booking",
                "poi_id": poi['id'],
                "metadata": {"total_price": price, "people": people}
            })
            
            # Verificar logros
            check_booking_achievements(db, st.session_state.user_id)
        else:
            st.error("❌ No se pudo completar la reserva. Por favor, intenta de nuevo.")


def show_my_bookings(db, n8n):
    """Muestra las reservas del usuario"""
    
    st.subheader("📋 Mis Reservas")
    
    # Obtener reservas
    bookings = db.get_user_bookings(st.session_state.user_id)
    
    if not bookings:
        st.info("No tienes reservas aún. ¡Crea tu primera reserva en la pestaña anterior!")
        return
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox(
            "Filtrar por estado",
            ["Todas"] + list(config.BOOKING_STATUSES.values())
        )
    with col2:
        sort_by = st.selectbox("Ordenar por", ["Fecha (Reciente)", "Fecha (Antigua)", "Precio"])
    
    # Aplicar filtros
    filtered_bookings = bookings
    if status_filter != "Todas":
        status_key = [k for k, v in config.BOOKING_STATUSES.items() if v == status_filter][0]
        filtered_bookings = [b for b in bookings if b['status'] == status_key]
    
    # Ordenar
    if sort_by == "Fecha (Antigua)":
        filtered_bookings = sorted(filtered_bookings, key=lambda x: x['booking_date'])
    elif sort_by == "Precio":
        filtered_bookings = sorted(filtered_bookings, key=lambda x: x['total_price'], reverse=True)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Reservas", len(bookings))
    with col2:
        confirmed = len([b for b in bookings if b['status'] == 'confirmed'])
        st.metric("✅ Confirmadas", confirmed)
    with col3:
        total_spent = sum(b['total_price'] for b in bookings)
        st.metric("💰 Total Gastado", f"€{total_spent:.2f}")
    
    st.markdown("---")
    
    # Listar reservas
    for booking in filtered_bookings:
        poi = booking.get('points_of_interest', {})
        city = poi.get('cities', {})
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Título
                st.markdown(f"### 🎫 {poi.get('name', 'N/A')}")
                
                # Información
                info_cols = st.columns(5)
                with info_cols[0]:
                    st.caption(f"📍 {city.get('name', 'N/A')}")
                with info_cols[1]:
                    booking_date = datetime.fromisoformat(booking['booking_date'].replace('Z', '+00:00'))
                    st.caption(f"📅 {booking_date.strftime('%d/%m/%Y')}")
                with info_cols[2]:
                    st.caption(f"🕐 {booking_date.strftime('%H:%M')}")
                with info_cols[3]:
                    st.caption(f"👥 {booking['number_of_people']} persona(s)")
                with info_cols[4]:
                    status_emoji = {
                        'confirmed': '✅',
                        'pending': '⏳',
                        'cancelled': '❌',
                        'completed': '✔️',
                        'refunded': '💰'
                    }
                    emoji = status_emoji.get(booking['status'], '❓')
                    status_text = config.BOOKING_STATUSES.get(booking['status'], booking['status'])
                    st.caption(f"{emoji} {status_text}")
                
                # Código de confirmación
                if booking.get('confirmation_code'):
                    st.code(f"Código: {booking['confirmation_code']}", language=None)
            
            with col2:
                # Precio
                st.metric("Total", f"€{booking['total_price']:.2f}")
                
                # Acciones
                if booking['status'] == 'confirmed':
                    if st.button("❌ Cancelar", key=f"cancel_{booking['id']}", use_container_width=True):
                        cancel_booking(db, booking)
                
                if st.button("👁️ Ver Detalles", key=f"view_{booking['id']}", use_container_width=True):
                    show_booking_details(db, booking, poi, city)
            
            st.divider()


def show_booking_details(db, booking, poi, city):
    """Muestra los detalles completos de una reserva"""
    
    with st.expander(f"📄 Detalles de Reserva: {poi.get('name', 'N/A')}", expanded=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {poi.get('name', 'N/A')}")
            st.write(f"📍 **Ciudad:** {city.get('name', 'N/A')}, {city.get('country', 'N/A')}")
            
            booking_date = datetime.fromisoformat(booking['booking_date'].replace('Z', '+00:00'))
            st.write(f"📅 **Fecha:** {booking_date.strftime('%d de %B de %Y')}")
            st.write(f"🕐 **Hora:** {booking_date.strftime('%H:%M')}")
            st.write(f"👥 **Personas:** {booking['number_of_people']}")
            
            if booking.get('special_requirements'):
                st.info(f"📝 **Requisitos especiales:** {booking['special_requirements']}")
        
        with col2:
            st.metric("💰 Total", f"€{booking['total_price']:.2f}")
            st.metric("💳 Método de Pago", booking.get('payment_method', 'N/A'))
            
            status_text = config.BOOKING_STATUSES.get(booking['status'], booking['status'])
            st.metric("📊 Estado", status_text)
            
            if booking.get('confirmation_code'):
                st.code(booking['confirmation_code'])
        
        # Información del POI
        st.markdown("---")
        st.markdown("### 📍 Información del Lugar")
        
        if poi.get('description'):
            st.write(poi['description'][:300] + "...")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("⭐ Rating", f"{poi.get('rating', 0):.1f}")
        with col_b:
            st.metric("🕐 Duración", f"{poi.get('visit_duration', 0)} min")
        with col_c:
            st.metric("📊 Dificultad", poi.get('difficulty_level', 'N/A'))


def cancel_booking(db, booking):
    """Cancela una reserva"""
    
    if st.button("⚠️ Confirmar Cancelación", key=f"confirm_cancel_{booking['id']}"):
        result = db.update_booking_status(booking['id'], 'cancelled')
        
        if result:
            st.success("✅ Reserva cancelada exitosamente")
            st.info("Se procesará el reembolso en 3-5 días hábiles")
            st.rerun()
        else:
            st.error("❌ No se pudo cancelar la reserva")


def check_booking_achievements(db, user_id):
    """Verifica y otorga logros relacionados con reservas"""
    
    bookings = db.get_user_bookings(user_id)
    booking_count = len(bookings)
    
    achievements = []
    
    # Primera reserva
    if booking_count == 1:
        achievements.append({
            "user_id": user_id,
            "achievement_type": "visitas",
            "achievement_name": "Primera Reserva",
            "achievement_description": "Realizaste tu primera reserva",
            "points": 100,
            "badge_icon": "🎫",
            "badge_color": "green"
        })
    
    # 5 reservas
    if booking_count == 5:
        achievements.append({
            "user_id": user_id,
            "achievement_type": "explorador",
            "achievement_name": "Viajero Frecuente",
            "achievement_description": "Realizaste 5 reservas",
            "points": 250,
            "badge_icon": "✈️",
            "badge_color": "blue"
        })
    
    # Crear logros
    for achievement in achievements:
        result = db.create_achievement(achievement)
        if result:
            st.success(f"🎉 ¡Nuevo logro! {achievement['achievement_name']} (+{achievement['points']} puntos)")
