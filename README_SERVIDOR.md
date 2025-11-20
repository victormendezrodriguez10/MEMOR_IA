# MEMOR.IA - Instalación en Servidor

## 📋 Requisitos del Servidor

- **Python 3.8+**
- **Conexión a Internet**
- **SSL/HTTPS recomendado**
- **Dominio propio**

## 🚀 Instalación

### 1. Subir archivos al servidor
```bash
# Archivos necesarios:
- memoria_tecnica_pro_v2.py
- .env
- logo.png
- requirements.txt
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno (.env)
```bash
ANTHROPIC_API_KEY=tu_clave_anthropic
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=notificacionesconcurso@oclem.com
EMAIL_PASSWORD=N0t1f1c4c1on35*
```

### 4. Ejecutar aplicación

#### Opción A: Desarrollo/Testing
```bash
streamlit run memoria_tecnica_pro_v2.py --server.port=8501
```

#### Opción B: Producción con Nginx
```bash
# Ejecutar en background
nohup streamlit run memoria_tecnica_pro_v2.py --server.port=8501 --server.headless=true > app.log 2>&1 &
```

### 5. Configuración Nginx (recomendado)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## 🔐 Configuración SSL (HTTPS)
```bash
# Con Let's Encrypt
sudo certbot --nginx -d tu-dominio.com
```

## 💾 Base de Datos
- Se crea automáticamente: `memoria_usuarios.db`
- Logos de usuarios: `logos_usuarios/`

## 🔧 Variables importantes
- **Puerto por defecto:** 8501
- **Logs:** app.log
- **Datos:** Se guardan localmente en SQLite

## 📞 Soporte
- Email: vmendez@oclem.com
- Sistema completo operativo