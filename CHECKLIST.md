# ✅ Checklist de Migración MEMOR.IA

## 📋 Pre-Migración

### Backup
- [ ] Ejecutar `python backup_sqlite.py` para hacer backup de datos actuales
- [ ] Guardar el archivo `backup_sqlite_YYYYMMDD_HHMMSS.json` en lugar seguro
- [ ] Hacer copia de seguridad de carpetas `logos_usuarios/` y `documentos_usuarios/`

### Archivos del Proyecto
- [ ] Verificar que existen todos estos archivos nuevos:
  - [ ] `db_helper.py`
  - [ ] `db_functions.py`
  - [ ] `storage_helper.py`
  - [ ] `database_schema.sql`
  - [ ] `backup_sqlite.py`
  - [ ] `migrate_code.py`
  - [ ] `.env.example`
- [ ] `requirements.txt` actualizado con psycopg2-binary y cloudinary

---

## 🔑 Configuración de Servicios

### Neon (PostgreSQL)
- [ ] Cuenta creada en https://neon.tech
- [ ] Proyecto creado (nombre: `memoria-ia`)
- [ ] `DATABASE_URL` copiada y guardada
- [ ] Tablas creadas usando `database_schema.sql` en SQL Editor
- [ ] Verificar que las 4 tablas existen: usuarios, perfiles_empresa, pagos, tokens_recuperacion

### Cloudinary
- [ ] Cuenta creada en https://cloudinary.com
- [ ] Credenciales copiadas:
  - [ ] `CLOUDINARY_CLOUD_NAME`
  - [ ] `CLOUDINARY_API_KEY`
  - [ ] `CLOUDINARY_API_SECRET`
- [ ] Verificar acceso al Dashboard

---

## 🌐 Configuración Local (Opcional para testing)

- [ ] Archivo `.env` creado (copiado de `.env.example`)
- [ ] Todas las variables completadas en `.env`:
  - [ ] `DATABASE_URL`
  - [ ] `CLOUDINARY_CLOUD_NAME`
  - [ ] `CLOUDINARY_API_KEY`
  - [ ] `CLOUDINARY_API_SECRET`
  - [ ] `ANTHROPIC_API_KEY`
  - [ ] `EMAIL_HOST`, `EMAIL_USER`, `EMAIL_PASSWORD`
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] Prueba local exitosa: `streamlit run memoria_tecnica_pro_v2.py`

---

## 🔧 Modificación del Código

### Imports
- [ ] Agregados imports al principio de `memoria_tecnica_pro_v2.py`:
```python
from db_helper import init_db_pool
from db_functions import *
from storage_helper import init_cloudinary
```

### Función init_database()
- [ ] Reemplazada función `init_database()` con:
```python
def init_database():
    init_db_pool()
    init_cloudinary()
```

### Funciones Antiguas
- [ ] Eliminadas o comentadas estas funciones (están en `db_functions.py`):
  - [ ] `registrar_usuario`
  - [ ] `obtener_perfil_empresa`
  - [ ] `guardar_perfil_empresa`
  - [ ] `guardar_logo_usuario`
  - [ ] `guardar_documentos_anexos`
  - [ ] `generar_token_recuperacion`
  - [ ] `validar_token_recuperacion`
  - [ ] `cambiar_password`

### Referencias a SQLite
- [ ] Buscar `sqlite3.connect` en el código (Ctrl+F)
- [ ] Todas las referencias eliminadas o comentadas
- [ ] No quedan llamadas directas a SQLite

---

## 🚀 Deploy en Streamlit Cloud

### Configuración de Secrets
- [ ] Ir a https://share.streamlit.io
- [ ] Seleccionar tu app → Settings → Secrets
- [ ] Agregar todas las variables:
```toml
DATABASE_URL = "postgresql://..."
CLOUDINARY_CLOUD_NAME = "..."
CLOUDINARY_API_KEY = "..."
CLOUDINARY_API_SECRET = "..."
ANTHROPIC_API_KEY = "..."
EMAIL_HOST = "..."
EMAIL_PORT = "465"
EMAIL_USER = "..."
EMAIL_PASSWORD = "..."
STRIPE_PUBLIC_KEY = "..."
STRIPE_SECRET_KEY = "..."
```
- [ ] Guardar secrets

