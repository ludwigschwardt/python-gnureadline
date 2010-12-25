# Test across all Python versions (see tox.ini)
test:
	curl "https://pytox.googlecode.com/hg/toxbootstrap.py" > /tmp/toxbootstrap.py
	python /tmp/toxbootstrap.py

.PHONY: test

