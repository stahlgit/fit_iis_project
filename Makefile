run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

build:
	sudo docker compose -f docker-compose.yml -f deploy/docker-compose-deploy.yml up --build -d

down:
	sudo docker compose -f docker-compose.yml -f deploy/docker-compose-deploy.yml down

copy:
	docker exec -t iis_database pg_dump -U postgres -d your_db_name > ./dump.sql


send:
	scp ./dump.sql root@164.92.232.11:fit_iis_project
	cat dump.sql | docker exec -i iis_database psql -U postgres -d your_db_name
