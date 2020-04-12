up:
	docker build docker -t signali
	docker run -it --rm -p 5100:5100 -v $(PWD)/app:/app --name signali signali
