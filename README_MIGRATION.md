# 🧠 MEMOR.IA - Migración a PostgreSQL + Cloudinary

## 📌 Resumen del Problema

Tu aplicación en Streamlit Cloud **no guardaba datos ni usuarios** porque:

- ❌ **SQLite local** → Los archivos `.db` se borran en cada reinicio
- ❌ **Archivos locales** → Logos y documentos desaparecen
- ❌ **Rutas hardcodeadas** → `/Users/macintosh/Desktop/...` no existen en la nube

## ✅ Solución Implementada

### Arquitectura Nueva (100% Gratis)

```
┌─────────────────────┐
│  Streamlit Cloud    │
│  (Frontend + App)   │
└──────────┬──────────┘
           │
           ├──────────────────┐
           │                  │
    ┌──────▼─────┐     ┌─────▼──────┐
    │   Neon     │     │ Cloudinary │
    │ PostgreSQL │     │  Storage   │
    │  (10 GB)   │     │  (25 GB)   │
    └────────────┘     └────────────┘
    Usuarios/Datos     Logos/Docs
```

### Componentes Creados

| Archivo | Descripción |
|---------|-------------|
| `db_helper.py` | Gestión de conexiones a PostgreSQL |
| `db_functions.py` | Funciones de BD migradas de SQLite |
| `storage_helper.py` | Manejo de archivos en Cloudinary |
| `database_schema.sql` | Schema de tablas PostgreSQL |
| `migrate_code.py` | Script de migración automática |
| `requirements.txt` | Dependencias actualizadas |
| `.env.example` | Plantilla de variables de entorno |

## 🚀 Cómo Aplicar la Migración

### Opción 1: Inicio Rápido (Recomendada)
Sigue el archivo **`QUICK_START.md`** → 30 minutos

### Opción 2: Guía Completa
Consulta **`MIGRATION_GUIDE.md`** → Paso a paso detallado

## 📦 Archivos del Proyecto

```
MEMOR_IA/
├── memoria_tecnica_pro_v2.py      # App principal (necesita modificación)
├── plantillas_memoria.py          # Plantillas (sin cambios)
│
├── db_helper.py                   # ✨ NUEVO - Conexión PostgreSQL
├── db_functions.py                # ✨ NUEVO - Funciones de BD
├── storage_helper.py              # ✨ NUEVO - Almacenamiento
│
├── database_schema.sql            # ✨ NUEVO - Schema SQL
├── migrate_code.py                # ✨ NUEVO - Script migración
│
├── requirements.txt               # ✅ ACTUALIZADO
├── .env                          # Tus credenciales (no subir a Git)
├── .env.example                  # ✨ NUEVO - Plantilla
│
├── MIGRATION_GUIDE.md            # 📚 Guía completa
├── QUICK_START.md                # ⚡ Inicio rápido
└── README_MIGRATION.md           # 📄 Este archivo
```

## 🔑 Variables de Entorno Necesarias

Configura estas variables en **Streamlit Secrets** y en tu `.env` local:

```toml
# PostgreSQL (Neon)
DATABASE_URL = "postgresql://..."

# Cloudinary
CLOUDINARY_CLOUD_NAME = "..."
CLOUDINARY_API_KEY = "..."
CLOUDINARY_API_SECRET = "..."

# Existentes (mantener)
ANTHROPIC_API_KEY = "..."
EMAIL_HOST = "..."
EMAIL_USER = "..."
EMAIL_PASSWORD = "..."
```

## 📊 Cambios en el Código Principal

### Antes (SQLite)
```python
import sqlite3

def init_database():
    conn = sqlite3.connect('memoria_usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE usuarios...''')
    conn.commit()
    conn.close()

def registrar_usuario(datos):
    conn = sqlite3.connect('memoria_usuarios.db')
    # ... código SQLite
    conn.close()
```

### Después (PostgreSQL)
```python
from db_helper import init_db_pool
from db_functions import *
from storage_helper import init_cloudinary

def init_database():
    init_db_pool()
    init_cloudinary()

# Las funciones de BD ahora están en db_functions.py
# Ya no necesitas definir registrar_usuario aquí
```

## 🎯 Ventajas de la Nueva Arquitectura

| Característica | SQLite Local | PostgreSQL + Cloudinary |
|---------------|--------------|------------------------|
| Persistencia | ❌ Temporal | ✅ Permanente |
| Archivos | ❌ Se pierden | ✅ En la nube |
| Escalabilidad | ❌ Limitada | ✅ Ilimitada |
| Concurrencia | ⚠️ Limitada | ✅ Múltiples usuarios |
| Backups | ❌ Manual | ✅ Automático |
| Costo | ✅ Gratis | ✅ Gratis |

## 🧪 Testing

### Local
```bash
# 1. Configurar .env con tus credenciales
cp .env.example .env
# Edita .env con tus valores

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
streamlit run memoria_tecnica_pro_v2.py
```

### Producción (Streamlit Cloud)
1. Configura Secrets en Streamlit Cloud
2. Sube el código a GitHub
3. Deploy automático
4. Verifica que funcione

## 🐛 Troubleshooting

### Error: "DATABASE_URL not found"
→ Configura el secret en Streamlit Cloud

### Error: "Cloudinary not configured"
→ Verifica las credenciales de Cloudinary

### Los datos se siguen perdiendo
→ Asegúrate de usar las funciones de `db_functions.py`

### Errores de importación
→ Verifica que todos los archivos estén en el mismo directorio

## 📈 Límites de los Planes Gratuitos

### Neon (PostgreSQL)
- ✅ 10 GB de almacenamiento
- ✅ 100 horas de compute/mes
- ✅ Suficiente para ~100,000 usuarios

### Cloudinary
- ✅ 25 GB de almacenamiento
- ✅ 25 GB de ancho de banda/mes
- ✅ Suficiente para ~25,000 imágenes

## 🔒 Seguridad

- ✅ Conexiones SSL/TLS
- ✅ Passwords hasheados (SHA-256)
- ✅ Variables sensibles en secrets
- ✅ No hay archivos locales

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs** en Streamlit Cloud
2. **Consulta** `MIGRATION_GUIDE.md`
3. **Verifica** las credenciales en Secrets
4. **Prueba localmente** primero

## 🎓 Recursos Adicionales

- [Documentación de Neon](https://neon.tech/docs)
- [Documentación de Cloudinary](https://cloudinary.com/documentation)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [PostgreSQL con psycopg2](https://www.psycopg.org/docs/)

## ✨ Próximos Pasos

1. ✅ Migrar a PostgreSQL + Cloudinary
2. 🔄 Migrar datos existentes (si aplica)
3. 🧪 Testing completo
4. 🚀 Deploy a producción
5. 📊 Monitorear performance

## 📝 Notas Finales

- **Tiempo estimado de migración**: 30-60 minutos
- **Dificultad**: Media
- **Reversible**: Sí (mantén backup de SQLite)
- **Impacto en usuarios**: Ninguno (si se hace correctamente)

---

**¡Tu aplicación MEMOR.IA estará lista para producción! 🎉**

Para comenzar, abre **`QUICK_START.md`** y sigue los pasos.
