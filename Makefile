WORKDIR = notes-app

style:
	black $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)