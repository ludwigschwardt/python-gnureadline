# Test across all Python versions (see tox.ini)
test:
	curl "https://bitbucket.org/hpk42/tox/raw/tip/toxbootstrap.py" > /tmp/toxbootstrap.py
	python /tmp/toxbootstrap.py

clean:
	-rm -rf build dist rl/readline-lib

.PHONY: test clean

