"""
Script para generar hashes SHA-256 de contraseñas
Usa esto para crear contraseñas para Streamlit Secrets
"""
import hashlib

def generar_hash(password):
    """Genera el hash SHA-256 de una contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

print("🔐 Generador de Hashes para Streamlit Secrets\n")
print("=" * 60)

# Ejemplos
ejemplos = [
    ("admin123", "Para usuario admin"),
    ("password123", "Contraseña de ejemplo"),
]

print("\n📋 Ejemplos:\n")
for password, descripcion in ejemplos:
    hash_result = generar_hash(password)
    print(f"Contraseña: {password} ({descripcion})")
    print(f"Hash: {hash_result}")
    print()

# Modo interactivo
print("=" * 60)
print("\n💡 Genera tu propio hash:")
print("   Escribe una contraseña y presiona Enter")
print("   (o escribe 'salir' para terminar)\n")

while True:
    password = input("Contraseña: ")
    
    if password.lower() in ['salir', 'exit', 'quit', '']:
        print("\n👋 ¡Hasta luego!")
        break
    
    if len(password) < 6:
        print("⚠️  La contraseña debe tener al menos 6 caracteres\n")
        continue
    
    hash_result = generar_hash(password)
    print(f"✅ Hash: {hash_result}\n")
    
    # Formato para copiar a Streamlit Secrets
    print("📋 Para copiar a Streamlit Secrets:")
    print(f'password = "{hash_result}"')
    print()
