# Test across all Python versions (see tox.ini)
test:
	pip install tox
	tox

clean:
	-rm -rf build dist rl/readline-lib

.PHONY: test clean

