# Arquivo: core/user_manager.py

import psycopg2
from psycopg2 import sql
import bcrypt
from .database_access import connect_to_db
from .session_manager import set_logged_in_user

def hash_password(password):
    """Cria um hash seguro da senha."""
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def validate_user(username, password):
    """
    Valida as credenciais do usuário no banco de dados.
    """
    conn = connect_to_db()
    if conn is None:
        return False

    try:
        with conn.cursor() as cur:
            query = sql.SQL("SELECT password FROM users WHERE username = %s")
            cur.execute(query, (username,))
            result = cur.fetchone()

            if result is None:
                print("Usuário ou senha inválidos.")
                return False
            
            stored_hashed_password = result[0].encode('utf-8')
            password_bytes = password.encode('utf-8')

            if bcrypt.checkpw(password_bytes, stored_hashed_password):
                print("Login bem-sucedido.")
                set_logged_in_user(username)
                return True
            else:
                print("Usuário ou senha inválidos.")
                return False
    except psycopg2.Error as e:
        print(f"Erro na consulta SQL: {e}")
        return False
    finally:
        if conn:
            conn.close()

def create_user(username, password):
    """
    Cria um novo usuário com a senha hasheada.
    """
    conn = connect_to_db()
    if conn is None:
        return False
    
    try:
        hashed_password = hash_password(password)
        with conn.cursor() as cur:
            query = sql.SQL("INSERT INTO users (username, password) VALUES (%s, %s)")
            cur.execute(query, (username, hashed_password))
            conn.commit()
            print(f"Usuário '{username}' criado com sucesso.")
            return True
    except psycopg2.Error as e:
        print(f"Erro ao criar usuário: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()