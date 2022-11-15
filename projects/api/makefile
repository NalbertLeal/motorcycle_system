build:
	@sudo docker build -t nalbertgml/api_alpr:latest -f dockerfile ../..
run:
	@sudo docker run -d --name api-alpr -p 8080:8080 nalbertgml/api_alpr:latest
stop:
	@sudo docker stop api-alpr