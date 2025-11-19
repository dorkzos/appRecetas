"""
Sistema de autenticación con SQLite
Base de datos local simple y liviana
"""
import sqlite3
import hashlib
import os
from pathlib import Path


class AuthManagerSQLite:
    """Gestor de autenticación usando SQLite"""
    
    def __init__(self, db_file="users.db"):
        self.db_file = db_file
        self._inicializar_db()
    
    def _inicializar_db(self):
        """Crea la base de datos y tabla si no existen"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
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
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Intentar insertar el usuario
            cursor.execute(
                'INSERT INTO users (username, password, nombre, apellido) VALUES (?, ?, ?, ?)',
                (username, self._hash_password(password), nombre, apellido)
            )
            
            conn.commit()
            conn.close()
            
            return True, "✅ Usuario registrado exitosamente"
            
        except sqlite3.IntegrityError:
            return False, "⚠️ El usuario ya existe"
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
    
    def login(self, username, password):
        """
        Autentica un usuario
        Retorna (success: bool, user_data: dict or None, message: str)
        """
        if not username or not password:
            return False, None, "⚠️ Usuario y contraseña son obligatorios"
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                'SELECT password, nombre, apellido FROM users WHERE username = ?',
                (username,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, None, "❌ Usuario o contraseña incorrectos"
            
            stored_password, nombre, apellido = result
            password_hash = self._hash_password(password)
            
            if stored_password != password_hash:
                return False, None, "❌ Usuario o contraseña incorrectos"
            
            # Login exitoso
            return True, {
                "username": username,
                "nombre": nombre,
                "apellido": apellido
            }, "✅ Login exitoso"
            
        except Exception as e:
            return False, None, f"❌ Error: {str(e)}"
    
    def change_password(self, username, old_password, new_password):
        """
        Cambia la contraseña de un usuario
        Retorna (success: bool, message: str)
        """
        if len(new_password) < 6:
            return False, "⚠️ La nueva contraseña debe tener al menos 6 caracteres"
        
        # Verificar credenciales actuales
        success, _, _ = self.login(username, old_password)
        if not success:
            return False, "❌ Contraseña actual incorrecta"
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute(
                'UPDATE users SET password = ? WHERE username = ?',
                (self._hash_password(new_password), username)
            )
            
            conn.commit()
            conn.close()
            
            return True, "✅ Contraseña actualizada exitosamente"
            
        except Exception as e:
            return False, f"❌ Error: {str(e)}"
