# Test across all Python versions (see tox.ini)
# Requires: http://codespeak.net/tox/
test:
	tox

# If tox is not installed:
test-notox:
	python toxbootstrap.py
