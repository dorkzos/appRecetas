# 🔐 Guía de Almacenamiento de Usuarios en Streamlit Cloud

Esta guía explica 3 formas de almacenar usuarios de forma segura cuando tu app está en Streamlit Cloud.

---

## 📋 Comparación de Opciones

| Característica | Streamlit Secrets | Google Sheets | SQLite + GitHub |
|----------------|-------------------|---------------|-----------------|
| **Dificultad** | ⭐ Fácil | ⭐⭐ Media | ⭐ Fácil |
| **Costo** | ✅ Gratis | ✅ Gratis | ✅ Gratis |
| **Edición remota** | ❌ No (requiere redeploy) | ✅ Sí (desde cualquier lugar) | ❌ No |
| **Registro automático** | ❌ No | ✅ Sí | ✅ Sí |
| **Privacidad** | ✅ Alta | ✅ Media-Alta | ✅ Media |
| **Mejor para** | Pocos usuarios fijos | Muchos usuarios | Usuarios moderados |

---

## 🎯 OPCIÓN 1: Streamlit Secrets (Recomendada para pocos usuarios)

### ✅ Ventajas:
- Muy fácil de configurar
- Totalmente privado
- Sin dependencias adicionales

### ❌ Desventajas:
- Requiere redeploy para agregar usuarios
- No permite registro automático desde la app

### 📝 Configuración:

#### 1. En Streamlit Cloud:

Ve a tu app → Settings → Secrets y agrega:

```toml
[users.admin]
password = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"  # Hash de "admin123"
nombre = "Administrador"
apellido = "Sistema"

[users.doctor1]
password = "e7d80ffeefa212b7c5c55700e4f7193e6b6f07d7e5c6b2e2e5e5e5e5e5e5e5e5"
nombre = "Juan"
apellido = "Pérez"
```

#### 2. Genera hashes de contraseñas:

```bash
python -c "import hashlib; print(hashlib.sha256('tu_contraseña'.encode()).hexdigest())"
```

#### 3. En `app.py`, el código YA está listo:

```python
from auth import AuthManager

# Usa secrets automáticamente si están disponibles
auth_manager = AuthManager()
```

✅ **Ya está implementado en tu código actual**

---

## 🎯 OPCIÓN 2: Google Sheets (RECOMENDADA - Flexible)

### ✅ Ventajas:
- Editas usuarios desde cualquier lugar
- Permite registro automático desde la app
- Interfaz familiar (Excel en la nube)
- Puedes compartir acceso con otros

### 📝 Configuración:

#### 1. Crear Google Sheet:

1. Ve a [Google Sheets](https://sheets.google.com)
2. Crea una nueva hoja llamada "AppRecetas"
3. Renombra la primera pestaña a "users"
4. Crea estos encabezados en la fila 1:
   ```
   username | password | nombre | apellido
   ```

#### 2. Obtener Service Account:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto (o usa uno existente)
3. Habilita "Google Sheets API"
4. Crea una Service Account
5. Genera una clave JSON
6. Comparte tu Google Sheet con el email de la service account

#### 3. En Streamlit Cloud:

Settings → Secrets:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/TU_ID_AQUI/edit"
type = "service_account"
project_id = "tu-proyecto"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "tu-service-account@..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

#### 4. Instalar dependencia:

Agrega a `requirements.txt`:
```
streamlit-gsheets==0.0.3
```

#### 5. Cambiar en `app.py`:

```python
from auth_gsheets import AuthManagerGSheets

# Usar Google Sheets
auth_manager = AuthManagerGSheets()
```

#### 6. Agregar usuarios directamente en Google Sheets:

| username | password (hash SHA-256) | nombre | apellido |
|----------|------------------------|--------|----------|
| admin | 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918 | Admin | Sistema |

---

## 🎯 OPCIÓN 3: SQLite + GitHub (Simple)

### ✅ Ventajas:
- Simple y rápido
- No requiere configuración externa
- Permite registro automático

### ❌ Desventajas:
- El archivo .db debe estar en .gitignore por seguridad
- No se sincroniza automáticamente entre deploys

### 📝 Configuración:

#### 1. En `app.py`:

```python
from auth_sqlite import AuthManagerSQLite

# Usar SQLite
auth_manager = AuthManagerSQLite()
```

#### 2. Actualizar `.gitignore`:

```
# Base de datos de usuarios (seguridad)
users.json
users.db
```

#### 3. En producción:

Tendrás que crear usuarios cada vez que se redeploy la app, o mantener el archivo `users.db` localmente y subirlo manualmente.

---

## 🏆 Recomendación Final

**Para tu caso (app médica con acceso controlado):**

### 👑 Mejor opción: **Google Sheets**

**Por qué:**
- ✅ Editas usuarios desde tu celular/computadora
- ✅ No requiere redeploy para agregar usuarios
- ✅ Puedes tener un backup automático
- ✅ Control total sobre quién tiene acceso

### 🥈 Alternativa: **Streamlit Secrets**

Si solo necesitas 2-3 usuarios fijos que nunca cambiarán.

---

## 🔧 ¿Necesitas ayuda para configurar?

Dime cuál opción prefieres y te ayudo paso a paso con:
1. Configuración completa
2. Migración de usuarios existentes
3. Scripts de administración
4. Deploy a producción

---

## 🔒 Recordatorio de Seguridad

**NUNCA subas a GitHub:**
- ❌ `users.json`
- ❌ `users.db`
- ❌ Claves de servicio de Google (.json)
- ❌ Contraseñas en texto plano

**SIEMPRE:**
- ✅ Usa hashes SHA-256 para contraseñas
- ✅ Mantén secrets en Streamlit Cloud
- ✅ Usa .gitignore correctamente
