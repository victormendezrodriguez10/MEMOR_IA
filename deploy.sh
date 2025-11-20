#!/bin/bash

# Script de despliegue para MEMOR.IA en Scaleway
echo "🚀 Desplegando MEMOR.IA en Scaleway..."

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Matar procesos anteriores de Streamlit
echo "⏹️ Deteniendo procesos anteriores..."
pkill -f "streamlit run memoria_tecnica_pro_v2.py" || true

# Esperar un momento
sleep 2

# Crear directorio para logos de usuarios
mkdir -p logos_usuarios

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Verificar que el archivo .env existe
if [ ! -f .env ]; then
    echo "❌ Error: Archivo .env no encontrado"
    echo "Crea el archivo .env con las configuraciones necesarias"
    exit 1
fi

# Verificar permisos de directorio
chmod 755 logos_usuarios
chmod 755 logs

# Ejecutar aplicación para Scaleway en subpath /memor-ia
echo "🎯 Iniciando MEMOR.IA en oclemcertificacion.com/memor-ia..."
export STREAMLIT_SERVER_BASE_URL_PATH="/memor-ia"
nohup streamlit run memoria_tecnica_pro_v2.py \
    --server.port=8501 \
    --server.address=127.0.0.1 \
    --server.headless=true \
    --server.baseUrlPath="/memor-ia" \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --server.maxUploadSize=200 \
    > logs/app.log 2>&1 &

# Guardar PID
echo $! > logs/streamlit.pid

echo "✅ MEMOR.IA desplegado correctamente en Scaleway"
echo "🏠 Servidor: 127.0.0.1:8501 (detrás de Nginx)"
echo "📝 Logs: logs/app.log"
echo "🔄 PID: $(cat logs/streamlit.pid)"

# Mostrar estado
sleep 3
if ps -p $(cat logs/streamlit.pid) > /dev/null; then
    echo "🟢 Aplicación ejecutándose correctamente"
    echo "🌐 Accede via tu dominio configurado con Nginx"
else
    echo "🔴 Error en el despliegue. Revisa logs/app.log"
    echo "📋 Últimas líneas del log:"
    tail -10 logs/app.log
fi