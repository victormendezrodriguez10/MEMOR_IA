"""
storage_helper.py
Módulo de gestión de archivos local (versión SQLite)
Maneja subida de logos y documentos para MEMOR.IA
"""

import os
import shutil
from pathlib import Path
import streamlit as st

# Directorios para almacenamiento local
LOGOS_DIR = "logos_usuarios"
DOCS_DIR = "documentos_usuarios"

def init_cloudinary():
    """Función de compatibilidad con versión Cloudinary"""
    return init_storage()

def init_storage():
    """Inicializa los directorios de almacenamiento local"""
    try:
        Path(LOGOS_DIR).mkdir(exist_ok=True)
        Path(DOCS_DIR).mkdir(exist_ok=True)
        return True
    except Exception as e:
        st.error(f"❌ Error al crear directorios: {e}")
        return False

def upload_logo(file_data, usuario_id, filename):
    """
    Guarda un logo localmente

    Args:
        file_data: Archivo en bytes o UploadedFile de Streamlit
        usuario_id: ID del usuario
        filename: Nombre del archivo

    Returns:
        Path del logo guardado o None si falla
    """
    if not init_storage():
        return None

    try:
        # Crear directorio del usuario si no existe
        user_dir = Path(LOGOS_DIR) / str(usuario_id)
        user_dir.mkdir(exist_ok=True)

        # Ruta completa del archivo
        file_path = user_dir / filename

        # Si es un UploadedFile de Streamlit, obtener los bytes
        if hasattr(file_data, 'read'):
            file_bytes = file_data.read()
            file_data.seek(0)  # Reset para futuras lecturas
        else:
            file_bytes = file_data

        # Guardar el archivo
        with open(file_path, 'wb') as f:
            f.write(file_bytes)

        # SOLUCIÓN: Retornar path absoluto para evitar problemas de carga
        return str(file_path.absolute())
    except Exception as e:
        st.error(f"❌ Error al guardar logo: {e}")
        return None

def upload_document(file_data, usuario_id, filename):
    """
    Guarda un documento localmente

    Args:
        file_data: Archivo en bytes o UploadedFile de Streamlit
        usuario_id: ID del usuario
        filename: Nombre del archivo

    Returns:
        Path del documento guardado o None si falla
    """
    if not init_storage():
        return None

    try:
        # Crear directorio del usuario si no existe
        user_dir = Path(DOCS_DIR) / str(usuario_id)
        user_dir.mkdir(exist_ok=True)

        # Ruta completa del archivo
        file_path = user_dir / filename

        # Si es un UploadedFile de Streamlit, obtener los bytes
        if hasattr(file_data, 'read'):
            file_bytes = file_data.read()
            file_data.seek(0)  # Reset para futuras lecturas
        else:
            file_bytes = file_data

        # Guardar el archivo
        with open(file_path, 'wb') as f:
            f.write(file_bytes)

        # SOLUCIÓN: Retornar path absoluto para evitar problemas de carga
        return str(file_path.absolute())
    except Exception as e:
        st.error(f"❌ Error al guardar documento: {e}")
        return None

def delete_file(file_path):
    """
    Elimina un archivo local

    Args:
        file_path: Path del archivo

    Returns:
        True si se eliminó, False si falla
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        st.warning(f"⚠️ No se pudo eliminar el archivo: {e}")
        return False

def get_file_url(folder, usuario_id, filename):
    """
    Obtiene la ruta de un archivo local

    Args:
        folder: "logos" o "documentos"
        usuario_id: ID del usuario
        filename: Nombre del archivo

    Returns:
        Path del archivo o None
    """
    try:
        base_dir = LOGOS_DIR if folder == "logos" else DOCS_DIR
        file_path = Path(base_dir) / str(usuario_id) / filename

        if file_path.exists():
            # SOLUCIÓN: Retornar path absoluto
            return str(file_path.absolute())
        return None
    except Exception as e:
        st.warning(f"⚠️ Error al obtener archivo: {e}")
        return None

def list_user_files(usuario_id, folder="logos"):
    """
    Lista todos los archivos de un usuario

    Args:
        usuario_id: ID del usuario
        folder: "logos" o "documentos"

    Returns:
        Lista de paths o lista vacía
    """
    try:
        base_dir = LOGOS_DIR if folder == "logos" else DOCS_DIR
        user_dir = Path(base_dir) / str(usuario_id)

        if not user_dir.exists():
            return []

        files = [str(f) for f in user_dir.iterdir() if f.is_file()]
        return files
    except Exception as e:
        st.warning(f"⚠️ Error al listar archivos: {e}")
        return []

# Inicializar almacenamiento al importar
init_storage()
