"""
Sistema de autenticación simple para la aplicación de recetas
"""
import json
import hashlib
import os
from pathlib import Path


class AuthManager:
    """Gestor de autenticación de usuarios"""
    
    def __init__(self, users_file="users.json", use_secrets=False):
        self.users_file = users_file
        self.use_secrets = use_secrets
        
        # Detectar automáticamente si estamos en Streamlit Cloud
        try:
            import streamlit as st
            if hasattr(st, 'secrets') and 'users' in st.secrets:
                self.use_secrets = True
        except:
            pass
        
        if not self.use_secrets:
            self._inicializar_archivo()
    
    def _inicializar_archivo(self):
        """Crea el archivo de usuarios si no existe"""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        """Carga los usuarios desde el archivo o Streamlit Secrets"""
        if self.use_secrets:
            try:
                import streamlit as st
                # Convertir los secrets a diccionario
                users = {}
                for username in st.secrets.users:
                    users[username] = dict(st.secrets.users[username])
                return users
            except:
                return {}
        else:
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
    
    def _save_users(self, users):
        """Guarda los usuarios en el archivo (solo modo local)"""
        if self.use_secrets:
            # En modo secrets, no podemos guardar automáticamente
            raise Exception("❌ No se pueden crear usuarios automáticamente con Streamlit Secrets. Debes agregarlos manualmente en la configuración de Streamlit Cloud.")
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
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
        
        # Cargar usuarios existentes
        users = self._load_users()
        
        # Verificar si el usuario ya existe
        if username in users:
            return False, "⚠️ El usuario ya existe"
        
        # Crear nuevo usuario
        users[username] = {
            "password": self._hash_password(password),
            "nombre": nombre,
            "apellido": apellido
        }
        
        # Guardar
        self._save_users(users)
        
        return True, "✅ Usuario registrado exitosamente"
    
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
    
    def change_password(self, username, old_password, new_password):
        """
        Cambia la contraseña de un usuario
        Retorna (success: bool, message: str)
        """
        if len(new_password) < 6:
            return False, "⚠️ La nueva contraseña debe tener al menos 6 caracteres"
        
        users = self._load_users()
        
        if username not in users:
            return False, "❌ Usuario no encontrado"
        
        # Verificar contraseña actual
        if users[username]["password"] != self._hash_password(old_password):
            return False, "❌ Contraseña actual incorrecta"
        
        # Actualizar contraseña
        users[username]["password"] = self._hash_password(new_password)
        self._save_users(users)
        
        return True, "✅ Contraseña actualizada exitosamente"
