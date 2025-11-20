# ⚡ Inicio Rápido - Migración a PostgreSQL

## 🎯 Pasos Rápidos (30 minutos)

### 1️⃣ Crear cuenta Neon (5 min)
1. Ve a https://neon.tech
2. Sign up → Create Project
3. Copia tu `DATABASE_URL`

### 2️⃣ Crear cuenta Cloudinary (5 min)
1. Ve a https://cloudinary.com
2. Sign up → Dashboard
3. Copia: `Cloud Name`, `API Key`, `API Secret`

### 3️⃣ Configurar Streamlit Secrets (5 min)
1. Ve a https://share.streamlit.io
2. Tu app → Settings → Secrets
3. Pega esto (con tus valores):

```toml
DATABASE_URL = "postgresql://..."
CLOUDINARY_CLOUD_NAME = "..."
CLOUDINARY_API_KEY = "..."
CLOUDINARY_API_SECRET = "..."

# Mantén tus secrets existentes
ANTHROPIC_API_KEY = "..."
EMAIL_HOST = "..."
EMAIL_PORT = "465"
EMAIL_USER = "..."
EMAIL_PASSWORD = "..."
```

### 4️⃣ Subir archivos nuevos (10 min)
Sube estos archivos a tu repositorio:
- `db_helper.py` ✅
- `db_functions.py` ✅
- `storage_helper.py` ✅
- `database_schema.sql` ✅
- `requirements.txt` (actualizado) ✅

### 5️⃣ Modificar código principal (5 min)

En `memoria_tecnica_pro_v2.py`, haz estos cambios:

#### A. Agregar imports (línea ~40, después de otros imports):
```python
from db_helper import init_db_pool
from db_functions import *
from storage_helper import init_cloudinary
```

#### B. Reemplazar `init_database()` (línea ~270):
```python
def init_database():
    """Inicializa la base de datos PostgreSQL"""
    try:
        init_db_pool()
        init_cloudinary()
    except Exception as e:
        st.error(f"❌ Error: {e}")
```

#### C. Eliminar funciones antiguas (líneas ~441-690):
Elimina estas funciones completas (ahora están en `db_functions.py`):
- `registrar_usuario`
- `obtener_perfil_empresa`
- `guardar_perfil_empresa`
- `guardar_logo_usuario`
- `guardar_documentos_anexos`
- `generar_token_recuperacion`
- `validar_token_recuperacion`
- `cambiar_password`

#### D. Buscar y comentar (Ctrl+F):
Busca: `sqlite3.connect`
Reemplaza con: `# MIGRADO A POSTGRESQL`

### 6️⃣ Deploy (5 min)
```bash
git add .
git commit -m "Migración a PostgreSQL + Cloudinary"
git push
```

Espera 2-5 minutos y ¡listo! 🎉

---

## 🆘 Si algo falla

1. **Revisa los logs** en Streamlit Cloud
2. **Verifica secrets** están bien escritos
3. **Consulta** `MIGRATION_GUIDE.md` para más detalles

---

## ✅ Verificación

Después del deploy, prueba:
- [ ] Registrar un usuario nuevo
- [ ] Iniciar sesión
- [ ] Subir un logo
- [ ] Cerrar y volver a abrir → datos siguen ahí

---

## 💡 Tip

Si prefieres probar localmente primero:
1. Copia `.env.example` a `.env`
2. Completa con tus credenciales
3. `pip install -r requirements.txt`
4. `streamlit run memoria_tecnica_pro_v2.py`

---

**¿Todo funcionó?** ¡Perfecto! Ahora tus datos persisten correctamente en Streamlit Cloud.
