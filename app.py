"""
Aplicación Principal - Guía Turística Virtual
"""
import streamlit as st
from database import get_database
from n8n_integration import get_n8n_integration
import config

# Configuración de la página
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.APP_LAYOUT,
    initial_sidebar_state="expanded"
)

# Inicializar conexiones
db = get_database()
n8n = get_n8n_integration()

# Inicializar session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = None
if 'selected_poi' not in st.session_state:
    st.session_state.selected_poi = None

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Autenticación y Navegación
with st.sidebar:
    st.markdown(f"# {config.APP_ICON} Guía Turística")
    st.markdown("---")
    
    # Sistema de autenticación simple
    if st.session_state.user_id is None:
        st.subheader("🔐 Iniciar Sesión")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="tu@email.com")
            name = st.text_input("Nombre", placeholder="Tu nombre")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit and email and name:
                # Buscar o crear usuario
                user = db.get_user_by_email(email)
                
                if user is None:
                    # Crear nuevo usuario
                    user = db.create_user({
                        "email": email,
                        "name": name,
                        "subscription_tier": "free"
                    })
                    if user:
                        st.success(f"¡Bienvenido {name}! 🎉")
                
                if user:
                    st.session_state.user_id = user['id']
                    st.session_state.user_email = user['email']
                    st.session_state.user_data = user
                    st.rerun()
    else:
        # Usuario autenticado
        user_data = st.session_state.user_data
        st.success(f"👤 {user_data['name']}")
        st.info(f"🎖️ {user_data['subscription_tier'].title()}")
        st.metric("Puntos", user_data.get('total_points', 0))
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.user_data = None
            st.rerun()
        
        st.markdown("---")
    
    # Navegación
    st.subheader("📍 Navegación")
    
    menu_options = {
        "🏠 Inicio": "home",
        "🌍 Explorar Ciudades": "cities",
        "📍 Puntos de Interés": "pois",
        "🎧 Audio-Guías": "audio",
        "🎫 Mis Reservas": "bookings",
        "⭐ Favoritos": "favorites",
        "🎮 Gamificación": "achievements",
        "📊 Estadísticas": "stats",
        "📄 Reportes": "reports"
    }
    
    selected_page = st.radio(
        "Selecciona una página",
        list(menu_options.keys()),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Configuración
    st.subheader("⚙️ Configuración")
    language = st.selectbox("Idioma", list(config.LANGUAGES.values()))
    dark_mode = st.toggle("Modo Oscuro", value=False)

# Contenido principal basado en la página seleccionada
page = menu_options[selected_page]

if page == "home":
    # PÁGINA DE INICIO
    st.markdown('<h1 class="main-header">🏛️ Guía Turística Virtual</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Bienvenido a tu experiencia turística inteligente
    
    Descubre el mundo de una manera completamente nueva con nuestra plataforma impulsada por IA.
    """)
    
    # Características principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎧 Audio-Guías IA</h3>
            <p>Contenido generado por inteligencia artificial adaptado a tus intereses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📍 Recomendaciones</h3>
            <p>Descubre lugares únicos basados en tu ubicación y preferencias</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎮 Gamificación</h3>
            <p>Gana puntos y logros mientras exploras el mundo</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Métricas globales
    st.subheader("📊 Estadísticas Globales")
    
    try:
        cities = db.get_cities() or []
        pois = db.get_pois() or []
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        cities = []
        pois = []
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌍 Ciudades", len(cities))
    with col2:
        st.metric("📍 Puntos de Interés", len(pois))
    with col3:
        st.metric("🎧 Audio-Guías", "1,247")
    with col4:
        st.metric("👥 Usuarios", "5,892")
    
    st.markdown("---")
    
    # Ciudades destacadas
    st.subheader("🌟 Ciudades Destacadas")
    
    if cities and len(cities) > 0:
        cols = st.columns(min(4, len(cities)))
        for idx, city in enumerate(cities[:4]):
            if city:  # Verificar que city no sea None
                with cols[idx]:
                    st.image(city.get('image_url', 'https://via.placeholder.com/300x200'), 
                            width=300)
                    st.markdown(f"**{city.get('name', 'Sin nombre')}**")
                    st.caption(f"{city.get('country', 'N/A')} • €{city.get('price', 0)}")
                    if st.button("Explorar", key=f"city_{city.get('id', idx)}", use_container_width=True):
                        st.session_state.selected_city = city.get('id')
                        st.rerun()
    else:
        st.info("📍 No hay ciudades disponibles. Agrega ciudades desde Supabase para comenzar.")
    
    # Call to action
    st.markdown("---")
    st.info("💡 **Consejo:** Inicia sesión para acceder a todas las funcionalidades y comenzar a ganar puntos.")

elif page == "cities":
    from pages import cities_page
    cities_page.show(db, n8n)

elif page == "pois":
    from pages import pois_page
    pois_page.show(db, n8n)

elif page == "audio":
    from pages import audio_page
    audio_page.show(db, n8n)

elif page == "bookings":
    from pages import bookings_page
    bookings_page.show(db, n8n)

elif page == "favorites":
    from pages import favorites_page
    favorites_page.show(db, n8n)

elif page == "achievements":
    from pages import achievements_page
    achievements_page.show(db, n8n)

elif page == "stats":
    from pages import stats_page
    stats_page.show(db, n8n)

elif page == "reports":
    from pages import reports_page
    reports_page.show(db, n8n)

# Footer
st.markdown("---")
st.caption("🏛️ Guía Turística Virtual - Powered by n8n, Supabase & OpenAI")
