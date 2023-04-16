.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: clean
clean:
	docker-compose clean

.PHONY: build
build:
	docker-compose build
	
.PHONY: shell-vue
shell-vue:
	docker-compose exec vue sh

.PHONY: shell-flask
shell-flask:
	docker-compose exec flask bash