# Arquivo: core/database_access.py

import psycopg2
import os

def connect_to_db():
    """
    Função para conectar ao banco de dados PostgreSQL.
    As credenciais são obtidas de variáveis de ambiente.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME", "sicon"),
            user=os.environ.get("DB_USER", "postgres"),
            password=os.environ.get("DB_PASSWORD", "AbnP@2009"),
            host=os.environ.get("DB_HOST", "localhost"),
            port=os.environ.get("DB_PORT", "5432")
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None