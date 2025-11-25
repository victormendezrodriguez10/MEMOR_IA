"""
db_helper.py
Módulo de ayuda para la gestión de base de datos PostgreSQL (Neon)
Conexión y operaciones comunes para MEMOR.IA
"""

import psycopg2
from psycopg2 import pool, extras
import os
from contextlib import contextmanager
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Priorizar st.secrets si está disponible (Streamlit), sino usar .env
DATABASE_URL = None
try:
    # En Streamlit Cloud, usar secrets
    DATABASE_URL = st.secrets["DATABASE_URL"]
except:
    # En local, usar .env
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL no configurado. Revisa .env o Streamlit secrets")

# Pool de conexiones global
connection_pool = None

def init_db_pool():
    """Inicializa el pool de conexiones a PostgreSQL"""
    global connection_pool

    if connection_pool is None:
        try:
            if not DATABASE_URL:
                raise ValueError("DATABASE_URL no está configurado")

            connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  # minconn
                10,  # maxconn
                DATABASE_URL
            )
            if connection_pool:
                print("✅ Pool de conexiones PostgreSQL inicializado")
                return True
            else:
                raise Exception("No se pudo crear el pool de conexiones")
        except Exception as e:
            error_msg = f"❌ Error al inicializar pool de conexiones: {e}"
            print(error_msg)
            st.error(error_msg)
            raise Exception(f"No se pudo inicializar el pool de conexiones: {e}")
    return True

def init_db():
    """Función de compatibilidad - las tablas ya están creadas en Neon"""
    return init_db_pool()

@contextmanager
def get_db_connection():
    """
    Context manager para obtener conexión de base de datos PostgreSQL
    Uso:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
    """
    conn = None
    try:
        if connection_pool is None:
            init_db_pool()

        if connection_pool is None:
            raise Exception("No se pudo inicializar el pool de conexiones")

        conn = connection_pool.getconn()
        # Usar RealDictCursor para acceder a columnas por nombre
        conn.cursor_factory = extras.RealDictCursor
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn and connection_pool:
            connection_pool.putconn(conn)

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una query y retorna los resultados

    Args:
        query: SQL query a ejecutar
        params: Parámetros para la query (tuple)
        fetch: Si True, retorna los resultados. Si False, solo ejecuta

    Returns:
        Lista de resultados o None
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                rows = cursor.fetchall()
                # RealDictCursor ya retorna diccionarios
                return rows
            else:
                return None
    except Exception as e:
        st.error(f"Error en la query: {e}")
        return None

def execute_insert(query, params=None, returning=True):
    """
    Ejecuta un INSERT y retorna el ID insertado

    Args:
        query: SQL INSERT query
        params: Parámetros para la query
        returning: Si True, retorna el ID insertado

    Returns:
        ID del registro insertado o None
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if returning:
                # En PostgreSQL usamos RETURNING id
                if "RETURNING" in query.upper():
                    result = cursor.fetchone()
                    return result['id'] if result else None
                else:
                    return True
            return True
    except Exception as e:
        st.error(f"Error al insertar: {e}")
        return None

def close_all_connections():
    """Cierra todas las conexiones del pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None

# Inicializar el pool al importar el módulo
init_db_pool()
