"""
Sistema de autenticación con Google Sheets
Permite almacenar y gestionar usuarios en una hoja de cálculo de Google
"""
import hashlib
import streamlit as st

try:
    from streamlit_gsheets import GSheetsConnection
    GSHEETS_AVAILABLE = True
except ImportError:
    GSHEETS_AVAILABLE = False


class AuthManagerGSheets:
    """Gestor de autenticación usando Google Sheets"""
    
    def __init__(self):
        if not GSHEETS_AVAILABLE:
            raise ImportError("❌ Instala streamlit-gsheets: pip install streamlit-gsheets")
        
        self.conn = st.connection("gsheets", type=GSheetsConnection)
    
    def _hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        """Carga los usuarios desde Google Sheets"""
        try:
            df = self.conn.read(worksheet="users", usecols=[0, 1, 2, 3])
            # Convertir DataFrame a diccionario
            users = {}
            for _, row in df.iterrows():
                users[row['username']] = {
                    'password': row['password'],
                    'nombre': row['nombre'],
                    'apellido': row['apellido']
                }
            return users
        except Exception as e:
            st.error(f"Error al cargar usuarios: {str(e)}")
            return {}
    
    def _save_user(self, username, password_hash, nombre, apellido):
        """Guarda un nuevo usuario en Google Sheets"""
        try:
            # Leer datos actuales
            df = self.conn.read(worksheet="users")
            
            # Agregar nueva fila
            new_row = {
                'username': username,
                'password': password_hash,
                'nombre': nombre,
                'apellido': apellido
            }
            
            # Actualizar Google Sheet
            df = df.append(new_row, ignore_index=True)
            self.conn.update(worksheet="users", data=df)
            
            return True
        except Exception as e:
            st.error(f"Error al guardar usuario: {str(e)}")
            return False
    
    def register_user(self, username, password, nombre, apellido):
        """
        Registra un nuevo usuario
        Retorna (success: bool, message: str)
        """
        # Validaciones
        if not username or not password:
            return False, "⚠️ Usuario y contraseña son obligatorios"
        
        if len(username) < 3:
            return False, "⚠️ El usuario debe tener al menos 3 caracteres"
        
        if len(password) < 6:
            return False, "⚠️ La contraseña debe tener al menos 6 caracteres"
        
        if not nombre or not apellido:
            return False, "⚠️ Nombre y apellido son obligatorios"
        
        # Verificar si el usuario ya existe
        users = self._load_users()
        if username in users:
            return False, "⚠️ El usuario ya existe"
        
        # Guardar nuevo usuario
        password_hash = self._hash_password(password)
        success = self._save_user(username, password_hash, nombre, apellido)
        
        if success:
            return True, "✅ Usuario registrado exitosamente"
        else:
            return False, "❌ Error al registrar usuario"
    
    def login(self, username, password):
        """
        Autentica un usuario
        Retorna (success: bool, user_data: dict or None, message: str)
        """
        if not username or not password:
            return False, None, "⚠️ Usuario y contraseña son obligatorios"
        
        users = self._load_users()
        
        if username not in users:
            return False, None, "❌ Usuario o contraseña incorrectos"
        
        user_data = users[username]
        password_hash = self._hash_password(password)
        
        if user_data["password"] != password_hash:
            return False, None, "❌ Usuario o contraseña incorrectos"
        
        # Login exitoso
        return True, {
            "username": username,
            "nombre": user_data["nombre"],
            "apellido": user_data["apellido"]
        }, "✅ Login exitoso"
