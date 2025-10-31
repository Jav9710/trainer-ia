# ==============================================================================
# DOCKERFILE - Entrenador Personal con Asistente IA
# ==============================================================================
# Aplicación Streamlit para predicción de calorías con ML y coach IA
# ==============================================================================

# Usar imagen oficial de Python 3.11 (slim para reducir tamaño)
FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="Entrenador Personal con Asistente IA - Streamlit App"
LABEL version="2.0.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para pygame y audio
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    portaudio19-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de dependencias primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p models logs /tmp/tts_cache_edge

# Configurar permisos
RUN chmod -R 755 /app && \
    chmod -R 777 /tmp/tts_cache_edge

# Exponer el puerto de Streamlit (por defecto 8501)
EXPOSE 8501

# Configuración de salud para verificar que la app está corriendo
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando para ejecutar la aplicación
# Streamlit requiere el flag --server.address para aceptar conexiones externas
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false", \
     "--server.fileWatcherType=none"]

# ==============================================================================
# NOTAS DE USO
# ==============================================================================
#
# Build:
#   docker build -t calorie-predictor:latest .
#
# Run (desarrollo):
#   docker run -p 8501:8501 calorie-predictor:latest
#
# Run (producción con variables de entorno):
#   docker run -p 8501:8501 \
#     -e OPEN_ROUTER_API_KEY=your_api_key \
#     calorie-predictor:latest
#
# Run (con volumen para persistencia de modelos):
#   docker run -p 8501:8501 \
#     -v $(pwd)/models:/app/models \
#     calorie-predictor:latest
#
# Acceder a la aplicación:
#   http://localhost:8501
#
# ==============================================================================
