#!/bin/bash

# Script para ejecutar la aplicación Streamlit

cd "$(dirname "$0")"

# Activar el entorno virtual
source venv/bin/activate

# Ejecutar Streamlit
streamlit run app.py
