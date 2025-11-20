# 🚀 MEMOR.IA - Despliegue en Servidor Dedicado Scaleway

## 🖥️ Configuración Inicial del Servidor

### 1. Conectar al servidor
```bash
ssh root@tu-ip-scaleway
```

### 2. Actualizar sistema (Ubuntu/Debian)
```bash
apt update && apt upgrade -y
```

### 3. Instalar dependencias base
```bash
# Python y pip
apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx -y

# Crear usuario para la aplicación
useradd -m -s /bin/bash memoria
```

## 📁 Preparar directorio de aplicación

```bash
# Cambiar a usuario memoria
su - memoria

# Crear directorio
mkdir -p /home/memoria/app
cd /home/memoria/app

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
```

## 📤 Subir archivos al servidor

### Opción A: SCP desde tu Mac
```bash
# Desde tu Mac, en el directorio /Users/macintosh/Desktop/memoria/
scp memoria_tecnica_pro_v2.py .env logo.png requirements.txt deploy.sh stop.sh README_SERVIDOR.md root@tu-ip-scaleway:/home/memoria/app/

# Cambiar permisos
ssh root@tu-ip-scaleway "chown -R memoria:memoria /home/memoria/app && chmod +x /home/memoria/app/*.sh"
```

### Opción B: Git (recomendado)
```bash
# En el servidor
git clone tu-repositorio
# O crear repo y hacer push desde tu Mac
```

## 🔧 Configuración de Nginx

```bash
# Como root, crear configuración
nano /etc/nginx/sites-available/memoria

# Contenido del archivo:
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;  # Cambia por tu dominio

    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    # Configuración SSL (se completará con certbot)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Archivos estáticos
    location /_stcore/static/ {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
    }

    # WebSocket para Streamlit
    location /_stcore/stream {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Seguridad adicional
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
}

# Activar sitio
ln -s /etc/nginx/sites-available/memoria /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

## 🔐 Configurar SSL con Let's Encrypt

```bash
# Obtener certificado SSL
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Configurar renovación automática
crontab -e
# Añadir línea:
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🎯 Desplegar la aplicación

```bash
# Como usuario memoria
su - memoria
cd /home/memoria/app
source venv/bin/activate

# Ejecutar deploy
./deploy.sh
```

## 🔄 Configurar como servicio systemd

```bash
# Como root, crear archivo de servicio
nano /etc/systemd/system/memoria.service

# Contenido:
[Unit]
Description=MEMOR.IA Streamlit App
After=network.target

[Service]
Type=simple
User=memoria
WorkingDirectory=/home/memoria/app
Environment=PATH=/home/memoria/app/venv/bin
ExecStart=/home/memoria/app/venv/bin/streamlit run memoria_tecnica_pro_v2.py --server.port=8501 --server.address=127.0.0.1 --server.headless=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Activar servicio
systemctl daemon-reload
systemctl enable memoria
systemctl start memoria
```

## 🔥 Configurar Firewall (UFW)

```bash
# Permitir puertos necesarios
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

# Verificar estado
ufw status
```

## 📊 Monitoreo

```bash
# Ver logs de la aplicación
journalctl -u memoria -f

# Ver logs de Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Estado del servicio
systemctl status memoria
```

## 🚀 Comandos útiles

```bash
# Reiniciar aplicación
systemctl restart memoria

# Detener aplicación
systemctl stop memoria

# Ver logs en tiempo real
journalctl -u memoria -f

# Actualizar aplicación
cd /home/memoria/app
git pull  # si usas git
systemctl restart memoria
```

## 🌐 DNS Configuration

En el panel de Scaleway:
1. Ve a "Domains and DNS"
2. Configura registro A: `tu-dominio.com` → `IP-de-tu-servidor`
3. Configura registro CNAME: `www.tu-dominio.com` → `tu-dominio.com`

## 💡 Optimizaciones para Producción

```bash
# Instalar supervisor como alternativa
apt install supervisor

# Configurar límites de memoria
# En /etc/systemd/system/memoria.service añadir:
MemoryMax=2G
MemoryHigh=1.5G
```

## 🆘 Troubleshooting

```bash
# Si la aplicación no carga:
systemctl status memoria
journalctl -u memoria --no-pager -l

# Si hay problemas de conexión:
nginx -t
systemctl status nginx

# Si hay problemas de SSL:
certbot certificates
certbot renew --dry-run
```

¡Tu aplicación estará disponible en https://tu-dominio.com!