"""
Página de Audio-Guías
"""
import streamlit as st
import config
from datetime import datetime

def show(db, n8n):
    """Muestra la página de audio-guías"""
    
    st.title("🎧 Audio-Guías Generadas por IA")
    st.markdown("Escucha guías personalizadas creadas con inteligencia artificial")
    
    if not st.session_state.user_id:
        st.warning("⚠️ Debes iniciar sesión para generar audio-guías")
        return
    
    # Tabs
    tab1, tab2 = st.tabs(["🎵 Generar Nueva", "📚 Mis Audio-Guías"])
    
    with tab1:
        show_generate_audio(db, n8n)
    
    with tab2:
        show_my_audios(db, n8n)


def show_generate_audio(db, n8n):
    """Muestra el formulario para generar una nueva audio-guía"""
    
    st.subheader("🎵 Generar Nueva Audio-Guía")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Selección de ciudad
        cities = db.get_cities()
        city_options = {c['name']: c['id'] for c in cities}
        selected_city_name = st.selectbox("Selecciona una ciudad", list(city_options.keys()))
        selected_city_id = city_options[selected_city_name]
        
        # Selección de POI
        pois = db.get_pois(city_id=selected_city_id)
        
        if not pois:
            st.warning("No hay puntos de interés disponibles para esta ciudad")
            return
        
        poi_options = {p['name']: p for p in pois}
        selected_poi_name = st.selectbox("Selecciona un punto de interés", list(poi_options.keys()))
        selected_poi = poi_options[selected_poi_name]
        
        # Contexto adicional
        additional_context = st.text_area(
            "Contexto adicional (opcional)",
            placeholder="Proporciona información específica que quieras incluir en la guía...\nEj: Enfócate en la arquitectura gótica, menciona anécdotas históricas, etc.",
            height=100
        )
    
    with col2:
        st.markdown("### ⚙️ Configuración")
        
        # Idioma
        language_options = {
            "Español": "es",
            "English": "en",
            "Français": "fr",
            "Italiano": "it"
        }
        selected_language = st.selectbox("Idioma", list(language_options.keys()))
        language_code = language_options[selected_language]
        
        # Tipo de voz
        voice_type = st.selectbox("Tipo de voz", ["Femenina", "Masculina"])
        voice_code = "female" if voice_type == "Femenina" else "male"
        
        # Duración estimada
        duration = st.slider("Duración aproximada (minutos)", 2, 10, 5)
        
        st.info(f"💡 Se generará una guía de aproximadamente {duration} minutos")
    
    # Vista previa del POI
    with st.expander("👁️ Vista Previa del POI", expanded=False):
        st.write(f"**{selected_poi['name']}**")
        st.caption(f"{selected_poi.get('category', 'Sin categoría')} • {selected_poi.get('visit_duration', 0)} min")
        
        if selected_poi.get('description'):
            st.write(selected_poi['description'][:200] + "...")
        
        if selected_poi.get('rating'):
            st.write(f"⭐ {selected_poi['rating']:.1f}/5.0")
    
    # Botón de generación
    st.markdown("---")
    
    if st.button("🎵 Generar Audio-Guía", type="primary", use_container_width=True):
        generate_audio_guide(db, n8n, selected_poi, additional_context, language_code, voice_code, duration)


def generate_audio_guide(db, n8n, poi, context, language, voice_type, duration):
    """Genera una audio-guía usando n8n"""
    
    with st.spinner("🤖 Generando tu audio-guía personalizada..."):
        # Llamar a n8n para generar la audio-guía
        result = n8n.generate_audio_guide(
            poi_id=poi['id'],
            poi_name=poi['name'],
            poi_description=poi.get('description', '') + "\n\n" + context,
            user_id=st.session_state.user_id,
            language=language,
            voice_type=voice_type
        )
        
        if result:
            st.success("✅ ¡Audio-guía generada exitosamente!")
            
            # Mostrar reproductor (simulado)
            st.markdown("### 🎧 Tu Audio-Guía")
            
            # En una implementación real, aquí iría la URL del audio generado
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
            
            # Mostrar transcripción
            with st.expander("📄 Ver Transcripción", expanded=True):
                # Transcripción simulada (en una implementación real vendría de n8n/OpenAI)
                transcription = f"""
                Bienvenidos a {poi['name']}, uno de los lugares más emblemáticos de nuestra ciudad.
                
                {poi.get('description', 'Este maravilloso lugar tiene una rica historia que contar.')}
                
                Durante tu visita, te recomendamos dedicar aproximadamente {poi.get('visit_duration', 30)} minutos 
                para apreciar todos los detalles de este magnífico lugar.
                
                {context if context else ''}
                
                No olvides tomar fotografías y compartir tu experiencia. ¡Disfruta tu visita!
                """
                st.write(transcription)
            
            # Guardar en base de datos
            audio_data = {
                "poi_id": poi['id'],
                "language": language,
                "voice_type": voice_type,
                "transcript": transcription,
                "audio_url": result.get('audio_url', ''),
                "duration_seconds": duration * 60,
                "generation_model": "openai-gpt4",
                "is_active": True
            }
            
            saved_audio = db.create_audio_guide(audio_data)
            
            # Registrar estadística
            db.create_usage_stat({
                "user_id": st.session_state.user_id,
                "action_type": "audio_guide",
                "poi_id": poi['id'],
                "metadata": {"language": language, "duration": duration}
            })
            
            # Verificar logros
            check_audio_achievements(db, st.session_state.user_id)
            
            st.balloons()
        else:
            st.error("❌ No se pudo generar la audio-guía. Por favor, intenta de nuevo.")


