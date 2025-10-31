# Guía de Docker - Entrenador Personal con Asistente IA

Esta guía explica cómo containerizar y ejecutar la aplicación usando Docker.

## Requisitos Previos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 2.0 o superior)

Para verificar la instalación:
```bash
docker --version
docker-compose --version
```

## Estructura de Archivos Docker

```
.
├── Dockerfile              # Definición de la imagen Docker
├── docker-compose.yml      # Orquestación con Docker Compose
├── .dockerignore          # Archivos a excluir de la imagen
└── requirements.txt       # Dependencias Python
```

## Opción 1: Usar Docker directamente

### 1. Construir la imagen

```bash
docker build -t calorie-predictor:latest .
```

Construcción con nombre personalizado:
```bash
docker build -t mi-app-fitness:v1.0 .
```

### 2. Ejecutar el contenedor

Ejecución básica:
```bash
docker run -p 8501:8501 calorie-predictor:latest
```

Con variables de entorno:
```bash
docker run -p 8501:8501 \
  -e OPEN_ROUTER_API_KEY=your_api_key_here \
  calorie-predictor:latest
```

Con volúmenes para persistencia:
```bash
docker run -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/logs:/app/logs \
  -e OPEN_ROUTER_API_KEY=your_api_key_here \
  calorie-predictor:latest
```

En modo detached (segundo plano):
```bash
docker run -d -p 8501:8501 --name calorie-app calorie-predictor:latest
```

### 3. Acceder a la aplicación

Abre tu navegador en:
```
http://localhost:8501
```

## Opción 2: Usar Docker Compose (Recomendado)

Docker Compose simplifica la gestión de contenedores.

### 1. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:
```bash
# .env
OPEN_ROUTER_API_KEY=your_api_key_here
```

### 2. Iniciar servicios

```bash
docker-compose up
```

En modo detached (segundo plano):
```bash
docker-compose up -d
```

Reconstruir antes de iniciar:
```bash
docker-compose up --build
```

### 3. Ver logs

```bash
docker-compose logs -f
```

Ver logs de las últimas 100 líneas:
```bash
docker-compose logs --tail=100 -f
```

### 4. Detener servicios

```bash
docker-compose down
```

Detener y eliminar volúmenes:
```bash
docker-compose down -v
```

### 5. Reiniciar servicios

```bash
docker-compose restart
```

### 6. Ver estado

```bash
docker-compose ps
```

## Comandos Útiles

### Ver contenedores en ejecución
```bash
docker ps
```

### Ver todas las imágenes
```bash
docker images
```

### Eliminar contenedor
```bash
docker rm -f calorie-app
```

### Eliminar imagen
```bash
docker rmi calorie-predictor:latest
```

### Ejecutar comando dentro del contenedor
```bash
docker exec -it calorie-app bash
```

Con docker-compose:
```bash
docker-compose exec calorie-predictor bash
```

### Ver logs del contenedor
```bash
docker logs -f calorie-app
```

### Inspeccionar contenedor
```bash
docker inspect calorie-app
```

## Optimización

### Reducir tamaño de imagen

El Dockerfile ya usa `python:3.11-slim` que es ligero. Para reducir más:

1. Usar multi-stage builds
2. Limpiar cache de apt y pip
3. Usar `.dockerignore` para excluir archivos innecesarios

### Mejorar velocidad de build

1. Aprovechar cache de layers:
   - El `requirements.txt` se copia primero
   - Cambios en el código no recompilan dependencias

2. Build con BuildKit:
```bash
DOCKER_BUILDKIT=1 docker build -t calorie-predictor:latest .
```

## Despliegue en Producción

### Variables de entorno importantes

```bash
# API Keys
OPEN_ROUTER_API_KEY=your_key

# Configuración Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

### Usar con proxy inverso (Nginx)

Ejemplo de configuración Nginx:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Limitar recursos

En docker-compose.yml ya está configurado:
- CPU: 2 cores máximo
- RAM: 2GB máximo

Ajusta según tus necesidades en la sección `deploy.resources`.

## Troubleshooting

### Puerto ya en uso
```bash
# Encontrar proceso usando el puerto
lsof -i :8501

# Usar otro puerto
docker run -p 8502:8501 calorie-predictor:latest
```

### Problema con permisos
```bash
# Dar permisos al directorio
chmod -R 755 .

# Ejecutar como root (no recomendado)
docker run --user root -p 8501:8501 calorie-predictor:latest
```

### Contenedor se detiene inmediatamente
```bash
# Ver logs
docker logs calorie-app

# Ejecutar en modo interactivo
docker run -it -p 8501:8501 calorie-predictor:latest bash
```

### Liberar espacio en disco
```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes sin usar
docker image prune -a

# Limpiar todo (cuidado!)
docker system prune -a --volumes
```

## Seguridad

1. **No incluir secrets en la imagen**
   - Usa variables de entorno
   - Usa Docker secrets en Swarm
   - Usa archivo `.env` (no lo subas a git)

2. **Actualizar dependencias**
```bash
# Reconstruir sin cache
docker-compose build --no-cache
```

3. **Escanear vulnerabilidades**
```bash
docker scout quickview calorie-predictor:latest
```

## Monitoreo

### Health check
El contenedor incluye un health check que verifica el endpoint de Streamlit:
```bash
docker inspect --format='{{json .State.Health}}' calorie-app
```

### Métricas
```bash
docker stats calorie-app
```

## Backup

### Backup de volúmenes
```bash
# Backup del volumen de modelos
docker run --rm \
  -v calorie-predictor_models:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/models-backup.tar.gz /data
```

### Exportar imagen
```bash
docker save calorie-predictor:latest | gzip > calorie-predictor-image.tar.gz
```

### Importar imagen
```bash
docker load < calorie-predictor-image.tar.gz
```

## Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)

## Soporte

Si encuentras problemas:
1. Revisa los logs: `docker-compose logs -f`
2. Verifica variables de entorno
3. Comprueba que los puertos no estén en uso
4. Revisa los permisos de archivos y directorios
