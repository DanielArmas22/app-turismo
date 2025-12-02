"""
Aplicación Principal - Guía Turística Virtual
"""
import streamlit as st
from database import get_database
from n8n import get_n8n_integration
import config.config as config
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
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'show_city_detail' not in st.session_state:
    st.session_state.show_city_detail = False
if 'main_menu' not in st.session_state:
    st.session_state.main_menu = "🏠 Inicio"


def ensure_user_role(user: dict | None) -> dict | None:
    """Garantiza que el diccionario de usuario siempre tenga un rol válido."""
    if not user:
        return user
    if not user.get("role"):
        user["role"] = "user"
    return user


def get_current_role() -> str:
    """Obtiene el rol asociado al usuario actual."""
    user_data = st.session_state.get("user_data") or {}
    if st.session_state.get("user_id"):
        return user_data.get("role", "user")
    return "guest"


def navigate_to_city(city_id: str):
    """Navega a la vista detallada de una ciudad."""
    st.session_state.selected_city = city_id
    st.session_state.show_city_detail = True
    st.session_state.main_menu = "🌍 Explorar Ciudades"
    st.rerun()

# CSS personalizado mejorado
st.markdown("""
<style>
    :root {
        --primary-500: #6750f8;
        --primary-600: #5b3df0;
        --primary-700: #4526d9;
        --accent-500: #f97316;
        --bg-soft: #f4f5ff;
        --text-muted: #5d5f77;
    }

    body {
        background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 35%);
    }

    /* Header principal */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        line-height: 1.1;
        background: linear-gradient(90deg, var(--primary-500) 0%, var(--accent-500) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.8rem;
    }

    /* Hero */
    .hero {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 2rem;
        padding: 1.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.12) 0%, rgba(103, 80, 248, 0.35) 100%);
        position: relative;
        overflow: hidden;
        box-shadow: 0 30px 60px -40px rgba(50, 65, 208, 0.55);
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        pointer-events: none;
    }

    .hero-content {
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        z-index: 1;
    }

    .hero-visual {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .hero-visual img {
        width: 100%;
        max-width: 320px;
        border-radius: 20px;
        box-shadow: 0 20px 45px -25px rgba(14, 21, 58, 0.65);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.35);
        border-radius: 999px;
        padding: 0.45rem 1.1rem;
        font-weight: 600;
        color: var(--primary-700);
        width: fit-content;
        backdrop-filter: blur(8px);
    }

    .hero-actions {
        display: inline-flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .cta-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        padding: 0.75rem 1.6rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.95rem;
        color: white;
        text-decoration: none;
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--accent-500) 100%);
        box-shadow: 0 18px 35px -22px rgba(103, 80, 248, 0.9);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .cta-button.secondary {
        background: rgba(255, 255, 255, 0.92);
        color: #1c1f3b;
        border: 1px solid rgba(103, 80, 248, 0.24);
        box-shadow: none;
    }

    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 22px 40px -25px rgba(103, 80, 248, 0.75);
    }

    .cta-button.secondary:hover {
        box-shadow: 0 22px 35px -26px rgba(28, 31, 59, 0.35);
    }

    .hero-description {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 520px;
    }

    /* Feature cards */
    .feature-card {
        position: relative;
        padding: 1.6rem;
        border-radius: 18px;
        background: white;
        border: 1px solid #f0f1ff;
        box-shadow: 0 14px 30px -18px rgba(29, 41, 112, 0.35);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
        gap: 0.85rem;
    }

    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 25px 35px -25px rgba(50, 65, 208, 0.5);
    }

    .feature-card h3 {
        font-size: 1.25rem;
        margin: 0;
        color: #1c1f3b;
    }

    .feature-card p {
        margin: 0;
        color: var(--text-muted);
        line-height: 1.6;
    }

    .feature-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.14), rgba(249, 115, 22, 0.22));
        color: var(--primary-600);
    }

    .feature-chip {
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--accent-500);
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        font-weight: 600;
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.18), rgba(249, 115, 22, 0.24));
        color: var(--primary-700);
        font-size: 0.85rem;
    }

    /* Metric cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0 2.5rem;
    }

    .metric-card {
        padding: 1.4rem;
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(255,255,255,0.92) 0%, rgba(244, 245, 255, 1) 100%);
        position: relative;
        border: 1px solid rgba(103, 80, 248, 0.18);
        overflow: hidden;
    }

    .metric-card::after {
        content: "";
        position: absolute;
        inset: 0;
        backdrop-filter: blur(50px);
        opacity: 0.45;
        pointer-events: none;
    }

    .metric-card strong {
        display: block;
        font-size: 2rem;
        z-index: 1;
        position: relative;
        color: #1c1f3b;
    }

    .metric-card span {
        position: relative;
        z-index: 1;
        font-size: 0.95rem;
        color: var(--text-muted);
    }

    /* City cards */
    .city-card {
        position: relative;
        height: 220px;
        border-radius: 20px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-end;
        box-shadow: 0 25px 45px -36px rgba(14, 21, 58, 0.65);
    }

    .city-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(18, 24, 39, 0) 0%, rgba(18, 24, 39, 0.75) 100%);
    }

    .city-overlay {
        position: relative;
        padding: 1.25rem;
        color: white;
        width: 100%;
    }

    .city-overlay h4 {
        margin: 0 0 0.45rem 0;
        font-size: 1.1rem;
    }

    .city-meta {
        font-size: 0.9rem;
        opacity: 0.85;
    }

    /* CTA tips */
    .cta-card {
        border-radius: 18px;
        padding: 1.6rem;
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.1), rgba(249, 115, 22, 0.1));
        border: 1px dashed rgba(103, 80, 248, 0.35);
        color: var(--primary-600);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.65rem 1.1rem;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, var(--primary-600), var(--primary-700));
        color: white;
        box-shadow: 0 12px 22px -18px rgba(103, 80, 248, 0.7);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 22px 28px -20px rgba(103, 80, 248, 0.65);
    }

    .stButton>button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(103, 80, 248, 0.25);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f4f5ff 0%, #ffffff 100%);
        border-right: 1px solid rgba(103, 80, 248, 0.12);
    }

    .sidebar-header {
        display: flex;
        gap: 0.9rem;
        align-items: center;
        padding: 1.2rem 1rem 0.8rem;
    }

    .sidebar-header h2 {
        margin: 0;
        font-size: 1.4rem;
        color: #1c1f3b;
    }

    .sidebar-header p {
        margin: 0;
        color: var(--text-muted);
        font-size: 0.92rem;
    }

    .sidebar-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: grid;
        place-items: center;
        font-size: 1.4rem;
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.18), rgba(249, 115, 22, 0.24));
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 0.95rem 1.1rem;
        box-shadow: 0 20px 40px -35px rgba(28, 31, 59, 0.65);
        border: 1px solid rgba(103, 80, 248, 0.08);
        margin: 0.6rem 0;
    }

    .sidebar-section-title {
        text-transform: uppercase;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        margin-bottom: 0.8rem;
        color: var(--text-muted);
        font-weight: 700;
    }

    /* Radio buttons */
    div[data-baseweb="radio"] > div {
        gap: 0.5rem;
    }

    div[data-baseweb="radio"] label {
        border-radius: 12px;
        padding: 0.65rem 0.85rem;
        transition: all 0.2s ease;
        border: 1px solid transparent;
        font-weight: 500;
        color: #1c1f3b;
    }

    div[data-baseweb="radio"] label:hover {
        background: rgba(103, 80, 248, 0.07);
        border-color: rgba(103, 80, 248, 0.32);
    }

    div[data-baseweb="radio"] input:checked + div {
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.12), rgba(103, 80, 248, 0.05));
        border-radius: 12px;
        border: 1px solid rgba(103, 80, 248, 0.35);
    }

    /* Tabs mejorados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }

    /* Dataframes mejorados */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Expanders mejorados */
    .streamlit-expanderHeader {
        font-weight: 600;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.75rem;
    }

    /* Inputs mejorados */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid rgba(103, 80, 248, 0.15);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        padding: 0.35rem 0.75rem;
    }

    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: var(--primary-500);
        box-shadow: 0 0 0 3px rgba(103, 80, 248, 0.18);
    }

    /* Animaciones suaves */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }

    /* --- Overrides y mejoras de contraste --- */
    body {
        background: radial-gradient(circle at top left, rgba(103, 80, 248, 0.12), transparent 45%),
                    radial-gradient(circle at 120% 0%, rgba(56, 189, 248, 0.12), transparent 40%),
                    linear-gradient(180deg, #f9f9ff 0%, #ffffff 45%);
        color: #1c1f3b;
    }

    .hero {
        padding: clamp(2.2rem, 4vw, 3.1rem);
        border-radius: 28px;
        background: linear-gradient(140deg, rgba(247, 244, 255, 0.95) 0%, rgba(232, 243, 255, 0.95) 60%, rgba(237, 233, 255, 0.95) 100%);
        border: 1px solid rgba(99, 102, 241, 0.18);
        box-shadow: 0 36px 80px -45px rgba(58, 72, 166, 0.4);
    }

    .hero::after {
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.15);
    }

    .hero-badge {
        background: rgba(255, 255, 255, 0.92);
        color: #4338ca;
        box-shadow: 0 12px 25px -20px rgba(76, 29, 149, 0.45);
    }

    .hero-description {
        color: #34345f;
    }

    .home-layout {
        display: flex;
        flex-direction: column;
        gap: 2.6rem;
    }

    .section-block {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(246, 248, 255, 0.98));
        border-radius: 28px;
        padding: clamp(2rem, 3.2vw, 2.8rem);
        border: 1px solid rgba(28, 31, 59, 0.08);
        box-shadow: 0 30px 70px -55px rgba(47, 54, 110, 0.55);
    }

    .section-header {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
        margin-bottom: 1.8rem;
    }

    .section-header span {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: rgba(76, 29, 149, 0.6);
    }

    .section-header h2 {
        margin: 0;
        font-size: clamp(1.7rem, 2vw, 2.1rem);
        color: #1c1f3b;
    }

    .section-header p {
        margin: 0;
        color: #485072;
        max-width: 560px;
        line-height: 1.7;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.4rem;
    }

    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(242, 245, 255, 0.95) 100%);
        border: 1px solid rgba(103, 80, 248, 0.12);
        box-shadow: 0 22px 45px -35px rgba(50, 65, 208, 0.35);
        margin: 0;
    }

    .feature-card p {
        color: #4d5575;
    }

    .feature-icon {
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.16), rgba(56, 189, 248, 0.2));
        color: #4f46e5;
    }

    .feature-chip {
        color: #ea580c;
    }

    .metric-grid {
        margin-top: 1.5rem;
        margin-bottom: 0;
    }

    .metric-card {
        background: linear-gradient(160deg, rgba(255,255,255,0.98) 0%, rgba(239, 244, 255, 0.98) 100%);
        border: 1px solid rgba(103, 80, 248, 0.2);
        box-shadow: 0 24px 55px -48px rgba(50, 65, 208, 0.5);
    }

    .metric-card span {
        color: #4d5575;
    }

    .city-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.4rem;
    }

    .city-card {
        margin-bottom: 0;
        box-shadow: 0 25px 55px -38px rgba(14, 21, 58, 0.55);
    }

    .cta-card {
        border-radius: 20px;
        padding: 1.8rem;
        background: linear-gradient(140deg, rgba(250, 245, 255, 0.95), rgba(237, 250, 255, 0.95));
        border: 1px dashed rgba(103, 80, 248, 0.3);
        color: #4338ca;
        box-shadow: 0 26px 60px -52px rgba(59, 130, 246, 0.45);
    }

    .empty-state {
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        background: rgba(103, 80, 248, 0.08);
        border: 1px dashed rgba(103, 80, 248, 0.22);
        color: #4338ca;
        font-weight: 600;
        text-align: center;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(249, 250, 255, 0.96) 0%, rgba(255, 255, 255, 0.96) 100%);
        border-right: 1px solid rgba(103, 80, 248, 0.08);
        box-shadow: inset -1px 0 0 rgba(103, 80, 248, 0.06);
    }

    .sidebar-header p {
        color: rgba(93, 95, 119, 0.78);
    }

    .sidebar-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(243, 245, 255, 0.98));
        border-radius: 18px;
        padding: 1.05rem 1.25rem;
        box-shadow: 0 24px 50px -40px rgba(28, 31, 59, 0.38);
        border: 1px solid rgba(103, 80, 248, 0.12);
        margin: 0.75rem 0;
    }

    .sidebar-section-title {
        color: rgba(84, 86, 112, 0.72);
    }

    div[data-baseweb="radio"] label {
        border: 1px solid rgba(28, 31, 59, 0.08);
        background: rgba(255, 255, 255, 0.85);
    }

    div[data-baseweb="radio"] input:checked + div {
        background: linear-gradient(135deg, rgba(103, 80, 248, 0.14), rgba(56, 189, 248, 0.16));
        border: 1px solid rgba(103, 80, 248, 0.4);
    }

    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 12px;
        border: 1px solid rgba(28, 31, 59, 0.12);
        padding: 0.45rem 0.85rem;
        background: rgba(255, 255, 255, 0.92);
        color: #1c1f3b;
    }

    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: rgba(99, 102, 241, 0.55);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, #0f172a 0%, #111827 35%);
            color: #e2e8f0;
        }

        .main-header {
            background: linear-gradient(90deg, #c084fc 0%, #38bdf8 100%);
        }

        .hero {
            background: linear-gradient(135deg, rgba(100, 116, 255, 0.25) 0%, rgba(59, 130, 246, 0.18) 100%);
            box-shadow: 0 25px 60px -40px rgba(15, 23, 42, 0.9);
        }

        .hero::after {
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .hero-badge {
            background: rgba(30, 64, 175, 0.35);
            color: #bfdbfe;
        }

        .hero-description {
            color: rgba(15, 23, 42, 0.9);
        }

        .cta-button.secondary {
            background: rgba(15, 23, 42, 0.85);
            color: #e2e8f0;
            border: 1px solid rgba(148, 163, 184, 0.4);
        }

        .feature-card {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.92) 0%, rgba(17, 24, 39, 0.88) 100%);
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: 0 25px 45px -36px rgba(15, 23, 42, 0.9);
        }

        .feature-card h3 {
            color: #f8fafc;
        }

        .feature-card p {
            color: rgba(226, 232, 240, 0.78);
        }

        .feature-chip {
            color: #facc15;
        }

        .feature-icon {
            background: linear-gradient(135deg, rgba(100, 116, 255, 0.25), rgba(14, 165, 233, 0.25));
            color: #c084fc;
        }

        .metric-card {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.92) 0%, rgba(30, 41, 59, 0.88) 100%);
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        .metric-card strong {
            color: #f8fafc;
        }

        .metric-card span {
            color: rgba(226, 232, 240, 0.65);
        }

        .city-card::before {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0) 0%, rgba(15, 23, 42, 0.85) 100%);
        }

        .city-overlay h4 {
            color: #f8fafc;
        }

        .city-meta {
            color: rgba(226, 232, 240, 0.75);
        }

        .cta-card {
            background: linear-gradient(135deg, rgba(30, 64, 175, 0.18), rgba(14, 165, 233, 0.18));
            border: 1px dashed rgba(148, 163, 184, 0.4);
            color: #bae6fd;
        }

        .stButton>button {
            background: linear-gradient(135deg, #6d28d9, #2563eb);
            box-shadow: 0 18px 35px -22px rgba(59, 130, 246, 0.65);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            border-right: 1px solid rgba(100, 116, 255, 0.18);
        }

        .sidebar-card {
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid rgba(148, 163, 184, 0.12);
            color: #e2e8f0;
        }

        .sidebar-section-title {
            color: rgba(148, 163, 184, 0.7);
        }

        .sidebar-header h2 {
            color: #f8fafc;
        }

        .sidebar-header p {
            color: rgba(226, 232, 240, 0.68);
        }

        .sidebar-icon {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.35), rgba(16, 185, 129, 0.35));
        }

        div[data-baseweb="radio"] label {
            color: #f1f5f9;
        }

        div[data-baseweb="radio"] label:hover {
            background: rgba(79, 70, 229, 0.18);
            border-color: rgba(99, 102, 241, 0.35);
        }

        div[data-baseweb="radio"] input:checked + div {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.22), rgba(37, 99, 235, 0.18));
            border: 1px solid rgba(129, 140, 248, 0.42);
        }

        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background: rgba(15, 23, 42, 0.92);
            border: 2px solid rgba(148, 163, 184, 0.18);
            color: #e2e8f0;
        }

        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus,
        .stSelectbox>div>div>select:focus {
            border-color: rgba(129, 140, 248, 0.6);
            box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
        }

        /* --- Overrides modo oscuro --- */
        body {
            background: radial-gradient(circle at top left, rgba(30, 64, 175, 0.25), transparent 45%),
                        radial-gradient(circle at 120% 0%, rgba(6, 182, 212, 0.22), transparent 40%),
                        linear-gradient(180deg, #0f172a 0%, #111827 45%);
            color: #e2e8f0;
        }

        .hero {
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: linear-gradient(140deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.92));
            box-shadow: 0 45px 95px -65px rgba(2, 6, 23, 0.95);
        }

        .hero::after {
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        .hero-badge {
            background: rgba(59, 130, 246, 0.22);
            color: #e0e7ff;
        }

        .hero-description {
            color: rgba(226, 232, 240, 0.85);
        }

        .section-block {
            background: linear-gradient(145deg, rgba(17, 24, 39, 0.92), rgba(30, 41, 59, 0.92));
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: 0 45px 100px -75px rgba(2, 6, 23, 1);
        }

        .section-header span {
            color: rgba(165, 180, 252, 0.75);
        }

        .section-header h2 {
            color: #f8fafc;
        }

        .section-header p {
            color: rgba(226, 232, 240, 0.7);
        }

        .feature-card {
            background: linear-gradient(145deg, rgba(17, 24, 39, 0.95), rgba(30, 41, 59, 0.95));
            border: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: 0 30px 70px -48px rgba(2, 6, 23, 0.85);
        }

        .feature-card h3 {
            color: #f8fafc;
        }

        .feature-card p {
            color: rgba(226, 232, 240, 0.75);
        }

        .feature-icon {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.32), rgba(14, 165, 233, 0.32));
            color: #c084fc;
        }

        .metric-card {
            background: linear-gradient(160deg, rgba(17, 24, 39, 0.95), rgba(30, 41, 59, 0.95));
            border: 1px solid rgba(148, 163, 184, 0.18);
            box-shadow: 0 30px 70px -58px rgba(2, 6, 23, 0.9);
        }

        .metric-card span {
            color: rgba(226, 232, 240, 0.65);
        }

        .city-card::before {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0) 0%, rgba(15, 23, 42, 0.88) 100%);
        }

        .city-overlay h4 {
            color: #f8fafc;
        }

        .city-meta {
            color: rgba(226, 232, 240, 0.75);
        }

        .cta-card {
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.92), rgba(17, 24, 39, 0.92));
            border: 1px dashed rgba(148, 163, 184, 0.35);
            color: #bfdbfe;
        }

        .empty-state {
            background: rgba(59, 130, 246, 0.18);
            border: 1px dashed rgba(148, 163, 184, 0.28);
            color: #bfdbfe;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.96));
            border-right: 1px solid rgba(100, 116, 255, 0.18);
        }

        .sidebar-card {
            background: linear-gradient(145deg, rgba(17, 24, 39, 0.94), rgba(30, 41, 59, 0.94));
            border: 1px solid rgba(148, 163, 184, 0.12);
            color: #e2e8f0;
            box-shadow: 0 30px 65px -52px rgba(2, 6, 23, 0.85);
        }

        .sidebar-section-title {
            color: rgba(148, 163, 184, 0.7);
        }

        .sidebar-header h2 {
            color: #f8fafc;
        }

        .sidebar-header p {
            color: rgba(226, 232, 240, 0.65);
        }

        div[data-baseweb="radio"] label {
            color: #f1f5f9;
            border-color: rgba(30, 41, 59, 0.35);
            background: rgba(15, 23, 42, 0.85);
        }

        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select {
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.18);
            color: #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Autenticación y Navegación
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-icon">{config.APP_ICON}</div>
        <div>
            <h2>Guía Turística</h2>
            <p>Explora, reserva y vive experiencias únicas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sistema de autenticación simple
    if st.session_state.user_id is None:
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-section-title">Acceso rápido</div>
            <p>Inicia sesión para sincronizar itinerarios y favoritos en cualquier dispositivo.</p>
        </div>
        """, unsafe_allow_html=True)

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
                    user = ensure_user_role(user)
                    st.session_state.user_id = user['id']
                    st.session_state.user_email = user['email']
                    st.session_state.user_data = user
                    st.rerun()
    else:
        user_data = ensure_user_role(st.session_state.user_data)
        st.session_state.user_data = user_data
        user_role = get_current_role()
        role_labels = {
            "admin": "Administrador",
            "user": "Explorador",
            "guest": "Invitado"
        }
        role_badge = role_labels.get(user_role, user_role.title())
        st.markdown(f"""
        <div class="sidebar-card fade-in">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:0.5rem;">
                <div>
                    <div class="sidebar-section-title">Mi perfil</div>
                    <strong>👤 {user_data['name']}</strong>
                </div>
                <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
                    <span class="badge">{user_data['subscription_tier'].title()}</span>
                    <span class="badge">{role_badge}</span>
                </div>
            </div>
            <div style="margin-top:0.75rem;">
                <small style="color:var(--text-muted);">Puntos acumulados</small>
                <div style="font-size:1.4rem; font-weight:700;">{user_data.get('total_points', 0)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.user_data = None
            st.rerun()

    st.markdown("""
    <div class="sidebar-card" style="margin-top:1.2rem;">
        <div class="sidebar-section-title">Navegación</div>
        <p style="margin-bottom:0;">Descubre las funciones disponibles y salta rápidamente entre módulos.</p>
    </div>
    """, unsafe_allow_html=True)

    current_role = get_current_role()
    is_admin = current_role == "admin"
    
    menu_sequence = [
        ("🏠 Inicio", "home"),
        ("🌍 Explorar Ciudades", "cities"),
        ("📍 Puntos de Interés", "pois"),
        ("🎯 Recomendaciones", "recommendations"),
        ("🎧 Audio-Guías", "audio"),
        ("🎫 Mis Reservas", "bookings"),
        ("⭐ Favoritos", "favorites"),
        ("🎮 Gamificación", "achievements"),
        ("📄 Reportes", "reports")
    ]
    
    if is_admin:
        menu_sequence.extend([
            ("📊 Estadísticas", "stats"),
            ("⚙️ Administración", "admin")
        ])
    
    menu_options = dict(menu_sequence)
    available_menu_labels = list(menu_options.keys())
    if st.session_state.main_menu not in available_menu_labels:
        st.session_state.main_menu = available_menu_labels[0]
    
    selected_page = st.radio(
        "Selecciona una página",
        available_menu_labels,
        label_visibility="collapsed",
        key="main_menu"
    )

    # Configuración
    st.markdown("""
    <div class="sidebar-card" style="margin-top:1.2rem;">
        <div class="sidebar-section-title">Personaliza tu experiencia</div>
    </div>
    """, unsafe_allow_html=True)

    language = st.selectbox("Idioma", list(config.LANGUAGES.values()))
    dark_mode = st.toggle("Modo Oscuro", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()

# Contenido principal basado en la página seleccionada
page = menu_options[selected_page]

if page == "home":
    st.markdown('<div class="home-layout">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero fade-in">
        <div class="hero-content">
            <span class="hero-badge">✨ Nueva generación de turismo inteligente</span>
            <h1 class="main-header">Guía Turística Virtual</h1>
            <p class="hero-description">
                Diseña itinerarios personalizados con recomendaciones en tiempo real, audio-guías conversacionales y experiencias inmersivas en las mejores ciudades del mundo.
            </p>
            <div class="hero-actions">
                <a href="#destacadas" class="cta-button">Explorar ciudades</a>
                <a href="#estadisticas" class="cta-button secondary">Ver estadísticas</a>
            </div>
        </div>
        <div class="hero-visual">
            <img src="https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=720&q=80" alt="Experiencias turísticas" />
        </div>
    </div>
    """, unsafe_allow_html=True)

    features = [
        {
            "icon": "🎧",
            "title": "Audio-Guías IA",
            "description": "Recorridos narrados con inteligencia artificial que se adaptan a tu ritmo y estilo de viaje.",
            "chip": "Personalizado"
        },
        {
            "icon": "📍",
            "title": "Recomendaciones vivas",
            "description": "Encuentra experiencias imperdibles según clima, temporada y tus intereses actuales.",
            "chip": "Contexto en vivo"
        },
        {
            "icon": "🎮",
            "title": "Gamificación",
            "description": "Desbloquea logros, gana puntos y comparte tu progreso con otros exploradores.",
            "chip": "Modo aventura"
        }
    ]

    st.markdown("""
    <div class="section-block fade-in">
        <div class="section-header">
            <span>Experiencias inteligentes</span>
            <h2>Todo lo que necesitas para viajar mejor</h2>
            <p>Planifica, escucha y vive cada destino con herramientas diseñadas para acompañarte en todo momento.</p>
        </div>
        <div class="feature-grid">
    """, unsafe_allow_html=True)

    for feature in features:
        st.markdown(f"""
        <article class="feature-card fade-in">
            <span class="feature-icon">{feature['icon']}</span>
            <div class="feature-chip">{feature['chip']}</div>
            <h3>{feature['title']}</h3>
            <p>{feature['description']}</p>
        </article>
        """, unsafe_allow_html=True)

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        cities = db.get_cities() or []
        pois = db.get_pois() or []
        audio_guides = db.get_audio_guides() or []
        users = db.get_all_users() or []
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        cities = []
        pois = []
        audio_guides = []
        users = []

    metrics_html = f"""
    <div class="section-block fade-in" id="estadisticas">
        <div class="section-header">
            <span>Impacto global</span>
            <h2>Estadísticas en tiempo real</h2>
            <p>Observa cómo evoluciona la comunidad de viajeros y los contenidos disponibles en la plataforma.</p>
        </div>
        <div class="metric-grid">
            <div class="metric-card">
                <span>🌍 Ciudades activas</span>
                <strong>{len(cities)}</strong>
            </div>
            <div class="metric-card">
                <span>📍 Puntos de interés</span>
                <strong>{len(pois)}</strong>
            </div>
            <div class="metric-card">
                <span>🎧 Audio-guías disponibles</span>
                <strong>{len(audio_guides)}</strong>
            </div>
            <div class="metric-card">
                <span>👥 Viajeros conectados</span>
                <strong>{len(users)}</strong>
            </div>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-block fade-in" id="destacadas">', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <span>Destinos recomendados</span>
            <h2>Ciudades destacadas</h2>
            <p>Explora los hotspots más reservados por nuestra comunidad y descubre qué hace únicos a estos destinos.</p>
        </div>
        """, unsafe_allow_html=True)

        if cities and len(cities) > 0:
            cols = st.columns(min(4, len(cities)))
            for idx, city in enumerate(cities[:4]):
                if city:
                    with cols[idx]:
                        placeholder_image = "https://images.unsplash.com/photo-1505761671935-60b3a7427bad?auto=format&fit=crop&w=600&q=80"
                        raw_url = city.get('image_url') or placeholder_image
                        image_url = raw_url.replace("'", "%27")
                        st.markdown(f"""
                        <div class="city-card fade-in" style="background-image: url('{image_url}');">
                            <div class="city-overlay">
                                <h4>{city.get('name', 'Sin nombre')}</h4>
                                <div class="city-meta">{city.get('country', 'N/A')} • €{city.get('price', 0)}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.button(
                            "Explorar",
                            key=f"city_{city.get('id', idx)}",
                            use_container_width=True,
                            on_click=navigate_to_city,
                            args=(city.get('id'),)
                        )
        else:
            st.markdown('<div class="empty-state fade-in">📍 No hay ciudades disponibles. Agrega ciudades desde Supabase para comenzar.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-block fade-in">
        <div class="cta-card">
            <strong>💡 Consejo viajero:</strong> Inicia sesión para desbloquear rutas exclusivas, guardar tus favoritos y continuar tu aventura en cualquier dispositivo.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif page == "cities":
    from views import cities_page
    cities_page.show(db, n8n)

elif page == "pois":
    from views import pois_page
    pois_page.show(db, n8n)

elif page == "recommendations":
    from views import recommendations_page
    recommendations_page.show(db, n8n)

elif page == "audio":
    from views import audio_page
    audio_page.show(db, n8n)

elif page == "bookings":
    from views import bookings_page
    bookings_page.show(db, n8n)

elif page == "favorites":
    from views import favorites_page
    favorites_page.show(db, n8n)

elif page == "achievements":
    from views import achievements_page
    achievements_page.show(db, n8n)

elif page == "stats":
    from views import stats_page
    stats_page.show(db, n8n)

elif page == "reports":
    from views import reports_page
    reports_page.show(db, n8n)

elif page == "admin":
    from views import admin_page
    admin_page.show(db, n8n)

# Footer
st.markdown("---")
st.caption("🏛️ Guía Turística Virtual - Powered by n8n, Supabase & OpenAI")
