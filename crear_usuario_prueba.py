"""
Script para crear un usuario de prueba
"""
from auth import AuthManager

# Crear instancia del gestor de autenticación
auth = AuthManager()

# Crear usuario de prueba
print("🔧 Creando usuario de prueba...\n")

success, message = auth.register_user(
    username="admin",
    password="admin123",
    nombre="Administrador",
    apellido="Sistema"
)

print(message)

if success:
    print("\n📋 Credenciales de prueba:")
    print("   Usuario: admin")
    print("   Contraseña: admin123")
    print("\n⚠️ IMPORTANTE: Cambia estas credenciales en producción")
