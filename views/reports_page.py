"""
Página de Generación de Reportes
"""
import io
import os
import tempfile
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from fpdf import FPDF

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
            generate_preview(
                db,
                report_type,
                start_date,
                end_date,
                include_charts,
                include_tables,
                include_summary,
                include_recommendations
            )
    
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


def generate_preview(
    db,
    report_type,
    start_date,
    end_date,
    include_charts,
    include_tables,
    include_summary,
    include_recommendations
):
    """Genera una vista previa del reporte"""
    
    with st.spinner("Generando vista previa..."):
        content = get_report_content(report_type, db, start_date, end_date)
        st.success("Vista previa generada")
        
        with st.expander("📄 Vista Previa del Reporte", expanded=True):
            st.markdown(f"## {report_type}")
            st.markdown(f"**Período:** {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
            st.markdown(f"**Generado:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            st.markdown("---")
            render_report_preview(
                content,
                include_charts=include_charts,
                include_tables=include_tables,
                include_summary=include_summary,
                include_recommendations=include_recommendations
            )


def get_report_content(report_type, db, start_date, end_date):
    """Construye la información necesaria para cada tipo de reporte"""
    
    weeks = []
    for i in range(5, -1, -1):
        week_end = end_date - timedelta(days=7 * i)
        week_start = week_end - timedelta(days=6)
        weeks.append(f"{week_start.strftime('%d/%m')} - {week_end.strftime('%d/%m')}")
    
    if "Resumen General" in report_type:
        visits_weekly = [315, 338, 349, 362, 389, 420]
        bookings_weekly = [102, 108, 112, 121, 134, 148]
        
        summary_points = [
            "Crecimiento sostenido de visitas en las últimas tres semanas consecutivas.",
            "El 58 % de las reservas confirmadas proviene del canal móvil.",
            "La valoración media de la experiencia se mantiene en 4,7 sobre 5."
        ]
        
        detail_items = [
            "Reservas confirmadas en el período: 765",
            "Ticket promedio: € 38,20",
            "Tiempo medio de permanencia: 47 minutos"
        ]
        
        table_df = pd.DataFrame({
            "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"],
            "Visitas": [482, 451, 338, 295, 210],
            "Reservas": [212, 198, 156, 138, 95],
            "Valoración": [4.8, 4.7, 4.6, 4.5, 4.4]
        })
        
        recommendations = [
            "Refuerza las campañas de retargeting en Barcelona y Valencia.",
            "Prioriza experiencias combinadas para aumentar el ticket promedio.",
            "Potencia el programa de referidos para mantener el ritmo de nuevos usuarios."
        ]
        
        return {
            "summary_points": summary_points,
            "detail_items": detail_items,
            "metrics": [
                {"label": "Total de visitas", "value": f"{sum(visits_weekly):,}".replace(",", "."), "delta": "+6,8 %"},
                {"label": "Usuarios activos", "value": "3.482", "delta": "+4,3 %"},
                {"label": "Ingresos", "value": "€ 52.940", "delta": "+9,1 %"}
            ],
            "chart": {
                "title": "Evolución semanal de visitas y reservas",
                "data": pd.DataFrame({
                    "Periodo": weeks,
                    "Visitas": visits_weekly,
                    "Reservas": bookings_weekly
                }),
                "kind": "line"
            },
            "table": {
                "title": "Desempeño por ciudad",
                "data": table_df
            },
            "recommendations": recommendations
        }
    
    if "Usuario" in report_type:
        user_id = getattr(st.session_state, "user_id", None)
        user_email = getattr(st.session_state, "user_email", "")
        user_data = getattr(st.session_state, "user_data", {}) or {}
        
        visits = db.get_user_visits(user_id) if user_id and hasattr(db, "get_user_visits") else []
        bookings = db.get_user_bookings(user_id) if user_id and hasattr(db, "get_user_bookings") else []
        achievements = db.get_user_achievements(user_id) if user_id and hasattr(db, "get_user_achievements") else []
        
        confirmed_bookings = [b for b in bookings if isinstance(b, dict) and b.get("status") == "confirmed"]
        points = user_data.get("total_points", 0)
        
        base_activity = [2, 3, 4, 5, 6, 7]
        base_reservations = [1, 1, 2, 2, 3, 3]
        factor_visits = max(1, len(visits) // 3 + 1)
        factor_bookings = max(1, len(bookings) // 2 + 1)
        
        chart_df = pd.DataFrame({
            "Periodo": weeks,
            "Interacciones": [value * factor_visits for value in base_activity],
            "Reservas": [value * factor_bookings for value in base_reservations]
        })
        
        base_visits_distribution = [7, 6, 5, 4]
        scale_visits = max(len(visits), 8) / 8 if len(visits) else 1
        visits_by_category = [max(int(round(value * scale_visits)), 0) for value in base_visits_distribution]
        
        base_reservations_distribution = [5, 4, 3, 2]
        scale_reservations = max(len(bookings), 6) / 6 if len(bookings) else 1
        reservations_by_category = [max(int(round(value * scale_reservations)), 0) for value in base_reservations_distribution]
        
        table_df = pd.DataFrame({
            "Categoría": ["Cultura", "Gastronomía", "Naturaleza", "Aventura"],
            "Visitas": visits_by_category,
            "Reservas": reservations_by_category,
            "Valoración": [4.8, 4.6, 4.7, 4.5]
        })
        
        last_visit = None
        if visits:
            last_visit = visits[-1]
        
        summary_points = [
            f"Total de visitas completadas en el período: {len(visits)}.",
            f"Reservas confirmadas: {len(confirmed_bookings)}.",
            f"Puntos acumulados disponibles: {points}."
        ]
        
        if last_visit and isinstance(last_visit, dict):
            poi_name = last_visit.get("name") or last_visit.get("poi_name") or "Visita reciente"
            visit_date = last_visit.get("date") or last_visit.get("visited_at")
            if isinstance(visit_date, datetime):
                visit_date = visit_date.strftime("%d/%m/%Y")
            summary_points.append(f"Última visita registrada: {poi_name} ({visit_date}).")
        
        detail_items = [
            f"Correo asociado: {user_email or 'no disponible'}",
            f"Logros desbloqueados: {len(achievements)}",
            f"Reservas pendientes: {len(bookings) - len(confirmed_bookings)}"
        ]
        
        recommendations = [
            "Activa recordatorios automáticos para no perder nuevas experiencias.",
            "Explora rutas combinadas para incrementar los puntos de fidelidad.",
            "Comparte reseñas para mejorar la personalización de futuras sugerencias."
        ]
        
        return {
            "summary_points": summary_points,
            "detail_items": detail_items,
            "metrics": [
                {"label": "Lugares visitados", "value": str(len(visits)), "delta": "+2 en el último mes"},
                {"label": "Reservas confirmadas", "value": str(len(confirmed_bookings)), "delta": "+1 respecto al período previo"},
                {"label": "Logros obtenidos", "value": str(len(achievements)), "delta": "+1 nueva insignia"}
            ],
            "chart": {
                "title": "Actividad semanal del usuario",
                "data": chart_df,
                "kind": "line"
            },
            "table": {
                "title": "Participación por categoría",
                "data": table_df
            },
            "recommendations": recommendations
        }
    
    if "Popularidad" in report_type:
        pois = db.get_pois() if hasattr(db, "get_pois") else []
        pois = pois[:5] if pois else [
            {"name": "Museo de Arte Moderno", "rating": 4.8, "total_visits": 512, "bookings": 210},
            {"name": "Ruta Gastronómica Centro", "rating": 4.7, "total_visits": 476, "bookings": 198},
            {"name": "Mirador Panorámico", "rating": 4.6, "total_visits": 432, "bookings": 180},
            {"name": "Tour Histórico Colonial", "rating": 4.5, "total_visits": 398, "bookings": 162},
            {"name": "Circuito Natural Río Verde", "rating": 4.4, "total_visits": 365, "bookings": 149}
        ]
        
        table_df = pd.DataFrame([{
            "Lugar": poi.get("name", "Sin nombre"),
            "Visitas": poi.get("total_visits", 0),
            "Reservas": poi.get("bookings", poi.get("reservations", 0)),
            "Valoración": round(poi.get("rating", 0), 2)
        } for poi in pois])
        
        chart_df = pd.DataFrame({
            "Lugar": table_df["Lugar"].tolist(),
            "Visitas": table_df["Visitas"].tolist()
        })
        
        summary_points = [
            f"{table_df.iloc[0]['Lugar']} lidera con {int(table_df.iloc[0]['Visitas'])} visitas en el período.",
            "Las experiencias gastronómicas representan el 26 % de las reservas.",
            "El índice de satisfacción promedio supera el 4,6 en los principales atractivos."
        ]
        
        detail_items = [
            f"Valoración media del top 5: {table_df['Valoración'].mean():.2f}",
            f"Reservas promedio por atractivo: {table_df['Reservas'].mean():.0f}",
            "Tres de los cinco lugares destacados renovaron oferta de audio-guías."
        ]
        
        recommendations = [
            "Refuerza la disponibilidad de plazas en horarios pico para los tres primeros atractivos.",
            "Incorpora testimonios destacados en las fichas de los lugares con mejor valoración.",
            "Lanza campañas cruzadas entre los lugares culturales y gastronómicos."
        ]
        
        return {
            "summary_points": summary_points,
            "detail_items": detail_items,
            "metrics": [
                {"label": "Visitas promedio/día", "value": "152", "delta": "+7 %"},
                {"label": "Reservas convertidas", "value": "899", "delta": "+5 %"},
                {"label": "Valoración media", "value": "4,6", "delta": "+0,1"}
            ],
            "chart": {
                "title": "Visitas por atractivo destacado",
                "data": chart_df,
                "kind": "bar"
            },
            "table": {
                "title": "Top 5 atractivos",
                "data": table_df
            },
            "recommendations": recommendations
        }
    
    if "Financiero" in report_type:
        revenue_series = [18250, 19120, 19840, 20560, 21430, 22490]
        bookings_series = [365, 378, 392, 404, 417, 436]
        
        summary_points = [
            "Los ingresos crecieron un 7,4 % respecto al mismo período anterior.",
            "Las reservas anticipadas representan el 42 % de la facturación total.",
            "El margen promedio se mantiene en 34,5 %."
        ]
        
        detail_items = [
            "Ticket medio consolidado: € 51,60",
            "Cancelaciones reembolsadas: 3,2 %",
            "Ingresos por audio-guías premium: € 6.780"
        ]
        
        table_df = pd.DataFrame({
            "Canal": ["App móvil", "Web", "Agencias", "Empresarial"],
            "Ingresos": ["€ 21.480", "€ 18.960", "€ 8.740", "€ 3.310"],
            "Reservas": [436, 389, 162, 74],
            "Conversión": ["4,9 %", "3,8 %", "2,4 %", "1,9 %"]
        })
        
        recommendations = [
            "Optimiza las campañas de performance en la app para sostener el crecimiento.",
            "Revisa acuerdos con agencias para mejorar el margen por reserva.",
            "Introduce ofertas escalonadas para incrementar el ticket medio en web."
        ]
        
        return {
            "summary_points": summary_points,
            "detail_items": detail_items,
            "metrics": [
                {"label": "Ingresos totales", "value": "€ 124.690", "delta": "+7,4 %"},
                {"label": "Reservas pagadas", "value": "2.092", "delta": "+5,2 %"},
                {"label": "Ticket promedio", "value": "€ 51,60", "delta": "+3,1 %"}
            ],
            "chart": {
                "title": "Ingresos y reservas por semana",
                "data": pd.DataFrame({
                    "Periodo": weeks,
                    "Ingresos": revenue_series,
                    "Reservas": bookings_series
                }),
                "kind": "line"
            },
            "table": {
                "title": "Desempeño por canal de venta",
                "data": table_df
            },
            "recommendations": recommendations
        }
    
    # Tendencias y estadísticas
    new_users_series = [420, 438, 452, 469, 498, 522]
    returning_users_series = [612, 625, 637, 648, 666, 689]
    
    summary_points = [
        "Los usuarios nuevos crecieron 9,5 % en las últimas seis semanas.",
        "La retención a 30 días se consolida en 68 %.",
        "Las interacciones con contenidos dinámicos aumentaron 14 %."
    ]
    
    detail_items = [
        "Tiempo medio de sesión: 12 minutos",
        "Usuarios activos diarios: 3.820",
        "Tasa de conversión orgánica: 3,4 %"
    ]
    
    table_df = pd.DataFrame({
        "Indicador": ["Usuarios nuevos", "Usuarios recurrentes", "Sesiones", "Audio-guías generadas"],
        "Últimos 30 días": [5120, 6890, 18230, 2980],
        "Anterior": [4680, 6520, 17120, 2650],
        "Variación": ["+9,4 %", "+5,7 %", "+6,5 %", "+12,5 %"]
    })
    
    recommendations = [
        "Prioriza el onboarding interactivo para mantener la tasa de activación.",
        "Refuerza las notificaciones segmentadas con base en intereses recientes.",
        "Aumenta el catálogo de experiencias con audio en vivo los fines de semana."
    ]
    
    return {
        "summary_points": summary_points,
        "detail_items": detail_items,
        "metrics": [
            {"label": "Usuarios nuevos", "value": "5.120", "delta": "+9,4 %"},
            {"label": "Usuarios activos", "value": "8.710", "delta": "+6,1 %"},
            {"label": "Retención 30 días", "value": "68 %", "delta": "+1,2 p.p."}
        ],
        "chart": {
            "title": "Evolución de usuarios nuevos y recurrentes",
            "data": pd.DataFrame({
                "Periodo": weeks,
                "Usuarios nuevos": new_users_series,
                "Usuarios recurrentes": returning_users_series
            }),
            "kind": "line"
        },
        "table": {
            "title": "Indicadores clave del período",
            "data": table_df
        },
        "recommendations": recommendations
    }


def render_report_preview(content, include_charts, include_tables, include_summary, include_recommendations):
    """Renderiza la vista previa utilizando la configuración seleccionada"""
    
    metrics = content.get("metrics", [])
    if metrics:
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            delta = metric.get("delta")
            description = metric.get("description")
            if delta:
                col.metric(metric["label"], metric["value"], delta)
            elif description:
                col.metric(metric["label"], metric["value"], description)
            else:
                col.metric(metric["label"], metric["value"])
    
    detail_items = content.get("detail_items", [])
    if detail_items:
        st.markdown("### 📋 Detalles Clave")
        for item in detail_items:
            st.write(f"- {item}")
    
    if include_summary:
        summary_points = content.get("summary_points", [])
        if summary_points:
            st.markdown("### 📝 Resumen Ejecutivo")
            for point in summary_points:
                st.write(f"- {point}")
    
    if include_charts:
        chart_info = content.get("chart")
        if chart_info and isinstance(chart_info, dict):
            chart_df = chart_info.get("data")
            if isinstance(chart_df, pd.DataFrame) and not chart_df.empty:
                st.markdown(f"### {chart_info.get('title', 'Visualización')}")
                df_to_plot = chart_df.set_index(chart_df.columns[0])
                kind = chart_info.get("kind", "line")
                if kind == "bar":
                    st.bar_chart(df_to_plot)
                elif kind == "area":
                    st.area_chart(df_to_plot)
                else:
                    st.line_chart(df_to_plot)
    
    if include_tables:
        table_info = content.get("table")
        if table_info and isinstance(table_info, dict):
            table_df = table_info.get("data")
            if isinstance(table_df, pd.DataFrame) and not table_df.empty:
                st.markdown(f"### {table_info.get('title', 'Tabla de detalle')}")
                st.dataframe(table_df, use_container_width=True, hide_index=True)
    
    if include_recommendations:
        recommendations = content.get("recommendations", [])
        if recommendations:
            st.markdown("### 💡 Recomendaciones")
            for rec in recommendations:
                st.write(f"- {rec}")


def generate_pdf_report(db, n8n, report_type, start_date, end_date, 
                       include_charts, include_tables, include_summary, include_recommendations):
    """Genera el reporte en formato PDF"""
    
    with st.spinner("📄 Generando reporte PDF..."):
        content = get_report_content(report_type, db, start_date, end_date)
        
        pdf = PDFReport()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        
        pdf.set_text_color(33, 33, 33)
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 12, safe_pdf_text("Guía Turística Virtual"), 0, 1, 'C')
        pdf.ln(2)
        
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(55, 71, 79)
        pdf.cell(0, 10, safe_pdf_text(report_type), 0, 1, 'C')
        pdf.ln(4)
        
        pdf.set_text_color(97, 97, 97)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, safe_pdf_text(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"), 0, 1)
        pdf.cell(0, 6, safe_pdf_text(f"Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"), 0, 1)
        pdf.ln(8)
        
        metrics = content.get("metrics", [])
        if metrics:
            add_pdf_section_header(pdf, "Indicadores principales", (25, 118, 210))
            add_pdf_metrics(pdf, metrics)
        
        detail_items = content.get("detail_items", [])
        if detail_items:
            add_pdf_section_header(pdf, "Detalles clave", (84, 110, 122))
            add_pdf_bullet_list(pdf, detail_items)
        
        if include_summary:
            summary_points = content.get("summary_points", [])
            if summary_points:
                add_pdf_section_header(pdf, "Resumen ejecutivo", (30, 136, 229))
                add_pdf_bullet_list(pdf, summary_points)
        
        chart_info = content.get("chart")
        if include_charts and chart_info:
            add_pdf_chart(
                pdf,
                chart_info.get("title", "Visualización"),
                chart_info.get("data"),
                chart_info.get("kind", "line")
            )
        
        table_info = content.get("table")
        if include_tables and table_info:
            add_pdf_table(
                pdf,
                table_info.get("title", "Tabla de detalle"),
                table_info.get("data")
            )
        
        if include_recommendations:
            recommendations = content.get("recommendations", [])
            if recommendations:
                add_pdf_section_header(pdf, "Recomendaciones", (56, 142, 60))
                add_pdf_bullet_list(pdf, recommendations)
        
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


def safe_pdf_text(value):
    """Asegura compatibilidad de caracteres con el PDF."""
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    return value.encode('latin-1', 'replace').decode('latin-1')


def add_pdf_section_header(pdf, title, fill_color):
    """Agrega un encabezado de sección con fondo de color."""
    pdf.set_fill_color(*fill_color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 9, safe_pdf_text(title), 0, 1, 'L', True)
    pdf.ln(2)
    pdf.set_text_color(33, 33, 33)


def add_pdf_metrics(pdf, metrics):
    """Dibuja una grilla de métricas destacadas."""
    if not metrics:
        return
    
    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    max_cols = 3
    rows = [metrics[i:i + max_cols] for i in range(0, len(metrics), max_cols)]
    
    for row in rows:
        col_width = usable_width / len(row)
        
        pdf.set_fill_color(240, 244, 252)
        pdf.set_font("Arial", 'B', 10)
        for metric in row:
            pdf.cell(col_width, 8, safe_pdf_text(metric.get("label", "")), border=1, align='L', fill=True)
        pdf.ln()
        
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(33, 33, 33)
        for metric in row:
            pdf.cell(col_width, 10, safe_pdf_text(metric.get("value", "")), border=1, align='L')
        pdf.ln()
        
        pdf.set_font("Arial", '', 9)
        for metric in row:
            delta = metric.get("delta") or metric.get("description") or ""
            if delta:
                if isinstance(delta, str) and delta.strip().startswith("-"):
                    pdf.set_text_color(198, 40, 40)
                else:
                    pdf.set_text_color(46, 125, 50)
            else:
                pdf.set_text_color(120, 120, 120)
            pdf.cell(col_width, 8, safe_pdf_text(delta), border=1, align='L')
        pdf.ln(10)
        pdf.set_text_color(33, 33, 33)


def add_pdf_bullet_list(pdf, items):
    """Agrega una lista con viñetas."""
    if not items:
        return
    
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(55, 71, 79)
    for item in items:
        pdf.multi_cell(0, 6, safe_pdf_text(f"• {item}"))
    pdf.ln(4)
    pdf.set_text_color(33, 33, 33)


def add_pdf_table(pdf, title, dataframe):
    """Renderiza una tabla en el PDF."""
    if not isinstance(dataframe, pd.DataFrame) or dataframe.empty:
        return
    
    add_pdf_section_header(pdf, title, (39, 76, 119))
    
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(33, 33, 33)
    
    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    column_count = len(dataframe.columns)
    col_width = usable_width / column_count
    
    pdf.set_fill_color(224, 235, 255)
    for column in dataframe.columns:
        pdf.cell(col_width, 8, safe_pdf_text(column), border=1, align='C', fill=True)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(255, 255, 255)
    
    for _, row in dataframe.iterrows():
        for value in row:
            pdf.cell(col_width, 8, safe_pdf_text(value), border=1, align='C')
        pdf.ln()
    
    pdf.ln(6)


def add_pdf_chart(pdf, title, dataframe, kind):
    """Agrega una visualización como imagen al PDF."""
    if not isinstance(dataframe, pd.DataFrame) or dataframe.empty:
        return
    
    add_pdf_section_header(pdf, title, (38, 166, 154))
    
    fig, ax = plt.subplots(figsize=(6, 3))
    x_values = dataframe.iloc[:, 0]
    
    if kind == "bar":
        values = dataframe.iloc[:, 1]
        ax.bar(x_values, values, color="#1e88e5")
        ax.set_ylim(0, max(values) * 1.2 if len(values) else 1)
    else:
        for column in dataframe.columns[1:]:
            ax.plot(x_values, dataframe[column], marker='o', linewidth=2, label=column)
        if len(dataframe.columns) > 2:
            ax.legend(loc='upper left')
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.xticks(rotation=35, ha='right')
    fig.tight_layout()
    
    temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_path = temp_image.name
    temp_image.close()
    
    fig.savefig(temp_path, dpi=220, bbox_inches='tight')
    plt.close(fig)
    
    pdf.image(temp_path, w=pdf.w - pdf.l_margin - pdf.r_margin)
    os.unlink(temp_path)
    pdf.ln(6)

class PDFReport(FPDF):
    """Clase personalizada para generar reportes PDF"""
    
    def header(self):
        """Encabezado del PDF"""
        self.set_fill_color(25, 118, 210)
        self.rect(0, 0, self.w, 18, 'F')
        self.set_y(6)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, safe_pdf_text('Guía Turística Virtual - Reporte'), 0, 1, 'C')
        self.ln(4)
        self.set_text_color(33, 33, 33)
    
    def footer(self):
        """Pie de página del PDF"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, safe_pdf_text(f'Página {self.page_no()}'), 0, 0, 'C')
