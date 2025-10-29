"""
Página de Generación de Reportes
"""
import streamlit as st
from datetime import datetime, timedelta
from fpdf import FPDF
import io

def show(db, n8n):
    """Muestra la página de reportes"""
    
    st.title("📄 Generador de Reportes")
    st.markdown("Genera reportes personalizados en formato PDF")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_report_config(db, n8n)
    
    with col2:
        show_report_preview(db)


def show_report_config(db, n8n):
    """Muestra la configuración del reporte"""
    
    st.subheader("⚙️ Configuración del Reporte")
    
    # Tipo de reporte
    report_type = st.selectbox(
        "Tipo de Reporte",
        [
            "📊 Resumen General",
            "👤 Actividad de Usuario",
            "🏆 Análisis de Popularidad",
            "💰 Reporte Financiero",
            "📈 Tendencias y Estadísticas"
        ]
    )
    
    # Rango de fechas
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Fecha de inicio",
            value=datetime.now().date() - timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "Fecha de fin",
            value=datetime.now().date()
        )
    
    # Opciones adicionales
    st.markdown("### 📋 Opciones de Contenido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_charts = st.checkbox("Incluir gráficos", value=True)
        include_tables = st.checkbox("Incluir tablas detalladas", value=True)
    
    with col2:
        include_summary = st.checkbox("Incluir resumen ejecutivo", value=True)
        include_recommendations = st.checkbox("Incluir recomendaciones", value=True)
    
    # Filtros específicos según el tipo de reporte
    if "Usuario" in report_type:
        if st.session_state.user_id:
            st.info(f"📧 Generando reporte para: {st.session_state.user_email}")
        else:
            st.warning("⚠️ Debes iniciar sesión para generar reportes de usuario")
            return
    
    # Botones de acción
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👁️ Vista Previa", type="secondary", use_container_width=True):
            generate_preview(db, report_type, start_date, end_date)
    
    with col2:
        if st.button("📥 Generar PDF", type="primary", use_container_width=True):
            generate_pdf_report(
                db, n8n, report_type, start_date, end_date,
                include_charts, include_tables, include_summary, include_recommendations
            )


def show_report_preview(db):
    """Muestra una vista previa del reporte"""
    
    st.subheader("👁️ Vista Previa")
    
    st.info("Configura el reporte y haz clic en 'Vista Previa' para ver el contenido")
    
    # Placeholder para la vista previa
    with st.container():
        st.markdown("""
        ### 📊 Ejemplo de Reporte
        
        **Período:** 01/01/2024 - 31/01/2024
        
        #### Resumen Ejecutivo
        - Total de visitas: 1,247
        - Usuarios activos: 892
        - Reservas realizadas: 423
        - Ingresos totales: €15,247
        
        #### Métricas Principales
        - Tasa de conversión: 34%
        - Satisfacción promedio: 4.7/5.0
        - Tiempo promedio de visita: 45 min
        """)


def generate_preview(db, report_type, start_date, end_date):
    """Genera una vista previa del reporte"""
    
    with st.spinner("Generando vista previa..."):
        st.success("Vista previa generada")
        
        # Contenedor para la vista previa
        with st.expander("📄 Vista Previa del Reporte", expanded=True):
            st.markdown(f"## {report_type}")
            st.markdown(f"**Período:** {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
            st.markdown(f"**Generado:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            st.markdown("---")
            
            # Contenido según el tipo de reporte
            if "Resumen General" in report_type:
                show_general_summary(db, start_date, end_date)
            elif "Usuario" in report_type:
                show_user_activity_summary(db, start_date, end_date)
            elif "Popularidad" in report_type:
                show_popularity_summary(db, start_date, end_date)
            elif "Financiero" in report_type:
                show_financial_summary(db, start_date, end_date)
            else:
                show_trends_summary(db, start_date, end_date)


def show_general_summary(db, start_date, end_date):
    """Muestra resumen general"""
    
    st.subheader("📊 Resumen Ejecutivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Visitas", "1,247", "+12.5%")
    with col2:
        st.metric("Usuarios Activos", "892", "+8.3%")
    with col3:
        st.metric("Ingresos", "€15,247", "+18.7%")
    
    st.markdown("### 📈 Métricas Clave")
    
    metrics_data = {
        "Métrica": ["Tasa de Conversión", "Satisfacción Promedio", "Tiempo Promedio", "Reservas Completadas"],
        "Valor": ["34%", "4.7/5.0", "45 min", "423"],
        "Cambio": ["+5%", "+0.2", "+3 min", "+15%"]
    }
    
    st.table(metrics_data)


def show_user_activity_summary(db, start_date, end_date):
    """Muestra resumen de actividad de usuario"""
    
    if not st.session_state.user_id:
        st.warning("Debes iniciar sesión")
        return
    
    st.subheader("👤 Actividad del Usuario")
    
    visits = db.get_user_visits(st.session_state.user_id)
    bookings = db.get_user_bookings(st.session_state.user_id)
    achievements = db.get_user_achievements(st.session_state.user_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Lugares Visitados", len(visits))
    with col2:
        st.metric("Reservas", len(bookings))
    with col3:
        st.metric("Logros", len(achievements))
    
    st.markdown("### 📋 Detalle de Actividades")
    
    st.write(f"- Total de visitas realizadas: {len(visits)}")
    st.write(f"- Total de reservas: {len(bookings)}")
    st.write(f"- Puntos acumulados: {st.session_state.user_data.get('total_points', 0)}")


def show_popularity_summary(db, start_date, end_date):
    """Muestra resumen de popularidad"""
    
    st.subheader("🏆 Lugares Más Populares")
    
    pois = db.get_pois()[:5]
    
    for i, poi in enumerate(pois, 1):
        st.write(f"{i}. **{poi['name']}** - ⭐ {poi.get('rating', 0):.1f}")


def show_financial_summary(db, start_date, end_date):
    """Muestra resumen financiero"""
    
    st.subheader("💰 Resumen Financiero")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Ingresos Totales", "€15,247")
    with col2:
        st.metric("Reservas Pagadas", "423")
    with col3:
        st.metric("Ticket Promedio", "€36.05")


def show_trends_summary(db, start_date, end_date):
    """Muestra resumen de tendencias"""
    
    st.subheader("📈 Tendencias")
    
    st.write("- Crecimiento mensual: +12.5%")
    st.write("- Nuevos usuarios: +8.3%")
    st.write("- Tasa de retención: 67%")


def generate_pdf_report(db, n8n, report_type, start_date, end_date, 
                       include_charts, include_tables, include_summary, include_recommendations):
    """Genera el reporte en formato PDF"""
    
    with st.spinner("📄 Generando reporte PDF..."):
        # Crear PDF
        pdf = PDFReport()
        pdf.add_page()
        
        # Título
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, 'Guia Turistica Virtual', 0, 1, 'C')
        pdf.ln(5)
        
        # Tipo de reporte
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, report_type.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
        pdf.ln(5)
        
        # Información del reporte
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.cell(0, 10, f"Periodo: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}", 0, 1)
        pdf.ln(10)
        
        # Resumen ejecutivo
        if include_summary:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Resumen Ejecutivo", 0, 1)
            pdf.set_font("Arial", size=12)
            
            summary_items = [
                "Total de Visitas: 1,247",
                "Usuarios Activos: 892",
                "Audio-guias Generadas: 856",
                "Reservas Realizadas: 423",
                "Ingresos Totales: EUR 15,247"
            ]
            
            for item in summary_items:
                pdf.cell(0, 10, item, 0, 1)
            
            pdf.ln(10)
        
        # Métricas principales
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Metricas Principales", 0, 1)
        pdf.set_font("Arial", size=12)
        
        metrics = [
            "Tasa de Conversion: 34%",
            "Satisfaccion Promedio: 4.7/5.0",
            "Tiempo Promedio de Visita: 45 minutos",
            "Tasa de Retencion: 67%"
        ]
        
        for metric in metrics:
            pdf.cell(0, 10, metric, 0, 1)
        
        pdf.ln(10)
        
        # Recomendaciones
        if include_recommendations:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "Recomendaciones", 0, 1)
            pdf.set_font("Arial", size=12)
            
            recommendations = [
                "1. Incrementar la promocion de audio-guias",
                "2. Mejorar la experiencia de reservas",
                "3. Expandir el catalogo de ciudades",
                "4. Implementar programa de fidelizacion"
            ]
            
            for rec in recommendations:
                pdf.cell(0, 10, rec, 0, 1)
        
        # Generar el PDF
        pdf_output = io.BytesIO()
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_output.write(pdf_bytes)
        pdf_output.seek(0)
        
        # Botón de descarga
        st.success("✅ Reporte generado exitosamente!")
        
        st.download_button(
            label="📥 Descargar Reporte PDF",
            data=pdf_output,
            file_name=f"reporte_turismo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
        st.balloons()


class PDFReport(FPDF):
    """Clase personalizada para generar reportes PDF"""
    
    def header(self):
        """Encabezado del PDF"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Guia Turistica Virtual - Reporte', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Pie de página del PDF"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')
