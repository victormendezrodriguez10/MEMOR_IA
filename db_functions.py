"""
db_functions.py
Funciones de base de datos para SQLite
Para MEMOR.IA
"""

import hashlib
import json
import secrets
import string
from datetime import datetime, timedelta
from db_helper import get_db_connection
from storage_helper import upload_logo, upload_document
import streamlit as st

def generar_password():
    """Genera una contraseña aleatoria segura"""
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(caracteres) for _ in range(12))
    return password

def registrar_usuario(datos_usuario):
    """Registra un nuevo usuario en la base de datos"""
    password = generar_password()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios
                (email, password, nombre, empresa, telefono, cif, direccion, numero_cuenta, plan, fecha_expiracion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                datos_usuario['email'],
                password_hash,
                datos_usuario['nombre'],
                datos_usuario['empresa'],
                datos_usuario['telefono'],
                datos_usuario['cif'],
                datos_usuario['direccion'],
                datos_usuario.get('numero_cuenta', ''),
                'basico',
                (datetime.now() + timedelta(days=30)).date()
            ))
            return password
    except Exception as e:
        st.error(f"Error al registrar usuario: {e}")
        return None

def obtener_perfil_empresa(usuario_email):
    """Obtiene el perfil de empresa de un usuario"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pe.* FROM perfiles_empresa pe
                JOIN usuarios u ON pe.usuario_id = u.id
                WHERE u.email = %s
            ''', (usuario_email,))

            resultado = cursor.fetchone()

            if resultado:
                return {
                    'sector': resultado['sector'],
                    'empleados': resultado['empleados'],
                    'experiencia_anos': resultado['experiencia_anos'],
                    'certificaciones': json.loads(resultado['certificaciones']) if resultado['certificaciones'] else [],
                    'otras_certificaciones': resultado['otras_certificaciones'],
                    'experiencia_similar': resultado['experiencia_similar'],
                    'logo_path': resultado['logo_path'],
                    'medios_materiales': resultado['medios_materiales'],
                    'herramientas_software': resultado['herramientas_software'],
                    'equipo_tecnico': json.loads(resultado['equipo_tecnico']) if resultado['equipo_tecnico'] else [],
                    'fecha_actualizacion': resultado['fecha_actualizacion']
                }
            return None
    except Exception as e:
        st.error(f"Error al obtener perfil: {e}")
        return None

def guardar_perfil_empresa(usuario_email, datos_perfil):
    """Guarda o actualiza el perfil de empresa de un usuario"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Obtener ID del usuario
            cursor.execute('SELECT id FROM usuarios WHERE email = %s', (usuario_email,))
            usuario_result = cursor.fetchone()

            if not usuario_result:
                return False

            usuario_id = usuario_result['id']

            # Verificar si ya existe un perfil
            cursor.execute('SELECT id FROM perfiles_empresa WHERE usuario_id = %s', (usuario_id,))
            existe = cursor.fetchone()

            # Preparar datos JSON
            certificaciones_json = json.dumps(datos_perfil.get('certificaciones', []))
            equipo_tecnico_json = json.dumps(datos_perfil.get('equipo_tecnico', []))

            if existe:
                # Actualizar perfil existente
                cursor.execute('''
                    UPDATE perfiles_empresa SET
                        sector = %s, empleados = %s, experiencia_anos = %s,
                        certificaciones = %s, otras_certificaciones = %s,
                        experiencia_similar = %s, logo_path = %s,
                        medios_materiales = %s, herramientas_software = %s,
                        equipo_tecnico = %s, fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE usuario_id = %s
                ''', (
                    datos_perfil.get('sector', ''),
                    datos_perfil.get('empleados', ''),
                    datos_perfil.get('experiencia_anos', ''),
                    certificaciones_json,
                    datos_perfil.get('otras_certificaciones', ''),
                    datos_perfil.get('experiencia_similar', ''),
                    datos_perfil.get('logo_path', ''),
                    datos_perfil.get('medios_materiales', ''),
                    datos_perfil.get('herramientas_software', ''),
                    equipo_tecnico_json,
                    usuario_id
                ))
            else:
                # Crear nuevo perfil
                cursor.execute('''
                    INSERT INTO perfiles_empresa
                    (usuario_id, sector, empleados, experiencia_anos,
                     certificaciones, otras_certificaciones, experiencia_similar,
                     logo_path, medios_materiales, herramientas_software, equipo_tecnico)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    usuario_id,
                    datos_perfil.get('sector', ''),
                    datos_perfil.get('empleados', ''),
                    datos_perfil.get('experiencia_anos', ''),
                    certificaciones_json,
                    datos_perfil.get('otras_certificaciones', ''),
                    datos_perfil.get('experiencia_similar', ''),
                    datos_perfil.get('logo_path', ''),
                    datos_perfil.get('medios_materiales', ''),
                    datos_perfil.get('herramientas_software', ''),
                    equipo_tecnico_json
                ))

            return True
    except Exception as e:
        st.error(f"Error al guardar perfil: {e}")
        return False

def obtener_usuario_id(usuario_email):
    """Obtiene el ID de un usuario por su email"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM usuarios WHERE email = %s', (usuario_email,))
            result = cursor.fetchone()
            return result['id'] if result else None
    except Exception as e:
        st.error(f"Error al obtener usuario ID: {e}")
        return None

def guardar_logo_usuario(usuario_email, logo_file):
    """Guarda el logo de un usuario localmente"""
    usuario_id = obtener_usuario_id(usuario_email)

    if not usuario_id:
        st.error("Usuario no encontrado")
        return None

    # Subir a almacenamiento local
    logo_path = upload_logo(logo_file, usuario_id, logo_file.name)

    if logo_path:
        st.success(f"✅ Logo subido correctamente")
        return logo_path
    else:
        st.error("❌ Error al subir el logo")
        return None

def guardar_documentos_anexos(usuario_email, archivos_subidos, categoria):
    """Guarda los documentos anexos de un usuario localmente"""
    if not archivos_subidos:
        return []

    usuario_id = obtener_usuario_id(usuario_email)

    if not usuario_id:
        st.error("Usuario no encontrado")
        return []

    documentos_guardados = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, archivo in enumerate(archivos_subidos):
        # Subir a almacenamiento local
        doc_path = upload_document(archivo, usuario_id, f"{categoria}_{timestamp}_{i}_{archivo.name}")

        if doc_path:
            documentos_guardados.append({
                'nombre': archivo.name,
                'categoria': categoria,
                'url': doc_path,
                'fecha_subida': datetime.now().strftime("%d/%m/%Y %H:%M"),
                'tamaño': len(archivo.getbuffer())
            })
        else:
            st.error(f"Error guardando {archivo.name}")

    return documentos_guardados

def generar_token_recuperacion(email):
    """Genera un token para recuperación de contraseña"""
    token = secrets.token_urlsafe(32)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tokens_recuperacion (email, token)
                VALUES (%s, %s)
            ''', (email, token))
            return token
    except Exception as e:
        st.error(f"Error al generar token: {e}")
        return None

