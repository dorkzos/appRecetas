"""
Script para leer los campos de formulario de modeloReceta.pdf
"""
from pypdf import PdfReader

def extraer_campos_pdf(ruta_pdf):
    """
    Extrae los nombres de los campos de un formulario PDF
    """
    try:
        reader = PdfReader(ruta_pdf)
        
        fields = reader.get_fields()
        
        if fields:
            print(f"📋 CAMPOS ENCONTRADOS EN EL PDF ({len(fields)} campos):\n")
            print("=" * 60)
            
            for i, (field_name, field_info) in enumerate(fields.items(), 1):
                print(f"\n{i}. Campo: '{field_name}'")
                print(f"   Tipo: {field_info.get('/FT', 'Desconocido')}")
                
                # Obtener valor actual si existe
                valor = field_info.get('/V', None)
                if valor:
                    print(f"   Valor actual: {valor}")
                
                # Obtener valor por defecto si existe
                default = field_info.get('/DV', None)
                if default:
                    print(f"   Valor por defecto: {default}")
                
                # Flags del campo
                flags = field_info.get('/Ff', None)
                if flags:
                    print(f"   Flags: {flags}")
                
                print("-" * 60)
            
            print("\n" + "=" * 60)
            print(f"\n✅ Total de campos: {len(fields)}")
            
        else:
            print("❌ No se encontraron campos de formulario en este PDF")
            print("\nℹ️  Esto puede significar que:")
            print("   - El PDF no tiene campos de formulario")
            print("   - El PDF tiene campos aplanados (no editables)")
            print("   - El PDF está protegido")
            
    except Exception as e:
        print(f"❌ Error al leer el PDF: {str(e)}")

if __name__ == "__main__":
    ruta_pdf = "modeloReceta.pdf"
    print(f"🔍 Analizando archivo: {ruta_pdf}\n")
    extraer_campos_pdf(ruta_pdf)
