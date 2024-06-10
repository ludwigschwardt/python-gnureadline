Release HOWTO
=============

1. Ensure that the main branch passes all tests. Run "tox" in a local checkout
   and also look at the "Build and test package" GitHub Actions workflow at:

   https://github.com/ludwigschwardt/python-gnureadline/actions/workflows/test.yaml

2. Prepare for release by updating the changelog in NEWS.rst, bumping the
   version number in setup.py and doing a commit announcing the release to
   the GitHub repository.

3. Trigger the "Build wheels" GitHub Actions workflow manually by clicking the
   "Run workflow" button at:

   https://github.com/ludwigschwardt/python-gnureadline/actions/workflows/wheels.yaml

4. Download the "sdist" and "wheels" artifacts of the "Build wheels" workflow
   and unzip::

   $ mkdir wheelhouse
   $ unzip sdist.zip -d wheelhouse
   $ unzip wheels.zip -d wheelhouse

5. Securely upload artifacts to the test PyPI and check that all is well::

   $ twine check wheelhouse/*.tar.gz
   $ twine upload -r testpypi wheelhouse/*.tar.gz

6. Now upload artifacts to the real PyPI (release!)::

   $ twine upload wheelhouse/*.tar.gz
   $ twine upload wheelhouse/*.whl

7. Tag the git revision that was released::

    $ git tag -s vx.y.z -m 'Released to PyPI as gnureadline x.y.z' -u $IDENTITY
    $ git push origin vx.y.z
