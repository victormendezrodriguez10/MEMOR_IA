"""
db_helper.py
Módulo de ayuda para la gestión de base de datos PostgreSQL
Conexión y operaciones comunes para MEMOR.IA
"""

import psycopg2
from psycopg2 import pool, extras
import os
from contextlib import contextmanager
import streamlit as st

# Pool de conexiones para mejor rendimiento
connection_pool = None

def init_db_pool():
    """Inicializa el pool de conexiones a PostgreSQL"""
    global connection_pool

    if connection_pool is None:
        try:
            # Obtener DATABASE_URL de las variables de entorno o secrets de Streamlit
            database_url = os.getenv("DATABASE_URL") or st.secrets.get("DATABASE_URL")

            if not database_url:
                st.error("⚠️ DATABASE_URL no configurada. Configura tu base de datos PostgreSQL.")
                return None

            connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  # minconn
                10,  # maxconn
                database_url,
                connect_timeout=10
            )

            # Crear las tablas si no existen
            _init_tables()

            return connection_pool
        except Exception as e:
            st.error(f"❌ Error al conectar con la base de datos: {e}")
            return None

    return connection_pool

def _init_tables():
    """Crea las tablas necesarias si no existen"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    nombre VARCHAR(255) NOT NULL,
                    empresa VARCHAR(255) NOT NULL,
                    telefono VARCHAR(50),
                    cif VARCHAR(50),
                    direccion TEXT,
                    numero_cuenta VARCHAR(100),
                    rol VARCHAR(50) DEFAULT 'Usuario',
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT TRUE,
                    plan VARCHAR(50) DEFAULT 'basico',
                    fecha_expiracion DATE
                )
            ''')

            # Tabla de perfiles de empresa
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS perfiles_empresa (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER UNIQUE,
                    sector TEXT,
                    empleados VARCHAR(100),
                    experiencia_anos VARCHAR(50),
                    certificaciones TEXT,
                    otras_certificaciones TEXT,
                    experiencia_similar TEXT,
                    logo_path TEXT,
                    medios_materiales TEXT,
                    herramientas_software TEXT,
                    equipo_tecnico TEXT,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
                )
            ''')

            # Tabla de pagos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pagos (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER,
                    stripe_payment_id VARCHAR(255),
                    importe DECIMAL(10, 2),
                    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estado VARCHAR(50) DEFAULT 'pendiente',
                    plan VARCHAR(50),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
                )
            ''')

            # Tabla de tokens de recuperación
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tokens_recuperacion (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    token VARCHAR(255) NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usado BOOLEAN DEFAULT FALSE
                )
            ''')

            # Crear índices para mejorar el rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_perfiles_usuario_id ON perfiles_empresa(usuario_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_usuario_id ON pagos(usuario_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tokens_email ON tokens_recuperacion(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tokens_token ON tokens_recuperacion(token)')

            conn.commit()

@contextmanager
def get_db_connection():
    """
    Context manager para obtener conexión de base de datos
    Uso:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
    """
    pool = init_db_pool()

    if pool is None:
        raise Exception("No se pudo inicializar el pool de conexiones")

    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una query y retorna los resultados

    Args:
        query: SQL query a ejecutar
        params: Parámetros para la query (tuple o dict)
        fetch: Si True, retorna los resultados. Si False, solo ejecuta

    Returns:
        Lista de resultados o None
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query, params)

                if fetch:
                    return cursor.fetchall()
                else:
                    conn.commit()
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
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()

                if returning:
                    return cursor.fetchone()[0] if cursor.rowcount > 0 else None
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
