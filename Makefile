# Test across all Python versions (see tox.ini)
test:
	curl "https://bitbucket.org/hpk42/tox/raw/tip/toxbootstrap.py" > /tmp/toxbootstrap.py
	python /tmp/toxbootstrap.py

.PHONY: test