def show_my_audios(db, n8n):
    """Muestra las audio-guías del usuario"""
    
    st.subheader("📚 Mis Audio-Guías")
    
    # Obtener estadísticas de audio del usuario
    audio_stats = db.get_usage_stats(
        user_id=st.session_state.user_id,
        action_type="audio_guide",
        limit=50
    )
    
    if not audio_stats:
        st.info("Aún no has generado ninguna audio-guía. ¡Crea tu primera guía en la pestaña anterior!")
        return
    
    # Mostrar métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎧 Total Generadas", len(audio_stats))
    with col2:
        # Calcular tiempo total (simulado)
        total_minutes = len(audio_stats) * 5  # Promedio 5 min por audio
        st.metric("⏱️ Tiempo Total", f"{total_minutes} min")
    with col3:
        # Idiomas únicos
        languages = set(stat.get('metadata', {}).get('language', 'es') for stat in audio_stats)
        st.metric("🌍 Idiomas", len(languages))
    
    st.markdown("---")
    
    # Listar audio-guías
    for stat in audio_stats:
        poi_id = stat.get('poi_id')
        if poi_id:
            poi = db.get_poi_by_id(poi_id)
            if poi:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### 🎧 {poi['name']}")
                        
                        # Información
                        info_cols = st.columns(4)
                        with info_cols[0]:
                            city_name = poi.get('cities', {}).get('name', 'N/A')
                            st.caption(f"📍 {city_name}")
                        with info_cols[1]:
                            lang = stat.get('metadata', {}).get('language', 'es')
                            st.caption(f"🌍 {lang.upper()}")
                        with info_cols[2]:
                            duration = stat.get('metadata', {}).get('duration', 5)
                            st.caption(f"⏱️ {duration} min")
                        with info_cols[3]:
                            timestamp = stat.get('timestamp', '')
                            if timestamp:
                                date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                                st.caption(f"📅 {date.strftime('%d/%m/%Y')}")
                    
                    with col2:
                        if st.button("▶️ Reproducir", key=f"play_{stat['id']}", use_container_width=True):
                            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
                        
                        if st.button("📄 Ver Detalles", key=f"details_{stat['id']}", use_container_width=True):
                            show_audio_details(db, poi, stat)
                    
                    st.divider()


def show_audio_details(db, poi, stat):
    """Muestra los detalles de una audio-guía"""
    
    with st.expander(f"📄 Detalles de Audio-Guía: {poi['name']}", expanded=True):
        # Información del POI
        st.markdown(f"### {poi['name']}")
        st.write(poi.get('description', 'Sin descripción'))
        
        # Metadatos
        col1, col2, col3 = st.columns(3)
        with col1:
            lang = stat.get('metadata', {}).get('language', 'es')
            st.metric("Idioma", lang.upper())
        with col2:
            duration = stat.get('metadata', {}).get('duration', 5)
            st.metric("Duración", f"{duration} min")
        with col3:
            timestamp = stat.get('timestamp', '')
            if timestamp:
                date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                st.metric("Generada", date.strftime('%d/%m/%Y'))
        
        # Reproductor
        st.markdown("### 🎧 Reproducir")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        
        # Transcripción (simulada)
        st.markdown("### 📄 Transcripción")
        st.write(f"Transcripción de la audio-guía para {poi['name']}...")


def check_audio_achievements(db, user_id):
    """Verifica y otorga logros relacionados con audio-guías"""
    
    # Obtener estadísticas de audio del usuario
    audio_stats = db.get_usage_stats(user_id=user_id, action_type="audio_guide")
    audio_count = len(audio_stats)
    
    achievements = []
    
    # Primera audio-guía
    if audio_count == 1:
        achievements.append({
            "user_id": user_id,
            "achievement_type": "visitas",
            "achievement_name": "Primera Audio-Guía",
            "achievement_description": "Generaste tu primera audio-guía",
            "points": 50,
            "badge_icon": "🎧",
            "badge_color": "blue"
        })
    
    # 10 audio-guías
    if audio_count == 10:
        achievements.append({
            "user_id": user_id,
            "achievement_type": "coleccionista",
            "achievement_name": "Coleccionista de Audio",
            "achievement_description": "Generaste 10 audio-guías",
            "points": 200,
            "badge_icon": "🎵",
            "badge_color": "purple"
        })
    
    # Crear logros
    for achievement in achievements:
        result = db.create_achievement(achievement)
        if result:
            st.success(f"🎉 ¡Nuevo logro desbloqueado! {achievement['achievement_name']} (+{achievement['points']} puntos)")
