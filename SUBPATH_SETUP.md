# 🌐 MEMOR.IA en oclemcertificacion.com/memor-ia

## 📋 Configuración para Subpath

MEMOR.IA estará disponible en: **https://oclemcertificacion.com/memor-ia**

## 🚀 Pasos de Instalación Completos

### 1️⃣ **Subir archivos**
```bash
# Editar upload_to_scaleway.sh con la IP real
nano upload_to_scaleway.sh
# Cambiar TU_IP_SCALEWAY por la IP de oclemcertificacion.com

# Ejecutar subida
./upload_to_scaleway.sh
```

### 2️⃣ **Configurar Nginx**

#### Opción A: Archivo separado (recomendado)
```bash
# Como root en el servidor
ssh root@tu-ip

# Copiar configuración
cp /home/memoria/app/nginx_memor-ia.conf /etc/nginx/sites-available/memor-ia

# Activar
ln -s /etc/nginx/sites-available/memor-ia /etc/nginx/sites-enabled/

# Verificar y recargar
nginx -t
systemctl reload nginx
```

#### Opción B: Integrar en configuración existente
```bash
# Editar tu archivo de configuración existente
nano /etc/nginx/sites-available/oclemcertificacion

# Agregar las secciones de location /memor-ia/ del archivo nginx_memor-ia.conf
# dentro de tu bloque server existente

# Recargar Nginx
nginx -t && systemctl reload nginx
```

### 3️⃣ **Configurar Systemd**
```bash
# Como root
cp /home/memoria/app/systemd_memor-ia.service /etc/systemd/system/memor-ia.service
systemctl daemon-reload
systemctl enable memor-ia
```

### 4️⃣ **Configurar aplicación**
```bash
# Cambiar a usuario memoria
su - memoria
cd /home/memoria/app

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Desplegar aplicación
./deploy.sh
```

### 5️⃣ **Iniciar servicio**
```bash
# Como root
systemctl start memor-ia
systemctl status memor-ia
```

## 🔧 Configuraciones Específicas

### Variables de entorno para subpath:
```bash
STREAMLIT_SERVER_BASE_URL_PATH=/memor-ia
```

### Parámetros de Streamlit:
```bash
--server.baseUrlPath=/memor-ia
--server.port=8501
--server.address=127.0.0.1
```

### Configuración de Nginx:
- **Proxy a:** `http://127.0.0.1:8501/`
- **Location:** `/memor-ia/`
- **WebSocket:** `/memor-ia/_stcore/stream`
- **Archivos estáticos:** `/memor-ia/_stcore/`

## 🎯 Resultado Final

✅ **URL de acceso:** https://oclemcertificacion.com/memor-ia
✅ **Login admin:** vmendez@oclem.com / favorito1998
✅ **Certificados SSL:** Compartidos con dominio principal
✅ **Logs:** `journalctl -u memor-ia -f`

## 🔍 Verificación

### Comprobar servicio:
```bash
systemctl status memor-ia
curl -I https://oclemcertificacion.com/memor-ia
```

### Ver logs:
```bash
journalctl -u memor-ia -f
tail -f /home/memoria/app/logs/app.log
```

### Test de conectividad:
```bash
curl http://127.0.0.1:8501/healthz
```

## 🆘 Troubleshooting

### Si no carga la aplicación:
1. `systemctl status memor-ia`
2. `journalctl -u memor-ia --no-pager -l`
3. `nginx -t`
4. `curl -I http://127.0.0.1:8501`

### Si hay errores de ruta:
1. Verificar `STREAMLIT_SERVER_BASE_URL_PATH`
2. Verificar configuración Nginx
3. Limpiar caché del navegador

### Si los assets no cargan:
1. Verificar location `/_stcore/`
2. Verificar WebSocket connection
3. Revisar headers de proxy

## 📊 Monitoreo

```bash
# Estado del servicio
systemctl status memor-ia

# Logs en tiempo real
journalctl -u memor-ia -f

# Uso de recursos
htop -p $(pgrep -f streamlit)

# Conexiones
netstat -tlnp | grep 8501
```

¡MEMOR.IA estará funcionando perfectamente en tu subpath!