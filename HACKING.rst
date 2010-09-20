Release HOWTO
=============

1. Test on all Python versions::

   $ make test

2. Upload package metadata and source distribution to PyPI::

   $ python setup.py sdist register upload --sign

3. Upload binary egg to PyPI (do this on each desired architecture)::

   $ python setup.py bdist_egg upload --sign
