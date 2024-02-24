#!/usr/bin/make
build:
	docker build -t migration_frontend:latest .


shell:
	docker run -it --net=host --entrypoint /bin/bash migration_frontend:latest


lint:
	pre-commit run --all-files
