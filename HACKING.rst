Release HOWTO
=============

1. Prepare for release by updating the changelog in NEWS.rst, bumping the
   version number in setup.py and doing a commit announcing the release to
   the GitHub repository.

2. Test on all Python versions::

   $ make test

3. Upload package metadata and source distribution to PyPI::

   $ python setup.py sdist register upload --sign

4. Upload binary egg to PyPI directly (do this on each desired architecture)::

   $ python setup.py bdist_egg upload --sign

   Alternatively, do it the manual way, which allows comments to be added::

   $ python setup.py bdist_egg
   $ gpg -sab dist/readline-x.y.z-pyX.Y-platform.egg

   Then use the web form on PyPI (under Package: files) to upload the egg,
   together with the corresponding .asc PGP signature file and a comment
   explaining the architecture and specific Python distribution for which
   it was built.
