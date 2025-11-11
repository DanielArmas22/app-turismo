"""
Página de Audio-Guías
"""
import streamlit as st
import config
import os
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
        if not cities:
            st.warning("No hay ciudades disponibles")
            return
            
        city_options = {c['name']: c['id'] for c in cities}
        selected_city_name = st.selectbox(
            "Selecciona una ciudad", 
            list(city_options.keys()), 
            key="audio_page_city_selectbox"
        )
        selected_city_id = city_options[selected_city_name]
        
        # Selección de POI
        pois = db.get_pois(city_id=selected_city_id)
        
        if not pois:
            st.warning("No hay puntos de interés disponibles para esta ciudad")
            return
        
        poi_options = {p['name']: p for p in pois}
        selected_poi_name = st.selectbox(
            "Selecciona un punto de interés", 
            list(poi_options.keys()), 
            key="audio_page_poi_selectbox"
        )
        selected_poi = poi_options[selected_poi_name]
        
        # Contexto adicional
        additional_context = st.text_area(
            "Contexto adicional (opcional)",
            placeholder="Proporciona información específica que quieras incluir en la guía...\nEj: Enfócate en la arquitectura gótica, menciona anécdotas históricas, etc.",
            height=100,
            key="audio_page_context_textarea"
        )
    
    with col2:
        st.markdown("### ⚙️ Configuración")
        
        voice_labels = list(config.AUDIO_VOICES.keys())
        default_voice = "Echo" if "Echo" in config.AUDIO_VOICES else voice_labels[0]
        selected_voice_name = st.selectbox(
            "Voz",
            voice_labels,
            index=voice_labels.index(default_voice),
            key="audio_page_voice_selectbox"
        )
        custom_voice = st.text_input(
            "Voz personalizada (opcional)",
            placeholder="Ingresa el identificador exacto si necesitas una voz distinta...",
            key="audio_page_custom_voice"
        )
        voice_id = custom_voice.strip() or config.AUDIO_VOICES[selected_voice_name]
        
        st.info("💡 Selecciona una voz disponible o ingresa un identificador personalizado.")
    
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
    
    if st.button("🎵 Obtener Audio-Guía", type="primary", use_container_width=True, key="audio_page_generate_button"):
        generate_audio_guide(db, n8n, selected_poi, additional_context, voice_id)


