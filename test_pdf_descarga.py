"""
Script para probar la generación de PDF
"""
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

try:
    print("🔍 Probando generación de PDF...\n")
    
    # Verificar que el archivo existe
    import os
    if not os.path.exists('modeloReceta.pdf'):
        print("❌ modeloReceta.pdf no encontrado")
        print(f"📁 Archivos disponibles: {os.listdir('.')}")
        exit(1)
    
    print("✅ modeloReceta.pdf encontrado")
    
    # Leer el PDF
    reader = PdfReader('modeloReceta.pdf')
    print(f"✅ PDF leído - {len(reader.pages)} página(s)")
    
    # Crear writer
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    
    print("✅ Página copiada")
    
    # Rellenar campos
    writer.update_page_form_field_values(
        writer.pages[0],
        {
            'Date': '18/11/2025',
            'Paciente': 'Test Usuario',
            'Dx': 'Test Diagnóstico',
            'Texto1': 'Rp./\nTest contenido'
        }
    )
    
    print("✅ Campos rellenados")
    
    # Guardar a buffer (como lo hace la app)
    buffer = BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    pdf_data = buffer.getvalue()
    
    print(f"✅ PDF generado en memoria")
    print(f"📊 Tamaño del PDF: {len(pdf_data)} bytes")
    
    # Guardar a archivo para verificar
    with open('test_descarga.pdf', 'wb') as f:
        f.write(pdf_data)
    
    print(f"✅ PDF guardado como test_descarga.pdf")
    
    if len(pdf_data) > 0:
        print("\n✅ ¡TODO FUNCIONA CORRECTAMENTE!")
    else:
        print("\n❌ El PDF está vacío")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
