build:
	@docker build -t nalbertgml/alpr-api:1.0.0 -f dockerfile ../..
run:
	@docker run -d --name medias-api -p 8080:8080 nalbertgml/alpr-api:1.0.0
stop:
	@docker stop medias-api