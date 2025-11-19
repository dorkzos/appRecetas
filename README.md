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

## 👤 Configuración de Usuarios

Los usuarios se configuran directamente en **Streamlit Cloud → Settings → Secrets**.

Ver guía completa en: [`COMO_AGREGAR_USUARIOS.md`](COMO_AGREGAR_USUARIOS.md)

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
├── generar_hash.py           # Generador de hashes para contraseñas
├── requirements.txt          # Dependencias
├── .gitignore               # Archivos ignorados por Git
├── COMO_AGREGAR_USUARIOS.md # Guía para agregar usuarios
└── README.md                # Este archivo
```

## 🔒 Seguridad

- Las contraseñas se hashean con SHA-256
- El archivo `users.json` no se sube a GitHub
- Nunca se almacenan contraseñas en texto plano

## 🌐 Deploy en Streamlit Cloud

### 1. Push a GitHub
```bash
git push
```

### 2. Deploy en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io/)
2. Conecta tu repositorio `dorkzos/appRecetas`
3. Selecciona `app.py` como archivo principal
4. Click en **Deploy**

### 3. Configurar Usuarios (IMPORTANTE)

Una vez deployado, ve a **Settings → Secrets** y agrega tus usuarios:

```toml
[users.admin]
password = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
nombre = "Administrador"
apellido = "Sistema"

[users.tu_usuario]
password = "TU_HASH_AQUI"
nombre = "Tu Nombre"
apellido = "Tu Apellido"
```

### 4. Generar Hash de Contraseña

```bash
python generar_hash.py
```

O manualmente:
```bash
python -c "import hashlib; print(hashlib.sha256('tu_contraseña'.encode()).hexdigest())"
```

🔒 **Seguridad:** Los usuarios están SOLO en Streamlit Secrets, NO en GitHub.

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
