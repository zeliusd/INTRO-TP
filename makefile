
APP_IMAGE_NAME=flask-app
WEB_IMAGE_NAME=web-server

APP_DOCKERFILE_DIR=./api
WEB_DOCKERFILE_DIR=./web

all: instalar iniciar

instalar: . 
	sudo docker build -t $(APP_IMAGE_NAME) $(APP_DOCKERFILE_DIR) && sudo docker build -t $(WEB_IMAGE_NAME) $(WEB_DOCKERFILE_DIR) && mkdir -p ./pgadmin-data && sudo chown -R 5050:5050 ./pgadmin-data

iniciar: .
	sudo docker-compose up -d

apagar: .
	sudo docker-compose down

limpiar: .
	sudo docker rmi $(APP_IMAGE_NAME) $(WEB_IMAGE_NAME)


