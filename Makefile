# Test across all Python versions (see tox.ini)
test:
	tox

clean:
	-rm -rf build dist rl/readline-lib

.PHONY: test clean

