Release HOWTO
=============

1. Prepare for release by updating the changelog in NEWS.rst, bumping the
   version number in setup.py and doing a commit announcing the release to
   the GitHub repository. Also clear out old build products::

   $ make clean

2. Test on all Python versions::

   $ make test

3. Upload package metadata for new version to PyPI::

   $ python setup.py register

4. Build source distribution, wheel and egg::

   $ python setup.py sdist bdist_wheel bdist_egg

5. Securely upload source distribution to PyPI::

   $ twine upload dist/*.tar.gz --sign

6. Securely upload binary egg and wheel to PyPI (with comment explaining
   the version of Mac OS X and architectures for which it were built)::

   $ twine upload dist/*.egg dist/*.whl -c 'Mavericks System Python (32 + 64 bit)' --sign

   Alternatively, do it the manual way, by first signing the egg/wheel, e.g.::

   $ gpg -sab dist/*.whl

   Then use the web form on PyPI (under Package: files) to upload the egg/wheel,
   together with the corresponding .asc PGP signature file and a comment.

7. Repeat steps 4 and 6 for each desired architecture / OS version::

   $ python setup.py bdist_wheel bdist_egg
   $ twine upload dist/*.egg dist/*.whl -c 'Mavericks Other Python (64-bit only)' --sign

8. Tag the git revision that was released::

   $ git tag -s vx.y.z -m 'Released to PyPI as readline x.y.z'
   $ git push origin vx.y.z