def generate_audio_guide(db, n8n, poi, context, voice_id):
    """Obtiene una audio-guía usando n8n"""
    
    if n8n is None:
        st.error("❌ Error: n8n no está inicializado")
        return
    
    # Mostrar mensaje de espera con información sobre el tiempo estimado
    st.info("⏳ Generando audio-guía... Esto puede tardar varios minutos. Por favor, espera pacientemente...")
    
    with st.spinner("🤖 Obteniendo tu audio-guía personalizada (esto puede tardar varios minutos, por favor espera)..."):
        # Preparar descripción del POI
        poi_description = poi.get('description', '')
        if context:
            poi_description += f"\n\n{context}"
        if not poi_description:
            poi_description = f"Historia, horarios y consejos sobre {poi['name']}"
        
        # Llamar a n8n para obtener la audio-guía
        try:
            result = n8n.generate_audio_guide(
                poi_id=poi['id'],
                poi_name=poi['name'],
                poi_description=poi_description,
                user_id=st.session_state.user_id,
                voice_id=voice_id
            )
        except Exception as e:
            st.error(f"❌ Error al llamar a n8n: {str(e)}")
            return
        
        if result:
            # Inicializar variables al inicio para evitar errores de scope
            audio_url = None
            audio_data_binary = None
            transcription = None
            
            try:
                st.success("✅ ¡Audio-guía obtenida exitosamente!")
                
                # Mostrar reproductor con el audio real
                st.markdown("### 🎧 Tu Audio-Guía")
                
                # Verificar si es un archivo binario de audio
                if result.get('is_binary') and result.get('audio_data'):
                    # Es un archivo binario de audio
                    import io
                    audio_bytes = result.get('audio_data')
                    audio_data_binary = audio_bytes
                    audio_file = io.BytesIO(audio_bytes)
                    st.audio(audio_file, format="audio/mp3")
                    st.info(f"📦 Audio recibido: {result.get('audio_size', 0) / (1024*1024):.2f} MB")
                    # Para archivos binarios, no hay URL pero tenemos los datos
                    audio_url = "binary_audio"  # Marcador para indicar que es binario
                else:
                    # Intentar obtener URL del audio desde la respuesta
                    audio_url = result.get('audio_url') or result.get('audioUrl') or result.get('url')
                    
                    if audio_url:
                        # Si es una ruta de archivo local, usar directamente
                        if os.path.exists(audio_url):
                            st.audio(audio_url, format="audio/mp3")
                            st.info(f"🔗 Archivo de audio: {audio_url}")
                        else:
                            # Si es una URL, usar directamente
                            st.audio(audio_url, format="audio/mp3")
                            st.info(f"🔗 URL del audio: {audio_url}")
                    else:
                        st.warning("⚠️ No se encontró URL del audio en la respuesta")
                        with st.expander("📄 Ver Respuesta Completa", expanded=False):
                            st.json(result)
                
                # Mostrar transcripción si está disponible
                transcription = result.get('transcript') or result.get('transcription') or result.get('text')
                
                if transcription:
                    with st.expander("📄 Ver Transcripción", expanded=True):
                        st.write(transcription)
                else:
                    with st.expander("📄 Ver Respuesta Completa", expanded=False):
                        st.json(result)
                
                # Guardar en base de datos si tenemos los datos necesarios
                if audio_url or audio_data_binary or transcription:
                    # Preparar datos del audio para guardar
                    audio_data = {
                        "poi_id": poi['id'],
                        "language": "es",  # Por defecto, se puede extraer de la respuesta si está disponible
                        "voice_type": voice_id,
                        "transcript": transcription or "",
                        "audio_url": audio_url if audio_url and audio_url != "binary_audio" else "",
                        "duration_seconds": result.get('duration_seconds') or result.get('duration', 0),
                        "generation_model": result.get('model') or "openai-gpt4",
                        "is_active": True
                    }
                    
                    # Si es audio binario, no podemos guardar la URL pero sí los metadatos
                    if audio_data_binary:
                        st.info("💡 Audio binario recibido - se guardarán los metadatos")
                    
                    saved_audio = db.create_audio_guide(audio_data)
                    if saved_audio:
                        st.success("💾 Audio-guía guardada en tu biblioteca")
                
                # Registrar estadística
                db.create_usage_stat({
                    "user_id": st.session_state.user_id,
                    "action_type": "audio_guide",
                    "poi_id": poi['id'],
                    "metadata": {
                        "voice_id": voice_id,
                        "poi_name": poi['name'],
                        "has_audio": bool(audio_url),
                        "has_transcript": bool(transcription)
                    }
                })
                
                # Verificar logros
                check_audio_achievements(db, st.session_state.user_id)
                
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error al procesar la respuesta: {str(e)}")
        else:
            st.error("❌ No se pudo obtener la audio-guía. Por favor, verifica:")
            st.error("1. Que el endpoint de n8n esté funcionando")
            st.error("2. Que los parámetros sean correctos")
            st.error("3. Que tengas conexión a internet")


