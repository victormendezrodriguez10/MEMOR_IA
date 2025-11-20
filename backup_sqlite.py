"""
backup_sqlite.py
Script para hacer backup de la base de datos SQLite antes de migrar
"""

import sqlite3
import json
import os
from datetime import datetime

def backup_sqlite_to_json():
    """Exporta toda la base de datos SQLite a JSON"""

    db_path = 'memoria_usuarios.db'

    if not os.path.exists(db_path):
        print("❌ No se encontró memoria_usuarios.db")
        print("   Si ya migraste, no necesitas hacer backup.")
        return

    print("📦 Haciendo backup de SQLite...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    backup_data = {
        'fecha_backup': datetime.now().isoformat(),
        'usuarios': [],
        'perfiles_empresa': [],
        'pagos': [],
        'tokens_recuperacion': []
    }

    # Backup usuarios
    print("   → Exportando usuarios...")
    cursor.execute("SELECT * FROM usuarios")
    columns = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        usuario = dict(zip(columns, row))
        backup_data['usuarios'].append(usuario)

    # Backup perfiles_empresa
    print("   → Exportando perfiles de empresa...")
    cursor.execute("SELECT * FROM perfiles_empresa")
    columns = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        perfil = dict(zip(columns, row))
        backup_data['perfiles_empresa'].append(perfil)

    # Backup pagos
    print("   → Exportando pagos...")
    cursor.execute("SELECT * FROM pagos")
    columns = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        pago = dict(zip(columns, row))
        backup_data['pagos'].append(pago)

    # Backup tokens
    print("   → Exportando tokens...")
    cursor.execute("SELECT * FROM tokens_recuperacion")
    columns = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        token = dict(zip(columns, row))
        backup_data['tokens_recuperacion'].append(token)

    conn.close()

    # Guardar a JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_sqlite_{timestamp}.json"

    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n✅ Backup completado: {backup_filename}")
    print(f"\n📊 Estadísticas:")
    print(f"   - Usuarios: {len(backup_data['usuarios'])}")
    print(f"   - Perfiles: {len(backup_data['perfiles_empresa'])}")
    print(f"   - Pagos: {len(backup_data['pagos'])}")
    print(f"   - Tokens: {len(backup_data['tokens_recuperacion'])}")
    print(f"\n💡 Guarda este archivo antes de migrar a PostgreSQL")

def restore_from_json_to_postgresql(backup_file):
    """Restaura datos del backup JSON a PostgreSQL"""

    if not os.path.exists(backup_file):
        print(f"❌ No se encontró el archivo: {backup_file}")
        return

    print(f"📥 Restaurando desde {backup_file}...")

    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_data = json.load(f)

    # Importar las funciones de PostgreSQL
    try:
        from db_helper import get_db_connection
    except ImportError:
        print("❌ Error: Asegúrate de tener db_helper.py en el directorio")
        return

    print("   → Restaurando usuarios...")
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            for usuario in backup_data['usuarios']:
                try:
                    cursor.execute('''
                        INSERT INTO usuarios
                        (email, password, nombre, empresa, telefono, cif, direccion,
                         numero_cuenta, rol, fecha_registro, activo, plan, fecha_expiracion)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO NOTHING
                    ''', (
                        usuario['email'], usuario['password'], usuario['nombre'],
                        usuario['empresa'], usuario.get('telefono'), usuario.get('cif'),
                        usuario.get('direccion'), usuario.get('numero_cuenta'),
                        usuario.get('rol', 'Usuario'), usuario.get('fecha_registro'),
                        usuario.get('activo', True), usuario.get('plan', 'basico'),
                        usuario.get('fecha_expiracion')
                    ))
                except Exception as e:
                    print(f"   ⚠️  Error con usuario {usuario['email']}: {e}")

            conn.commit()

    print("   → Restaurando perfiles...")
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            for perfil in backup_data['perfiles_empresa']:
                try:
                    cursor.execute('''
                        INSERT INTO perfiles_empresa
                        (usuario_id, sector, empleados, experiencia_anos, certificaciones,
                         otras_certificaciones, experiencia_similar, logo_path,
                         medios_materiales, herramientas_software, equipo_tecnico)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (usuario_id) DO NOTHING
                    ''', (
                        perfil['usuario_id'], perfil.get('sector'), perfil.get('empleados'),
                        perfil.get('experiencia_anos'), perfil.get('certificaciones'),
                        perfil.get('otras_certificaciones'), perfil.get('experiencia_similar'),
                        perfil.get('logo_path'), perfil.get('medios_materiales'),
                        perfil.get('herramientas_software'), perfil.get('equipo_tecnico')
                    ))
                except Exception as e:
                    print(f"   ⚠️  Error con perfil: {e}")

            conn.commit()

    print("   → Restaurando pagos...")
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            for pago in backup_data['pagos']:
                try:
                    cursor.execute('''
                        INSERT INTO pagos
                        (usuario_id, stripe_payment_id, importe, fecha_pago, estado, plan)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (
                        pago['usuario_id'], pago.get('stripe_payment_id'),
                        pago['importe'], pago.get('fecha_pago'),
                        pago.get('estado', 'pendiente'), pago.get('plan')
                    ))
                except Exception as e:
                    print(f"   ⚠️  Error con pago: {e}")

            conn.commit()

    print(f"\n✅ Restauración completada")
    print(f"   - Usuarios restaurados: {len(backup_data['usuarios'])}")
    print(f"   - Perfiles restaurados: {len(backup_data['perfiles_empresa'])}")
    print(f"   - Pagos restaurados: {len(backup_data['pagos'])}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        # Modo restauración
        if len(sys.argv) < 3:
            print("Uso: python backup_sqlite.py restore <archivo_backup.json>")
        else:
            restore_from_json_to_postgresql(sys.argv[2])
    else:
        # Modo backup (por defecto)
        backup_sqlite_to_json()
        print("\n💡 Para restaurar en PostgreSQL, ejecuta:")
        print("   python backup_sqlite.py restore <archivo_backup.json>")
