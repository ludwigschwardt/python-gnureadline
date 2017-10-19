Release HOWTO
=============

1. Ensure that the master branch passes all tests on Travis at::

   https://travis-ci.org/ludwigschwardt/python-gnureadline/branches

2. Update the macOS Travis branch and ensure that it also passes all tests::

   $ git checkout travis-ci.macosx
   $ git merge master [accept all "our" changes to .travis.yml]
   $ git push
   $ git checkout master

3. Prepare for release by updating the changelog in NEWS.rst, bumping the
   version number in setup.py and doing a commit announcing the release to
   the GitHub repository. Also clear out old build products::

   $ make clean

4. Build source distribution::

   $ python setup.py sdist

5. Securely upload source distribution to PyPI and/or the test PyPI (release!)::

   $ twine upload -r testpypi dist/*.tar.gz --sign
   $ twine upload dist/*.tar.gz --sign

6. Tag the git revision that was released::

    $ git tag -s vx.y.z -m 'Released to PyPI as gnureadline x.y.z'
    $ git push origin vx.y.z

7. Clone python-gnureadline-wheels repository, update python-gnureadline
   submodule to tagged version, bump BUILD_COMMIT to latest tag in .travis.yml
   and push to GitHub to trigger wheel production. Check progress at::

    https://travis-ci.org/MacPython/python-gnureadline-wheels

8. Clone terryfy repository to get wheel-uploader utility and run::

    $ VERSION=x.y.z
    $ CDN_URL=https://3f23b170c54c2533c070-1c8a9b3114517dc5fe17b7c3f8c63a43.ssl.cf2.rackcdn.com
    $ wheel-uploader -r testpypi -u $CDN_URL -s -v -w ~/scratch/wheelhouse -t manylinux1 gnureadline $VERSION
    $ wheel-uploader -r testpypi -u $CDN_URL -s -v -w ~/scratch/wheelhouse -t macosx gnureadline $VERSION
