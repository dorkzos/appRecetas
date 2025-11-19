"""
Script de prueba para rellenar el PDF modelo
"""
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime

def test_rellenar_pdf():
    try:
        print("🔍 Leyendo PDF modelo...")
        reader = PdfReader("modeloReceta.pdf")
        writer = PdfWriter()
        
        # Copiar páginas
        for page in reader.pages:
            writer.add_page(page)
        
        print("✅ PDF leído correctamente")
        
        # Datos de prueba
        contenido_original = "Rp.\n/\nParacetamol 500mg - 1 tableta cada 8 horas\nDescanso por 3 días"
        contenido_formateado = contenido_original.replace("Rp.\n/", "Rp./")
        
        datos = {
            "Date": "18/11/2025",
            "Paciente": "Juan Pérez",
            "Dx": "Gripe común",
            "Texto1": contenido_formateado
        }
        
        print(f"\n📝 Formato original: {repr(contenido_original[:20])}...")
        print(f"✨ Formato corregido: {repr(contenido_formateado[:20])}...")
        
        print("\n📝 Rellenando campos:")
        for campo, valor in datos.items():
            print(f"   {campo}: {valor[:30]}...")
        
        # Rellenar campos
        writer.update_page_form_field_values(
            writer.pages[0],
            datos
        )
        
        # Guardar
        with open("receta_prueba.pdf", "wb") as output_file:
            writer.write(output_file)
        
        print("\n✅ ¡PDF generado exitosamente!")
        print("📄 Revisa el archivo: receta_prueba.pdf")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Posibles soluciones:")
        print("   1. El PDF puede tener los campos aplanados (flatten)")
        print("   2. Los nombres de los campos pueden ser diferentes")
        print("   3. El PDF puede estar protegido")

if __name__ == "__main__":
    test_rellenar_pdf()
