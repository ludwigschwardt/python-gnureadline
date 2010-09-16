Release HOWTO
=============

1. Test on all Python versions::

   $ make test

2. Upload sdist to PyPI:

   $ python setup.py sdist register upload
