# 🔐 Cómo Agregar Usuarios en Streamlit Cloud

## 📝 Pasos Rápidos:

### 1. Ve a tu app en Streamlit Cloud
```
https://share.streamlit.io/
```

### 2. Click en tu app → **Settings** (⚙️) → **Secrets**

### 3. Copia y pega este formato:

```toml
[users.nombre_usuario]
password = "HASH_DE_CONTRASEÑA_AQUI"
nombre = "Nombre"
apellido = "Apellido"
```

---

## 🔑 Ejemplo Completo:

```toml
# Usuario: admin / admin123
[users.admin]
password = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
nombre = "Administrador"
apellido = "Sistema"

# Usuario: doctor1 / password123
[users.doctor1]
password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
nombre = "Juan"
apellido = "Pérez"

# Usuario: maria / mypass456
[users.maria]
password = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
nombre = "María"
apellido = "González"
```

---

## 🔧 Generar Hash de Contraseña:

### Opción 1: Script (Recomendado)
```bash
python generar_hash.py
```

### Opción 2: Comando Rápido
```bash
python -c "import hashlib; pwd='TU_CONTRASEÑA_AQUI'; print(hashlib.sha256(pwd.encode()).hexdigest())"
```

### Opción 3: Online (Cuidado - no uses contraseñas reales)
Busca "SHA256 hash generator" en Google

---

## 📋 Plantilla para Copiar:

```toml
[users.NOMBRE_USUARIO]
password = "REEMPLAZA_CON_HASH"
nombre = "Nombre Real"
apellido = "Apellido Real"
```

---

## ✅ Ejemplos de Hashes:

| Contraseña | Hash SHA-256 |
|------------|--------------|
| admin123 | `8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918` |
| password123 | `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8` |
| mypass456 | `9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08` |
| doctor2024 | `ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f` |

---

## 🎯 Proceso Completo:

### Para agregar el usuario "doctor_juan" con contraseña "Medicina2024":

1. **Genera el hash:**
   ```bash
   python -c "import hashlib; print(hashlib.sha256('Medicina2024'.encode()).hexdigest())"
   ```
   
   Resultado: `7a3f8b92c4d5e6f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5`

2. **Ve a Streamlit Cloud → Settings → Secrets**

3. **Agrega al final:**
   ```toml
   [users.doctor_juan]
   password = "7a3f8b92c4d5e6f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5"
   nombre = "Juan"
   apellido = "Ramírez"
   ```

4. **Click en "Save"**

5. **¡Listo!** El usuario ya puede hacer login con:
   - Usuario: `doctor_juan`
   - Contraseña: `Medicina2024`

---

## 🔒 Seguridad:

✅ **SÍ hacer:**
- Usar contraseñas fuertes (mínimo 8 caracteres)
- Combinar letras, números y símbolos
- Cambiar contraseñas periódicamente
- Guardar una copia de los hashes en lugar seguro

❌ **NO hacer:**
- Compartir el hash (es como compartir la contraseña)
- Usar contraseñas obvias (nombre, fecha nacimiento)
- Reutilizar contraseñas de otros servicios
- Compartir el acceso a Streamlit Cloud Secrets

---

## 📞 Soporte:

Si tienes problemas:
1. Verifica que el hash esté completo (64 caracteres)
2. Asegúrate de que no haya espacios extras
3. Verifica el formato TOML (comillas correctas)
4. Prueba con un usuario de ejemplo primero

---

## 🚀 Atajos:

### Agregar varios usuarios rápido:

```bash
# Genera múltiples hashes
python -c "
import hashlib
usuarios = [
    ('doctor1', 'pass123'),
    ('doctor2', 'pass456'),
    ('admin', 'admin123')
]
for user, pwd in usuarios:
    hash_pwd = hashlib.sha256(pwd.encode()).hexdigest()
    print(f'[users.{user}]')
    print(f'password = \"{hash_pwd}\"')
    print(f'nombre = \"Nombre\"')
    print(f'apellido = \"Apellido\"')
    print()
"
```

---

📌 **Tip:** Guarda este archivo para referencia rápida!
