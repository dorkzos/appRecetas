# Aplicación de Recetas Médicas con Streamlit

Una aplicación web simple y eficiente para generar recetas médicas y documentos de indicaciones médicas en formato PDF.

## Características

- **Interfaz amigable:** Formulario intuitivo para ingresar información del paciente
- **Dos tipos de documentos:**
  - **Receta (Rp.):** Para prescripciones de medicamentos con formato estándar
  - **Indicaciones / Notas:** Para indicaciones preoperatorias u otras notas médicas
- **Generación de PDF:** Descarga automática del documento generado
- **Vista previa:** Visualización del contenido antes de descargar

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   cd recetas_medicas_app
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

2. **Acceder a la aplicación:**
   - La aplicación se abrirá automáticamente en tu navegador predeterminado
   - Si no se abre, accede a `http://localhost:8501`

3. **Completar el formulario:**
   - Ingresa el nombre y apellido del paciente
   - Selecciona la fecha de la receta
   - Escribe el diagnóstico
   - Elige el tipo de documento (Receta o Indicaciones)
   - Completa el contenido del documento
   - Haz clic en "Generar Documento"

4. **Descargar el PDF:**
   - Una vez generado, haz clic en "Descargar PDF" para obtener el archivo

## Estructura del Proyecto

```
recetas_medicas_app/
├── app.py                 # Archivo principal de la aplicación
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## Dependencias

- **Streamlit:** Framework para crear aplicaciones web interactivas
- **ReportLab:** Biblioteca para generar documentos PDF

## Notas Importantes

- Los datos ingresados en el formulario se guardan en la sesión actual
- Cada PDF descargado incluye la fecha en el nombre del archivo para fácil identificación
- La aplicación es completamente local y no requiere conexión a internet después de la instalación

## Soporte y Mejoras

Para reportar problemas o sugerir mejoras, por favor contacta al desarrollador.

---

**Versión:** 1.0  
**Última actualización:** 2024