def show_my_audios(db, n8n):
    """Muestra las audio-guías del usuario"""
    
    st.subheader("📚 Mis Audio-Guías")
    
    # Obtener audio-guías guardadas en la base de datos
    # Primero obtener estadísticas para contar
    audio_stats = db.get_usage_stats(
        user_id=st.session_state.user_id,
        action_type="audio_guide",
        limit=50
    )
    
    # Obtener POIs visitados para obtener sus audio-guías
    pois_with_audio = []
    for stat in audio_stats:
        poi_id = stat.get('poi_id')
        if poi_id:
            poi = db.get_poi_by_id(poi_id)
            if poi:
                # Obtener audio-guías del POI
                audio_guides = db.get_audio_guides(poi_id)
                for audio in audio_guides:
                    pois_with_audio.append({
                        'poi': poi,
                        'audio': audio,
                        'stat': stat
                    })
    
    if not pois_with_audio:
        st.info("Aún no has generado ninguna audio-guía. ¡Crea tu primera guía en la pestaña anterior!")
        return
    
    # Mostrar métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎧 Total Generadas", len(pois_with_audio))
    with col2:
        # Calcular tiempo total
        total_seconds = sum(a.get('audio', {}).get('duration_seconds', 0) for a in pois_with_audio)
        total_minutes = total_seconds // 60
        st.metric("⏱️ Tiempo Total", f"{total_minutes} min")
    with col3:
        # Idiomas únicos
        languages = set(a.get('audio', {}).get('language', 'es') for a in pois_with_audio)
        st.metric("🌍 Idiomas", len(languages))
    
    st.markdown("---")
    
    # Listar audio-guías
    for idx, item in enumerate(pois_with_audio):
        poi = item['poi']
        audio = item['audio']
        stat = item.get('stat', {})
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"### 🎧 {poi['name']}")
                
                # Información
                info_cols = st.columns(4)
                with info_cols[0]:
                    city_name = poi.get('cities', {}).get('name', 'N/A') if isinstance(poi.get('cities'), dict) else 'N/A'
                    st.caption(f"📍 {city_name}")
                with info_cols[1]:
                    lang = audio.get('language', 'es')
                    st.caption(f"🌍 {lang.upper()}")
                with info_cols[2]:
                    duration_sec = audio.get('duration_seconds', 0)
                    duration_min = duration_sec // 60 if duration_sec else 0
                    st.caption(f"⏱️ {duration_min} min")
                with info_cols[3]:
                    created_at = audio.get('created_at', '')
                    if created_at:
                        try:
                            date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            st.caption(f"📅 {date.strftime('%d/%m/%Y')}")
                        except:
                            st.caption("📅 N/A")
                
                # Mostrar audio si está disponible
                audio_url = audio.get('audio_url')
                if audio_url:
                    st.audio(audio_url, format="audio/mp3")
                else:
                    st.warning("⚠️ URL de audio no disponible")
            
            with col2:
                if audio_url:
                    if st.button("▶️ Reproducir", key=f"play_{idx}", use_container_width=True):
                        st.audio(audio_url, format="audio/mp3")
                
                if st.button("📄 Ver Detalles", key=f"details_{idx}", use_container_width=True):
                    show_audio_details(db, poi, audio)
            
            st.divider()


def show_audio_details(db, poi, audio):
    """Muestra los detalles de una audio-guía"""
    
    with st.expander(f"📄 Detalles de Audio-Guía: {poi['name']}", expanded=True):
        # Información del POI
        st.markdown(f"### {poi['name']}")
        st.write(poi.get('description', 'Sin descripción'))
        
        # Metadatos
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            lang = audio.get('language', 'es')
            st.metric("Idioma", lang.upper())
        with col2:
            duration_sec = audio.get('duration_seconds', 0)
            duration_min = duration_sec // 60 if duration_sec else 0
            st.metric("Duración", f"{duration_min} min")
        with col3:
            voice_type = audio.get('voice_type', 'N/A')
            st.metric("Voz", voice_type[:10] if len(str(voice_type)) > 10 else voice_type)
        with col4:
            play_count = audio.get('play_count', 0)
            st.metric("Reproducciones", play_count)
        
        # Reproductor
        audio_url = audio.get('audio_url')
        if audio_url:
            st.markdown("### 🎧 Reproducir")
            st.audio(audio_url, format="audio/mp3")
            st.info(f"🔗 URL: {audio_url}")
        else:
            st.warning("⚠️ URL de audio no disponible")
        
        # Transcripción
        transcript = audio.get('transcript')
        if transcript:
            st.markdown("### 📄 Transcripción")
            st.write(transcript)
        else:
            st.info("ℹ️ No hay transcripción disponible para esta audio-guía")
        
        # Información adicional
        with st.expander("ℹ️ Información Técnica", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Modelo:** {audio.get('generation_model', 'N/A')}")
                st.write(f"**Tamaño del archivo:** {audio.get('file_size_bytes', 0)} bytes")
            with col2:
                created_at = audio.get('created_at', '')
                if created_at:
                    try:
                        date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        st.write(f"**Creada:** {date.strftime('%d/%m/%Y %H:%M')}")
                    except:
                        st.write("**Creada:** N/A")
                
                last_played = audio.get('last_played_at')
                if last_played:
                    try:
                        date = datetime.fromisoformat(last_played.replace('Z', '+00:00'))
                        st.write(f"**Última reproducción:** {date.strftime('%d/%m/%Y %H:%M')}")
                    except:
                        pass


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
