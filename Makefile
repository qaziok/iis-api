dev:
	fastapi dev src/main.py --port 2137

run:
	fastapi run src/main.py --port 8080

requirements:
	pip-compile requirements.in
	pip-compile requirements-dev.in
