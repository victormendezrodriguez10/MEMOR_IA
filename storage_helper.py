"""
storage_helper.py
Módulo de gestión de archivos en Cloudinary
Maneja subida de logos y documentos para MEMOR.IA
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import streamlit as st
from io import BytesIO

# Inicializar Cloudinary
def init_cloudinary():
    """Inicializa la configuración de Cloudinary"""
    try:
        # Obtener credenciales de Cloudinary
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME") or st.secrets.get("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY") or st.secrets.get("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET") or st.secrets.get("CLOUDINARY_API_SECRET")

        if not all([cloud_name, api_key, api_secret]):
            st.warning("⚠️ Cloudinary no configurado. Los archivos no se guardarán.")
            return False

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )

        return True
    except Exception as e:
        st.error(f"❌ Error al configurar Cloudinary: {e}")
        return False

def upload_logo(file_data, usuario_id, filename):
    """
    Sube un logo a Cloudinary

    Args:
        file_data: Archivo en bytes o UploadedFile de Streamlit
        usuario_id: ID del usuario
        filename: Nombre del archivo

    Returns:
        URL del logo subido o None si falla
    """
    if not init_cloudinary():
        return None

    try:
        # Si es un UploadedFile de Streamlit, obtener los bytes
        if hasattr(file_data, 'read'):
            file_bytes = file_data.read()
            file_data.seek(0)  # Reset para futuras lecturas
        else:
            file_bytes = file_data

        # Subir a Cloudinary en la carpeta "logos"
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=f"memoria_ia/logos",
            public_id=f"usuario_{usuario_id}_{filename}",
            resource_type="auto",
            overwrite=True,
            invalidate=True
        )

        return result['secure_url']
    except Exception as e:
        st.error(f"❌ Error al subir logo: {e}")
        return None

def upload_document(file_data, usuario_id, filename):
    """
    Sube un documento a Cloudinary

    Args:
        file_data: Archivo en bytes o UploadedFile de Streamlit
        usuario_id: ID del usuario
        filename: Nombre del archivo

    Returns:
        URL del documento subido o None si falla
    """
    if not init_cloudinary():
        return None

    try:
        # Si es un UploadedFile de Streamlit, obtener los bytes
        if hasattr(file_data, 'read'):
            file_bytes = file_data.read()
            file_data.seek(0)  # Reset para futuras lecturas
        else:
            file_bytes = file_data

        # Subir a Cloudinary en la carpeta "documentos"
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=f"memoria_ia/documentos",
            public_id=f"usuario_{usuario_id}_{filename}",
            resource_type="auto",
            overwrite=True,
            invalidate=True
        )

        return result['secure_url']
    except Exception as e:
        st.error(f"❌ Error al subir documento: {e}")
        return None

def delete_file(url):
    """
    Elimina un archivo de Cloudinary

    Args:
        url: URL completa del archivo en Cloudinary

    Returns:
        True si se eliminó, False si falla
    """
    if not init_cloudinary():
        return False

    try:
        # Extraer public_id de la URL
        # Ejemplo: https://res.cloudinary.com/cloud/image/upload/v123/folder/file.jpg
        # public_id sería: folder/file
        parts = url.split('/')
        version_index = next((i for i, part in enumerate(parts) if part.startswith('v')), None)

        if version_index is None:
            return False

        # El public_id está después de la versión
        public_id_parts = parts[version_index + 1:]
        public_id = '/'.join(public_id_parts)

        # Quitar la extensión
        public_id = public_id.rsplit('.', 1)[0]

        # Eliminar el archivo
        result = cloudinary.uploader.destroy(public_id)

        return result.get('result') == 'ok'
    except Exception as e:
        st.warning(f"⚠️ No se pudo eliminar el archivo: {e}")
        return False

def get_file_url(folder, usuario_id, filename):
    """
    Obtiene la URL de un archivo en Cloudinary

    Args:
        folder: "logos" o "documentos"
        usuario_id: ID del usuario
        filename: Nombre del archivo

    Returns:
        URL del archivo o None
    """
    if not init_cloudinary():
        return None

    try:
        public_id = f"memoria_ia/{folder}/usuario_{usuario_id}_{filename}"

        # Verificar si existe
        result = cloudinary.api.resource(public_id)

        return result.get('secure_url')
    except cloudinary.exceptions.NotFound:
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
        Lista de URLs o lista vacía
    """
    if not init_cloudinary():
        return []

    try:
        # Buscar archivos en la carpeta del usuario
        result = cloudinary.api.resources(
            type="upload",
            prefix=f"memoria_ia/{folder}/usuario_{usuario_id}_",
            max_results=100
        )

        return [resource['secure_url'] for resource in result.get('resources', [])]
    except Exception as e:
        st.warning(f"⚠️ Error al listar archivos: {e}")
        return []
