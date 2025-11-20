#!/bin/bash

# Script para detener MEMOR.IA
echo "⏹️ Deteniendo MEMOR.IA..."

# Verificar si existe el archivo PID
if [ -f logs/streamlit.pid ]; then
    PID=$(cat logs/streamlit.pid)

    if ps -p $PID > /dev/null; then
        echo "🔄 Deteniendo proceso $PID..."
        kill $PID
        sleep 2

        if ps -p $PID > /dev/null; then
            echo "⚡ Forzando detención..."
            kill -9 $PID
        fi

        echo "✅ Proceso detenido"
    else
        echo "⚠️ El proceso ya estaba detenido"
    fi

    rm -f logs/streamlit.pid
else
    echo "⚠️ No se encontró archivo PID, deteniendo todos los procesos Streamlit..."
    pkill -f "streamlit run memoria_tecnica_pro_v2.py"
fi

echo "🏁 MEMOR.IA detenido correctamente"