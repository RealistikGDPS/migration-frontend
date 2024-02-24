#!/usr/bin/make
build:
	docker build -t migration_frontend:latest .


shell:
	docker run -it --net=host --entrypoint /bin/bash migration_frontend:latest


lint:
	pre-commit run --all-files

run:
	docker-compose up migration_frontend

run-bg:
	docker-compose up -d migration_frontend


stop:
	docker-compose down

logs:
	docker-compose logs -f
