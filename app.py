import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import os

# Configuración de la página
st.set_page_config(
    page_title="Aplicación de Recetas Médicas",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1f77b4;
            font-size: 2.5em;
            margin-bottom: 1em;
        }
        .section-header {
            color: #1f77b4;
            font-size: 1.3em;
            font-weight: bold;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        .info-box {
            background-color: #f0f2f6;
            padding: 1em;
            border-radius: 0.5em;
            margin-bottom: 1em;
        }
    </style>
""", unsafe_allow_html=True)


def generar_pdf(nombre, apellido, fecha, diagnostico, tipo_documento, contenido):
    """
    Genera un PDF con la información de la receta médica.
    """
    buffer = BytesIO()
    
    # Crear documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        alignment=1  # Centro
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=6,
        spaceBefore=6
    )
    
    # Contenido del documento
    story = []
    
    # Título
    story.append(Paragraph("RECETA MÉDICA", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Información del paciente
    story.append(Paragraph("INFORMACIÓN DEL PACIENTE", heading_style))
    patient_data = [
        ['Nombre:', f"{nombre} {apellido}"],
        ['Fecha:', fecha.strftime('%d/%m/%Y')],
        ['Diagnóstico:', diagnostico]
    ]
    patient_table = Table(patient_data, colWidths=[1.5*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Tipo de documento y contenido
    story.append(Paragraph(f"TIPO: {tipo_documento}", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Contenido formateado
    contenido_formateado = contenido.replace('\n', '<br/>')
    story.append(Paragraph(f"<pre>{contenido_formateado}</pre>", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer.getvalue()


# Título principal
st.markdown("<div class='main-title'>📋 Generador de Recetas Médicas</div>", unsafe_allow_html=True)

# Inicializar session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'nombre': '',
        'apellido': '',
        'fecha': datetime.now(),
        'diagnostico': '',
        'tipo_documento': 'Receta (Rp.)',
        'contenido': ''
    }

# Formulario principal
with st.form(key='receta_form', clear_on_submit=False):
    
    st.markdown("<div class='section-header'>👤 Información del Paciente</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Paciente", value=st.session_state.form_data['nombre'], key='nombre_input')
    with col2:
        apellido = st.text_input("Apellido del Paciente", value=st.session_state.form_data['apellido'], key='apellido_input')
    
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha", value=st.session_state.form_data['fecha'], key='fecha_input')
    with col2:
        diagnostico = st.text_area("Diagnóstico", value=st.session_state.form_data['diagnostico'], height=80, key='diagnostico_input')
    
    st.markdown("<div class='section-header'>📝 Tipo de Documento</div>", unsafe_allow_html=True)
    
    tipo_documento = st.radio(
        "Selecciona el tipo de documento:",
        options=['Receta (Rp.)', 'Indicaciones / Notas'],
        index=0 if st.session_state.form_data['tipo_documento'] == 'Receta (Rp.)' else 1,
        key='tipo_documento_input'
    )
    
    st.markdown("<div class='section-header'>📄 Contenido del Documento</div>", unsafe_allow_html=True)
    
    if tipo_documento == 'Receta (Rp.)':
        label_contenido = "Receta (Rp. / Medicamentos, dosis, indicaciones)"
        placeholder_contenido = "Rp.\n/\nAspirinas 500mg - 1 tableta cada 8 horas\nIbuprofeno 200mg - 1 tableta cada 6 horas si es necesario\n..."
    else:
        label_contenido = "Indicaciones / Notas Médicas"
        placeholder_contenido = "Escriba aquí las indicaciones preoperatorias, notas médicas o cualquier otra información relevante..."
    
    contenido = st.text_area(
        label_contenido,
        value=st.session_state.form_data['contenido'],
        height=250,
        placeholder=placeholder_contenido,
        key='contenido_input'
    )
    
    # Botones de acción
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        submit_button = st.form_submit_button("✅ Generar Documento", use_container_width=True)
    
    with col2:
        clear_button = st.form_submit_button("🔄 Limpiar Formulario", use_container_width=True)
    
    with col3:
        st.form_submit_button("📥 Descargar PDF", use_container_width=True, disabled=True)

# Procesar el formulario
if submit_button:
    # Guardar datos en session state
    st.session_state.form_data = {
        'nombre': nombre,
        'apellido': apellido,
        'fecha': fecha,
        'diagnostico': diagnostico,
        'tipo_documento': tipo_documento,
        'contenido': contenido
    }
    
    # Validar que los campos no estén vacíos
    if not nombre or not apellido or not diagnostico or not contenido:
        st.error("⚠️ Por favor, completa todos los campos antes de generar el documento.")
    else:
        try:
            st.success("✅ Documento generado exitosamente.")
            
            # Generar PDF
            pdf_buffer = generar_pdf(nombre, apellido, fecha, diagnostico, tipo_documento, contenido)
            
            # Mostrar botón de descarga
            st.download_button(
                label="📥 Descargar PDF",
                data=pdf_buffer,
                file_name=f"Receta_{apellido}_{nombre}_{fecha.strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            # Mostrar vista previa del documento
            st.markdown("<div class='section-header'>👁️ Vista Previa del Documento</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-box'>
                <b>Paciente:</b> {nombre} {apellido}<br>
                <b>Fecha:</b> {fecha.strftime('%d/%m/%Y')}<br>
                <b>Diagnóstico:</b> {diagnostico}<br>
                <b>Tipo de Documento:</b> {tipo_documento}<br>
                <hr>
                <b>Contenido:</b><br>
                <pre>{contenido}</pre>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error al generar el documento: {str(e)}")

if clear_button:
    st.session_state.form_data = {
        'nombre': '',
        'apellido': '',
        'fecha': datetime.now(),
        'diagnostico': '',
        'tipo_documento': 'Receta (Rp.)',
        'contenido': ''
    }
    st.rerun()
