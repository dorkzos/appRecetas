import streamlit as st
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import os
from auth import AuthManager
from st_tiny_editor import st_editor

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
            color: #000000;
        }
        .info-box pre {
            color: #000000;
            background-color: #ffffff;
            padding: 0.5em;
            border-radius: 0.3em;
            border: 1px solid #ddd;
        }
        /* Mejorar visibilidad de labels */
        label {
            color: #1f1f1f !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        /* Estilos para campos deshabilitados */
        .stTextInput input:disabled,
        .stTextArea textarea:disabled,
        .stDateInput input:disabled {
            background-color: #f0f0f0 !important;
            color: #333333 !important;
            cursor: not-allowed !important;
            font-weight: 500 !important;
        }
        /* Mejorar visibilidad de campos deshabilitados */
        .stTextInput input:disabled::placeholder,
        .stTextArea textarea:disabled::placeholder {
            color: #666666 !important;
        }
    </style>
""", unsafe_allow_html=True)


def formatear_contenido(contenido):
    """
    Formatea el contenido para que Rp. seguido de / en nueva línea
    se convierta en Rp./ en la misma línea.
    """
    # Reemplazar "Rp.\n/" por "Rp./"
    contenido = contenido.replace("Rp.\n/", "Rp./")
    # También manejar el caso con espacios
    contenido = contenido.replace("Rp. \n/", "Rp./")
    contenido = contenido.replace("Rp.\n /", "Rp./")
    contenido = contenido.replace("Rp. \n /", "Rp./")
    
    return contenido


def generar_pdf(nombre, apellido, fecha, diagnostico, tipo_documento, contenido):
    """
    Rellena los campos del formulario PDF existente y los aplana para visualización directa.
    Campos: Date, Paciente, Dx, Texto1
    """
    try:
        # Verificar que el archivo existe
        import os
        if not os.path.exists("modeloReceta.pdf"):
            raise FileNotFoundError("No se encontró el archivo modeloReceta.pdf")
        
        # Leer el PDF modelo
        reader = PdfReader("modeloReceta.pdf")
        writer = PdfWriter()
        
        # Copiar todas las páginas
        for page in reader.pages:
            writer.add_page(page)
        
        # Preparar los datos para rellenar
        nombre_completo = f"{nombre} {apellido}"
        fecha_formateada = fecha.strftime('%d/%m/%Y')
        
        # Formatear el contenido para que Rp.\n/ sea Rp./
        contenido_formateado = formatear_contenido(contenido)
        
        # Rellenar los campos del formulario
        writer.update_page_form_field_values(
            writer.pages[0],
            {
                "Date": fecha_formateada,
                "Paciente": nombre_completo,
                "Dx": diagnostico,
                "Texto1": contenido_formateado
            }
        )
        
        # Aplanar los campos del formulario para que se visualicen directamente
        # sin necesidad de hacer click (PyPDF2 >= 3.0)
        try:
            writer.add_metadata({"/Producer": "Generador de Recetas Médicas"})
            # Usar el método de aplanamiento si está disponible
            for page in writer.pages:
                # Marcar que los campos deben ser visibles siempre
                if "/Annots" in page:
                    annots = page["/Annots"]
                    for annot_ref in annots:
                        annot = annot_ref.get_object()
                        if annot["/Subtype"] == "/Widget":
                            # Hacer visible el campo por defecto
                            if "/F" not in annot:
                                annot["/F"] = 4  # PrintOnly flag para que sea visible
                            else:
                                annot["/F"] = annot["/F"] | 4
        except Exception as e:
            # Si hay error, intentar con el método directo flatten si existe
            pass
        
        # Intentar usar flatten() si está disponible (PyPDF2 >= 3.0)
        try:
            writer.pages[0].flatten(list(writer.pages[0].get_fields().keys()) if hasattr(writer.pages[0], 'get_fields') else None)
        except (AttributeError, TypeError):
            # Si flatten no está disponible o falla, continuar sin aplanar
            # Los campos seguirán siendo rellenados pero interactivos
            pass
        
        # Escribir el PDF en un buffer
        output_buffer = BytesIO()
        writer.write(output_buffer)
        output_buffer.seek(0)
        
        return output_buffer.getvalue()
        
    except FileNotFoundError as e:
        st.error(f"❌ {str(e)}")
        st.error("🔍 Archivos disponibles en el directorio:")
        st.code("\n".join(os.listdir(".")))
        raise
    except Exception as e:
        st.error(f"❌ Error al generar PDF: {str(e)}")
        st.error(f"📁 Directorio actual: {os.getcwd()}")
        raise


# Inicializar el gestor de autenticación
auth_manager = AuthManager()

# Inicializar session state para autenticación
if 'logged_in' not in st.session_state:
    # Permitir saltarse login en modo local/desarrollo
    dev_mode = os.getenv('DEV_MODE', 'false').lower() == 'true'
    
    if dev_mode:
        st.session_state.logged_in = True
        st.session_state.user_data = {
            'nombre': 'Dr.',
            'apellido': 'Desarrollo',
            'username': 'dev_user'
        }
    else:
        st.session_state.logged_in = False
        st.session_state.user_data = None
    
    st.session_state.show_register = False

# Función para mostrar el formulario de login
def show_login_page():
    st.markdown("<div class='main-title'>🔐 Iniciar Sesión</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form(key='login_form'):
            st.markdown("### 👤 Acceso al Sistema")
            
            username = st.text_input("Usuario", key='login_username')
            password = st.text_input("Contraseña", type='password', key='login_password')
            
            login_button = st.form_submit_button("🔓 Iniciar Sesión", use_container_width=True)
            
            if login_button:
                success, user_data, message = auth_manager.login(username, password)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # Información de contacto para solicitar acceso
        st.markdown("---")
        st.info("ℹ️ **¿Necesitas una cuenta?** Contacta al administrador del sistema.")

# Verificar si el usuario está autenticado
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Si llegamos aquí, el usuario está autenticado
# Mostrar información del usuario en la barra lateral
with st.sidebar:
    st.markdown("### 👤 Usuario")
    st.write(f"**{st.session_state.user_data['nombre']} {st.session_state.user_data['apellido']}**")
    st.write(f"Usuario: `{st.session_state.user_data['username']}`")
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.rerun()

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

if 'pdf_generated' not in st.session_state:
    st.session_state.pdf_generated = False

if 'pdf_data' not in st.session_state:
    st.session_state.pdf_data = None

# Formulario principal
with st.form(key='receta_form', clear_on_submit=False):
    
    st.markdown("<div class='section-header'>👤 Información del Paciente</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Paciente", value=st.session_state.form_data['nombre'], key='nombre_input', disabled=st.session_state.pdf_generated)
    with col2:
        apellido = st.text_input("Apellido del Paciente", value=st.session_state.form_data['apellido'], key='apellido_input', disabled=st.session_state.pdf_generated)
    
    col1, col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha", value=st.session_state.form_data['fecha'], key='fecha_input', disabled=st.session_state.pdf_generated)
    with col2:
        diagnostico = st.text_area("Diagnóstico", value=st.session_state.form_data['diagnostico'], height=80, key='diagnostico_input', disabled=st.session_state.pdf_generated)
    
    st.markdown("<div class='section-header'>📝 Tipo de Documento</div>", unsafe_allow_html=True)
    
    tipo_documento = st.radio(
        "Selecciona el tipo de documento:",
        options=['Receta (Rp.)', 'Indicaciones / Notas'],
        index=0 if st.session_state.form_data['tipo_documento'] == 'Receta (Rp.)' else 1,
        key='tipo_documento_input',
        disabled=st.session_state.pdf_generated
    )
    
    st.markdown("<div class='section-header'>📄 Contenido del Documento</div>", unsafe_allow_html=True)
    
    if tipo_documento == 'Receta (Rp.)':
        label_contenido = "Receta (Rp./ Medicamentos, dosis, indicaciones)"
        placeholder_contenido = "Rp./\n\nAspirinas 500mg - 1 tableta cada 8 horas\nIbuprofeno 200mg - 1 tableta cada 6 horas si es necesario\n..."
    else:
        label_contenido = "Indicaciones / Notas Médicas"
        placeholder_contenido = "Escriba aquí las indicaciones preoperatorias, notas médicas o cualquier otra información relevante..."
    
    st.markdown(f"**{label_contenido}**")
    
    # Editor de texto enriquecido con TinyMCE
    contenido = st_editor(
        value=st.session_state.form_data['contenido'],
        height=300,
        use_container_width=True,
        plugins='lists link code',
        toolbar='bold italic underline | bullist numlist | link',
        disabled=st.session_state.pdf_generated
    )
    
    if not contenido:
        contenido = st.session_state.form_data['contenido']
    
    # Botones de acción
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # El botón "Generar" solo se muestra si no hay PDF generado
        if not st.session_state.pdf_generated:
            submit_button = st.form_submit_button("✅ Generar Documento", use_container_width=True)
        else:
            submit_button = False
            st.info("📄 Documento ya generado. Usa 'Limpiar Formulario' para crear uno nuevo.")
    
    with col2:
        clear_button = st.form_submit_button("🔄 Limpiar Formulario", use_container_width=True)

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
        st.session_state.pdf_generated = False
    else:
        try:
            st.success("✅ Documento generado exitosamente.")
            
            # Formatear el contenido antes de generar el PDF
            contenido_formateado = formatear_contenido(contenido)
            
            # Generar PDF
            pdf_buffer = generar_pdf(nombre, apellido, fecha, diagnostico, tipo_documento, contenido)
            
            # Guardar PDF en session state
            st.session_state.pdf_data = pdf_buffer
            st.session_state.pdf_generated = True
            
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
                <pre>{contenido_formateado}</pre>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error al generar el documento: {str(e)}")
            st.session_state.pdf_generated = False

if clear_button:
    st.session_state.form_data = {
        'nombre': '',
        'apellido': '',
        'fecha': datetime.now(),
        'diagnostico': '',
        'tipo_documento': 'Receta (Rp.)',
        'contenido': ''
    }
    st.session_state.pdf_generated = False
    st.session_state.pdf_data = None
    st.rerun()

# Botón de descarga FUERA del formulario - Solución para sandbox de Streamlit Cloud
if st.session_state.pdf_generated and st.session_state.pdf_data:
    try:
        # Verificar que pdf_data tenga contenido
        if isinstance(st.session_state.pdf_data, bytes) and len(st.session_state.pdf_data) > 0:
            # Usar st.download_button - funciona mejor en Streamlit Cloud
            st.markdown("---")
            st.markdown("### 📥 Descarga del Documento")
            
            st.download_button(
                label="📥 Descargar PDF",
                data=st.session_state.pdf_data,
                file_name=f"Receta_{st.session_state.form_data['apellido']}_{st.session_state.form_data['nombre']}_{st.session_state.form_data['fecha'].strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.info(f"✅ PDF listo para descargar ({len(st.session_state.pdf_data)} bytes)\n\n**💡 Nota:** Si el navegador te pide permiso, autoriza la descarga. Si aún así no descargas, intenta con otro navegador.")
        else:
            st.error("❌ El PDF generado está vacío. Por favor, genera el documento nuevamente.")
    except Exception as e:
        st.error(f"❌ Error al preparar la descarga: {str(e)}")
        st.error(f"Tipo de datos: {type(st.session_state.pdf_data)}")
        st.error(f"Tamaño: {len(st.session_state.pdf_data) if isinstance(st.session_state.pdf_data, (bytes, bytearray)) else 'N/A'}")