# 🏥 Aplicación de Recetas Médicas

Aplicación web desarrollada con Streamlit para generar recetas médicas profesionales en formato PDF.

## 🚀 Características

- 🔐 **Sistema de autenticación** - Login y registro de usuarios
- 📋 **Formularios intuitivos** - Captura fácil de información del paciente
- 📄 **PDF profesional** - Rellena automáticamente un modelo de receta
- 👁️ **Vista previa** - Revisa antes de descargar
- 💾 **Descarga directa** - PDF listo para imprimir
- 🎨 **Interfaz moderna** - Diseño limpio y responsive

## 📦 Instalación Local

### Requisitos previos
- Python 3.8 o superior
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/dorkzos/appRecetas.git
cd appRecetas
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

6. **Abrir en el navegador**
   - La app se abrirá automáticamente en `http://localhost:8501`

## 👤 Primer Uso

### Crear usuario de prueba

```bash
python crear_usuario_prueba.py
```

Esto creará un usuario con las siguientes credenciales:
- **Usuario:** admin
- **Contraseña:** admin123

⚠️ **Importante:** Cambia estas credenciales en producción.

### Crear tu propio usuario

También puedes crear una cuenta directamente desde la aplicación usando el botón "📝 Crear Cuenta".

## 🛠️ Tecnologías

- **[Streamlit](https://streamlit.io/)** - Framework web para Python
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - Manipulación de PDFs
- **Python 3.13** - Lenguaje de programación

## 📁 Estructura del Proyecto

```
appRecetas/
├── app.py                    # Aplicación principal
├── auth.py                   # Sistema de autenticación
├── modeloReceta.pdf          # Plantilla PDF de receta
├── crear_usuario_prueba.py   # Script para crear usuario de prueba
├── leer_campos_pdf.py        # Utilidad para inspeccionar campos PDF
├── test_rellenar_pdf.py      # Test de relleno de PDF
├── requirements.txt          # Dependencias
├── .gitignore               # Archivos ignorados por Git
└── README.md                # Este archivo
```

## 🔒 Seguridad

- Las contraseñas se hashean con SHA-256
- El archivo `users.json` no se sube a GitHub
- Nunca se almacenan contraseñas en texto plano

## 🌐 Deploy en Streamlit Cloud

1. **Fork o push** este repositorio a tu GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io/)
3. Conecta tu repositorio
4. Selecciona `app.py` como archivo principal
5. Deploy automático

⚠️ **Nota:** Después del deploy, deberás crear usuarios desde la interfaz de registro.

## 📝 Uso

1. **Iniciar sesión** o crear una cuenta
2. **Completar el formulario** con los datos del paciente
3. **Escribir la receta** o indicaciones médicas (formato: `Rp./`)
4. **Generar documento** para ver la vista previa
5. **Descargar PDF** con el botón de descarga

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Proyecto personal de uso médico.

## 👨‍💻 Autor

**Dorian** - [dorkzos](https://github.com/dorkzos)

## 🆘 Soporte

Si encuentras algún problema, por favor abre un [issue](https://github.com/dorkzos/appRecetas/issues).

---

⭐ Si te ha sido útil, ¡no olvides dar una estrella al proyecto!
