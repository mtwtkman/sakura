
.PHONY:

init:
	python3 -m venv v
	v/bin/pip install -U pip
	v/bin/pip install -r requirements-dev.txt

test:
	v/bin/python -m unittest tests

example:
	v/bin/python example.py

mypy:
	v/bin/mypy sakura.py

lint:
	v/bin/black sakura.py

check: lint mypy
