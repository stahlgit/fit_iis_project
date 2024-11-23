run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

build:
	sudo docker compose -f docker-compose.yml -f deploy/docker-compose-deploy.yml up --build -d

down:
	sudo docker compose -f docker-compose.yml -f deploy/docker-compose-deploy.yml down
