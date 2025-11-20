# 🚀 Guía de Migración a PostgreSQL + Cloudinary

Esta guía te ayudará a migrar tu aplicación MEMOR.IA de SQLite local a PostgreSQL + Cloudinary para que funcione correctamente en Streamlit Cloud.

## 📋 Tabla de Contenidos

1. [¿Por qué migrar?](#por-qué-migrar)
2. [Servicios gratuitos necesarios](#servicios-gratuitos-necesarios)
3. [Configuración de Neon (PostgreSQL)](#configuración-de-neon)
4. [Configuración de Cloudinary](#configuración-de-cloudinary)
5. [Configuración de Streamlit Cloud](#configuración-de-streamlit-cloud)
6. [Aplicar la migración](#aplicar-la-migración)
7. [Verificación](#verificación)

---

## 🤔 ¿Por qué migrar?

Streamlit Cloud usa un filesystem **efímero** que se reinicia frecuentemente. Esto significa que:

- ❌ **SQLite local**: Los datos se pierden en cada reinicio
- ❌ **Archivos locales**: Logos y documentos desaparecen
- ✅ **PostgreSQL**: Base de datos persistente en la nube
- ✅ **Cloudinary**: Almacenamiento permanente de archivos

---

## 🆓 Servicios Gratuitos Necesarios

### 1. Neon (PostgreSQL)
- **Plan gratuito**: 10 GB de almacenamiento
- **URL**: https://neon.tech
- **Incluye**: Base de datos PostgreSQL completa

### 2. Cloudinary (Almacenamiento)
- **Plan gratuito**: 25 GB de almacenamiento
- **URL**: https://cloudinary.com
- **Incluye**: Almacenamiento de imágenes y documentos

---

## 🗄️ Configuración de Neon (PostgreSQL)

### Paso 1: Crear cuenta en Neon

1. Ve a https://neon.tech
2. Haz clic en **"Sign Up"**
3. Regístrate con GitHub o Google
4. Verifica tu email

### Paso 2: Crear un proyecto

1. En el dashboard, haz clic en **"Create a project"**
2. Nombre del proyecto: `memoria-ia`
3. Región: Selecciona la más cercana (ej: Frankfurt para Europa)
4. Haz clic en **"Create Project"**

### Paso 3: Obtener la DATABASE_URL

1. En tu proyecto, ve a **"Connection Details"**
2. Selecciona **"Pooled connection"**
3. Copia la **Connection string** (debería verse así):
   ```
   postgresql://usuario:password@ep-xxxx-xxxx.eu-central-1.aws.neon.tech/neondb?sslmode=require
   ```
4. **GUARDA ESTA URL**, la necesitarás más adelante

### Paso 4: Crear las tablas

1. En Neon, ve a **"SQL Editor"**
2. Copia y pega el contenido del archivo `database_schema.sql`
3. Haz clic en **"Run"**
4. Verifica que las tablas se crearon correctamente

---

## ☁️ Configuración de Cloudinary

### Paso 1: Crear cuenta

1. Ve a https://cloudinary.com
2. Haz clic en **"Sign Up Free"**
3. Completa el formulario de registro
4. Verifica tu email

### Paso 2: Obtener credenciales

1. Inicia sesión en Cloudinary
2. Ve al **Dashboard**
3. Encontrarás tus credenciales:
   - **Cloud Name**: ej. `dxxxxxx`
   - **API Key**: ej. `123456789012345`
   - **API Secret**: ej. `aBcDeFgHiJkLmNoPqRsTuVwXyZ`
4. **GUARDA ESTAS CREDENCIALES**, las necesitarás más adelante

---

## 🌐 Configuración de Streamlit Cloud

### Paso 1: Subir código a GitHub

1. Ve a tu repositorio de GitHub
2. Asegúrate de tener todos los archivos nuevos:
   - `db_helper.py`
   - `db_functions.py`
   - `storage_helper.py`
   - `requirements.txt` (actualizado)
   - `memoria_tecnica_pro_v2.py` (migrado)

### Paso 2: Configurar Secrets

1. Ve a https://share.streamlit.io
2. Selecciona tu aplicación
3. Ve a **"Settings" → "Secrets"**
4. Agrega las siguientes variables:

```toml
# PostgreSQL (Neon)
DATABASE_URL = "postgresql://usuario:password@ep-xxxx-xxxx.eu-central-1.aws.neon.tech/neondb?sslmode=require"

# Cloudinary
CLOUDINARY_CLOUD_NAME = "tu_cloud_name"
CLOUDINARY_API_KEY = "tu_api_key"
CLOUDINARY_API_SECRET = "tu_api_secret"

# Variables existentes (mantener)
ANTHROPIC_API_KEY = "tu_api_key"
EMAIL_HOST = "tu_host"
EMAIL_PORT = "465"
EMAIL_USER = "tu_email"
EMAIL_PASSWORD = "tu_password"
STRIPE_PUBLIC_KEY = "tu_stripe_key"
STRIPE_SECRET_KEY = "tu_stripe_secret"
```

5. Haz clic en **"Save"**

---

## 🔧 Aplicar la Migración

### Opción A: Migración Automática (Recomendada)

1. **Ejecuta el script de migración**:
   ```bash
   cd /Users/macintosh/Desktop/MEMOR_IA
   python migrate_code.py
   ```

2. **Revisa el archivo generado**:
   - Se creará `memoria_tecnica_pro_v2_postgresql.py`
   - Revisa que todo esté correcto
   - Busca comentarios con `# TODO` que requieran ajustes manuales

3. **Renombra el archivo**:
   ```bash
   mv memoria_tecnica_pro_v2.py memoria_tecnica_pro_v2_OLD.py
   mv memoria_tecnica_pro_v2_postgresql.py memoria_tecnica_pro_v2.py
   ```

### Opción B: Migración Manual

Si prefieres hacerlo manualmente:

1. **Actualizar imports en `memoria_tecnica_pro_v2.py`**:

   ```python
   # Agregar después de los imports existentes:
   from db_helper import get_db_connection, init_db_pool
   from db_functions import (
       registrar_usuario, obtener_perfil_empresa, guardar_perfil_empresa,
       guardar_logo_usuario, guardar_documentos_anexos,
       generar_token_recuperacion, validar_token_recuperacion, cambiar_password,
       verificar_usuario, obtener_usuario, listar_usuarios, actualizar_usuario,
       registrar_pago
   )
   from storage_helper import init_cloudinary
   ```

2. **Reemplazar `init_database()`**:

   ```python
   def init_database():
       """Inicializa la base de datos PostgreSQL"""
       try:
           init_db_pool()
           init_cloudinary()
       except Exception as e:
           st.error(f"❌ Error al inicializar: {e}")
   ```

3. **Eliminar las funciones antiguas** de base de datos (están ahora en `db_functions.py`):
   - `registrar_usuario`
   - `obtener_perfil_empresa`
   - `guardar_perfil_empresa`
   - `guardar_logo_usuario`
   - `guardar_documentos_anexos`
   - `generar_token_recuperacion`
   - `validar_token_recuperacion`
   - `cambiar_password`

4. **Buscar y reemplazar** en todo el archivo:
   - Buscar: `sqlite3.connect('memoria_usuarios.db')`
   - Reemplazar con llamadas a funciones de `db_functions.py`

---

## ✅ Verificación

### Prueba Local

1. **Configura variables de entorno locales**:
   ```bash
   # En tu archivo .env
   DATABASE_URL=postgresql://...
   CLOUDINARY_CLOUD_NAME=...
   CLOUDINARY_API_KEY=...
   CLOUDINARY_API_SECRET=...
   ```

2. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**:
   ```bash
   streamlit run memoria_tecnica_pro_v2.py
   ```

4. **Verifica**:
   - ✅ La aplicación inicia sin errores
   - ✅ Puedes registrar un usuario nuevo
   - ✅ Puedes iniciar sesión
   - ✅ Puedes subir un logo
   - ✅ Los datos persisten (cierra y vuelve a abrir)

### Prueba en Streamlit Cloud

1. **Sube los cambios a GitHub**:
   ```bash
   git add .
   git commit -m "Migración a PostgreSQL + Cloudinary"
   git push
   ```

2. **Espera el deploy** en Streamlit Cloud (2-5 minutos)

3. **Verifica en producción**:
   - ✅ La aplicación funciona
   - ✅ Puedes crear usuarios
   - ✅ Los datos persisten después de reinicios
   - ✅ Los logos se guardan correctamente

---

## 🆘 Solución de Problemas

### Error: "DATABASE_URL not found"
- **Solución**: Verifica que hayas configurado el secret `DATABASE_URL` en Streamlit Cloud

### Error: "Cloudinary not configured"
- **Solución**: Verifica las credenciales de Cloudinary en Streamlit Secrets

### Error: "connection refused"
- **Solución**: Verifica que la URL de Neon sea correcta y que el proyecto esté activo

### Error: "SSL required"
- **Solución**: Asegúrate de que la URL de Neon incluya `?sslmode=require`

### Los logos no se muestran
- **Solución**: Verifica que Cloudinary esté configurado correctamente y que los archivos se estén subiendo

---

## 📊 Comparación

| Característica | Antes (SQLite) | Después (PostgreSQL) |
|---------------|---------------|---------------------|
| **Persistencia** | ❌ Se pierde | ✅ Permanente |
| **Archivos** | ❌ Se pierden | ✅ En Cloudinary |
| **Escalabilidad** | ❌ Limitada | ✅ Ilimitada |
| **Costo** | ✅ Gratis | ✅ Gratis |
| **Performance** | ⚠️ Limitado | ✅ Óptimo |

---

## 📝 Notas Adicionales

- **Límites Neon gratuito**: 10 GB, suficiente para ~100,000 usuarios
- **Límites Cloudinary gratuito**: 25 GB, ~25,000 imágenes
- **Backups**: Neon hace backups automáticos
- **Seguridad**: Todas las conexiones usan SSL/TLS

---

## 🎉 ¡Listo!

Tu aplicación MEMOR.IA ahora está completamente migrada y funcionará correctamente en Streamlit Cloud con datos persistentes.

Si tienes algún problema, revisa los logs en Streamlit Cloud o contacta al soporte.

**¡Buena suerte! 🚀**
