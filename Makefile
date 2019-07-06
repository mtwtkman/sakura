bin=v/bin
py=${bin}/python
pip=${bin}/pip
mypy=${bin}/mypy
black=${bin}/black
PYVER := $(shell python -c 'import sys;print(sys.version_info[:2]>=(3,7))')

.PHONY:

init:
ifeq ($(PYVER), True)
	python -m venv v
	${pip} install -U pip
	${pip} install -r requirements-dev.txt
else
	@echo "Required python3.7+"
endif

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
