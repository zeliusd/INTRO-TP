# Makefile para construir imágenes Docker

# Definición de variables
APP_IMAGE_NAME=flask-app
WEB_IMAGE_NAME=web-server

# Definición de los directorios de los Dockerfiles
APP_DOCKERFILE_DIR=./api
WEB_DOCKERFILE_DIR=./web

# Objetivo por defecto
all: build-app build-web

# Construir la imagen de la aplicación
instalar: . 
	sudo docker build -t $(APP_IMAGE_NAME) $(APP_DOCKERFILE_DIR) && sudo docker build -t $(WEB_IMAGE_NAME) $(WEB_DOCKERFILE_DIR) && mkdir -p ./pgadmin-data && sudo chown -R 5050:5050 ./pgadmin-data

iniciar: .
	sudo docker compose up -d

apagar: .
	sudo docker compose down
# Construir la imagen de la interfaz web
build-web: docker build -t $(WEB_IMAGE_NAME) $(WEB_DOCKERFILE_DIR)

# Limpiar las imágenes (opcional)
limpiar: .
	sudo docker rmi $(APP_IMAGE_NAME) $(WEB_IMAGE_NAME)

# Ayuda

