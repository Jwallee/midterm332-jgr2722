#jgr2722

NAME ?= jwallee

all: build run

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker image build -t ${NAME}/app:1.0 .

run:
	docker run --name "ISS-Data-Analysis" -d -p 5023:5000 ${NAME}/app:1.0