### Subir Código a GitHub
- [ ] Todos los archivos nuevos agregados al repositorio
- [ ] `.gitignore` incluye `.env` y `*.db`
- [ ] Commit creado: "Migración a PostgreSQL + Cloudinary"
- [ ] Push a GitHub exitoso
- [ ] Deploy automático iniciado en Streamlit Cloud

---

## ✅ Verificación Post-Migración

### Testing en Streamlit Cloud
- [ ] App desplegada sin errores
- [ ] No aparecen errores en los logs
- [ ] Página de login carga correctamente

### Funcionalidad Básica
- [ ] ✅ Puedes acceder a la URL de la app
- [ ] ✅ Página de registro funciona
- [ ] ✅ Puedes crear un usuario nuevo
- [ ] ✅ Recibes la contraseña generada
- [ ] ✅ Puedes iniciar sesión con ese usuario
- [ ] ✅ Puedes subir un logo (se sube a Cloudinary)
- [ ] ✅ Puedes completar el perfil de empresa
- [ ] ✅ Los datos se guardan correctamente

### Persistencia
- [ ] Cierra y vuelve a abrir la app
- [ ] El usuario creado todavía existe
- [ ] Puedes iniciar sesión nuevamente
- [ ] El logo subido se muestra correctamente
- [ ] Los datos del perfil siguen ahí

### Funciones Avanzadas
- [ ] Recuperación de contraseña funciona
- [ ] Generación de memorias funciona
- [ ] Panel de administrador accesible (si aplica)
- [ ] Subida de documentos anexos funciona

---

## 🔄 Migración de Datos Existentes (Si aplica)

- [ ] Tienes el archivo de backup JSON
- [ ] Ejecutar: `python backup_sqlite.py restore backup_sqlite_XXXXXX.json`
- [ ] Verificar que usuarios se migraron correctamente
- [ ] Verificar que perfiles se migraron
- [ ] Verificar que pagos se migraron

---

## 🆘 Troubleshooting

### Si algo falla:
- [ ] Revisar logs en Streamlit Cloud (Settings → Logs)
- [ ] Verificar que todos los secrets están correctos
- [ ] Verificar que DATABASE_URL incluye `?sslmode=require`
- [ ] Probar conexión a Neon desde SQL Editor
- [ ] Probar subida a Cloudinary desde Dashboard
- [ ] Consultar `MIGRATION_GUIDE.md` para detalles

### Si los datos no persisten:
- [ ] Verificar que estás usando funciones de `db_functions.py`
- [ ] Verificar que `init_database()` llama a `init_db_pool()`
- [ ] Revisar que no quedan llamadas a `sqlite3.connect`
- [ ] Verificar que DATABASE_URL es correcta

---

## 🎉 ¡Completado!

Si todos los checkboxes están marcados, ¡tu migración está completa!

### Próximos Pasos
- [ ] Monitorear logs durante las primeras 24 horas
- [ ] Verificar que usuarios reales pueden registrarse
- [ ] Comprobar límites de uso en Neon y Cloudinary
- [ ] Considerar upgrade a plan de pago si es necesario

### Mantenimiento
- [ ] Backups automáticos de Neon están activos (por defecto)
- [ ] Revisar uso mensual de Cloudinary
- [ ] Mantener actualizado `requirements.txt`
- [ ] Revisar logs periódicamente

---

## 📊 Resumen

```
✅ Problema resuelto: Datos ahora persisten en la nube
✅ PostgreSQL configurado con Neon (gratis)
✅ Almacenamiento en Cloudinary (gratis)
✅ Aplicación lista para producción
✅ Sin cambios para los usuarios finales
```

---

**¿Todo funcionó? ¡Excelente! 🎉 Tu aplicación MEMOR.IA ahora es 100% productiva.**

**¿Algo falló?** Consulta `MIGRATION_GUIDE.md` o revisa los logs.
