app_name = private-rest-api

build:
	docker build -t $(app_name) .

run:
	docker run --name $(app_name) --detach -p 5000:5000 $(app_name)

kill:
	docker stop $(app_name)
	docker container prune -f
	docker rmi -f $(app_name)