def validar_token_recuperacion(email, token):
    """Valida un token de recuperación"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Calcular la fecha límite (1 hora atrás)
            fecha_limite = datetime.now() - timedelta(hours=1)

            cursor.execute('''
                SELECT id FROM tokens_recuperacion
                WHERE email = %s AND token = %s AND usado = FALSE
                AND fecha_creacion > %s
            ''', (email, token, fecha_limite))

            resultado = cursor.fetchone()
            return resultado is not None
    except Exception as e:
        st.error(f"Error al validar token: {e}")
        return False

def cambiar_password(email, nueva_password, token):
    """Cambia la contraseña usando un token válido"""
    if not validar_token_recuperacion(email, token):
        return False

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            password_hash = hashlib.sha256(nueva_password.encode()).hexdigest()

            # Actualizar contraseña
            cursor.execute('''
                UPDATE usuarios SET password = %s WHERE email = %s
            ''', (password_hash, email))

            # Marcar token como usado
            cursor.execute('''
                UPDATE tokens_recuperacion SET usado = TRUE WHERE email = %s AND token = %s
            ''', (email, token))

            return True
    except Exception as e:
        st.error(f"Error al cambiar contraseña: {e}")
        return False

def verificar_usuario(email, password):
    """Verifica las credenciales de un usuario"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM usuarios
                WHERE email = %s AND password = %s AND activo = TRUE
            ''', (email, password_hash))

            resultado = cursor.fetchone()
            return resultado is not None
    except Exception as e:
        st.error(f"Error al verificar usuario: {e}")
        return False

def obtener_usuario(email):
    """Obtiene los datos completos de un usuario"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM usuarios WHERE email = %s
            ''', (email,))

            resultado = cursor.fetchone()

            if resultado:
                return {
                    'id': resultado['id'],
                    'email': resultado['email'],
                    'nombre': resultado['nombre'],
                    'empresa': resultado['empresa'],
                    'telefono': resultado['telefono'],
                    'cif': resultado['cif'],
                    'direccion': resultado['direccion'],
                    'numero_cuenta': resultado['numero_cuenta'],
                    'rol': resultado['rol'],
                    'fecha_registro': resultado['fecha_registro'],
                    'activo': resultado['activo'],
                    'plan': resultado['plan'],
                    'fecha_expiracion': resultado['fecha_expiracion']
                }
            return None
    except Exception as e:
        st.error(f"Error al obtener usuario: {e}")
        return None

def listar_usuarios():
    """Lista todos los usuarios (para admin)"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, email, nombre, empresa, telefono, rol,
                       fecha_registro, activo, plan, fecha_expiracion
                FROM usuarios
                ORDER BY fecha_registro DESC
            ''')

            resultados = cursor.fetchall()

            usuarios = []
            for r in resultados:
                usuarios.append({
                    'id': r['id'],
                    'email': r['email'],
                    'nombre': r['nombre'],
                    'empresa': r['empresa'],
                    'telefono': r['telefono'],
                    'rol': r['rol'],
                    'fecha_registro': r['fecha_registro'],
                    'activo': r['activo'],
                    'plan': r['plan'],
                    'fecha_expiracion': r['fecha_expiracion']
                })

            return usuarios
    except Exception as e:
        st.error(f"Error al listar usuarios: {e}")
        return []

def actualizar_usuario(usuario_id, datos):
    """Actualiza los datos de un usuario"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE usuarios SET
                    nombre = %s, empresa = %s, telefono = %s,
                    activo = %s, plan = %s, fecha_expiracion = %s
                WHERE id = %s
            ''', (
                datos['nombre'],
                datos['empresa'],
                datos['telefono'],
                datos['activo'],
                datos['plan'],
                datos['fecha_expiracion'],
                usuario_id
            ))
            return True
    except Exception as e:
        st.error(f"Error al actualizar usuario: {e}")
        return False

def registrar_pago(usuario_id, importe, stripe_payment_id=None, plan='basico'):
    """Registra un pago en la base de datos"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pagos (usuario_id, stripe_payment_id, importe, estado, plan)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (usuario_id, stripe_payment_id, importe, 'completado', plan))

            result = cursor.fetchone()
            return result['id'] if result else None
    except Exception as e:
        st.error(f"Error al registrar pago: {e}")
        return None
