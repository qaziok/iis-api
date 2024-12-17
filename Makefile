dev:
	fastapi dev src/main.py

run:
	fastapi run src/main.py --port 8080

requirements:
	pip-compile requirements.in

requirements-dev:
	pip-compile requirements-dev.in
