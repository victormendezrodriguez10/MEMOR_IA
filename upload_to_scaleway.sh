#!/bin/bash

# Script para subir MEMOR.IA a servidor Scaleway
echo "📤 Subiendo MEMOR.IA a Scaleway..."

# Configuración para oclemcertificacion.com
SERVER_IP="195.154.137.88"  # IP de oclemcertificacion.com
SERVER_USER="root"
APP_DIR="/home/memoria/app"
DOMAIN="oclemcertificacion.com"

# Verificar que se proporcionó la IP
if [ "$SERVER_IP" == "TU_IP_SCALEWAY" ]; then
    echo "❌ Error: Debes cambiar TU_IP_SCALEWAY por la IP real de tu servidor"
    echo "Edita este archivo y cambia la variable SERVER_IP"
    exit 1
fi

echo "🎯 Servidor destino: $SERVER_USER@$SERVER_IP:$APP_DIR"

# Crear directorio en el servidor
echo "📁 Creando estructura de directorios..."
ssh $SERVER_USER@$SERVER_IP "mkdir -p $APP_DIR && chown -R memoria:memoria /home/memoria"

# Subir archivos principales
echo "📤 Subiendo archivos de aplicación..."
scp memoria_tecnica_pro_v2.py $SERVER_USER@$SERVER_IP:$APP_DIR/
scp .env $SERVER_USER@$SERVER_IP:$APP_DIR/
scp logo.png $SERVER_USER@$SERVER_IP:$APP_DIR/
scp requirements.txt $SERVER_USER@$SERVER_IP:$APP_DIR/
scp deploy.sh $SERVER_USER@$SERVER_IP:$APP_DIR/
scp stop.sh $SERVER_USER@$SERVER_IP:$APP_DIR/
scp SCALEWAY_DEPLOY.md $SERVER_USER@$SERVER_IP:$APP_DIR/
scp nginx_memor-ia.conf $SERVER_USER@$SERVER_IP:$APP_DIR/
scp systemd_memor-ia.service $SERVER_USER@$SERVER_IP:$APP_DIR/

# Establecer permisos correctos
echo "🔧 Configurando permisos..."
ssh $SERVER_USER@$SERVER_IP "
    chown -R memoria:memoria $APP_DIR
    chmod +x $APP_DIR/deploy.sh
    chmod +x $APP_DIR/stop.sh
    chmod 600 $APP_DIR/.env
"

echo "✅ Archivos subidos correctamente a $DOMAIN"
echo ""
echo "📋 Próximos pasos para configurar en /memor-ia:"
echo "1. Conéctate al servidor: ssh $SERVER_USER@$SERVER_IP"
echo "2. Configura Nginx:"
echo "   cp $APP_DIR/nginx_memor-ia.conf /etc/nginx/sites-available/memor-ia"
echo "   # O integra el contenido en tu configuración existente"
echo "3. Configura systemd:"
echo "   cp $APP_DIR/systemd_memor-ia.service /etc/systemd/system/memor-ia.service"
echo "   systemctl daemon-reload"
echo "4. Cambia al usuario memoria: su - memoria"
echo "5. Ve al directorio: cd $APP_DIR"
echo "6. Crea entorno virtual: python3 -m venv venv && source venv/bin/activate"
echo "7. Ejecuta despliegue: ./deploy.sh"
echo "8. Habilita servicio: systemctl enable memor-ia && systemctl start memor-ia"
echo ""
echo "🌐 MEMOR.IA estará disponible en: https://$DOMAIN/memor-ia"