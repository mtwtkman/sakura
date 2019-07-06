bin=v/bin
py=${bin}/python
pip=${bin}/pip
mypy=${bin}/mypy
black=${bin}/black

.PHONY:

init:
	python3 -m venv v
	${pip} install -U pip
	${pip} install -r requirements-dev.txt

t:
	${py} -m unittest tests

t-app:
	${py} -m unittest tests.test_app${T}

example:
	${py} example.py

mypy:
	${mypy} sakura.py

lint:
	${black} sakura.py

check: lint mypy
