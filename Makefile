dev:
	fastapi dev src/main.py

run:
	fastapi run src/main.py

requirements:
	pip-compile requirements.in

requirements-dev:
	pip-compile requirements-dev.in
