PRJ = pymlconf
PIP = pip3

.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

.PHONY: cover
cover:
	pytest --cov=$(PRJ) tests


.PHONY: lint
lint:
	pylama

.PHONY: dist
dist:
	python setup.py sdist
