Stand-alone GNU readline module
===============================

.. image:: https://img.shields.io/github/actions/workflow/status/ludwigschwardt/python-gnureadline/test.yaml?branch=main
   :alt: GitHub Workflow Status
   :target: https://github.com/ludwigschwardt/python-gnureadline/actions/workflows/test.yaml

Do I need this package?
-----------------------

Do the following quick check::

  python -c "import readline; print(readline.__doc__)"

If the output is::

  Importing this module enables command line editing using GNU readline.

then you already have GNU Readline and you probably don't need this package
(unless you know what you are doing!). However, if the output is::

  Importing this module enables command line editing using libedit readline.

then you've come to the right place.


Still interested?
-----------------

Some Posix platforms such as macOS do not ship with `GNU Readline`_ installed.
Readline is licensed under the GPL, which makes it hard to distribute with
proprietary software. A popular alternative is NetBSD's `Editline`_ (libedit)
library which has a less restrictive BSD license. If you install Python on
macOS via a popular open-source package manager such as Homebrew or MacPorts,
you'll get a readline extension module that calls libedit internally (even
though it's confusingly still called "readline"!).

While a lot of effort has been expended to make GNU Readline and Editline
interchangeable within Python, they are not fully equivalent. If you want
proper Readline support, this module provides it by bundling the standard
Python readline module with the GNU Readline source code, which is compiled
and statically linked to it. The end result is a package which is simple to
install and requires no extra shared libraries.

The module is called *gnureadline* so as not to clash with the readline module
in the standard library. This keeps polite installers such as `pip`_ happy and
is sufficient for shells such as `IPython`_. **Please take note that IPython
does not depend on gnureadline anymore since version 5.0 as it now uses**
`prompt_toolkit`_ **instead.**

A typical use case is to override readline in your code like this:

.. code:: python

  try:
      import gnureadline as readline
  except ImportError:
      import readline

If you want to use this module as a drop-in replacement for readline in the
standard Python shell, it has to be installed with the less polite easy_install
script found in `setuptools`_. **Please take note that easy_install has been
deprecated for a while and is about to be dropped from setuptools. Proceed at
your own risk!**

The module can be used with both Python 2.x and 3.x, and has been tested with
Python versions 2.6, 2.7, and 3.2 to 3.12. The first three numbers of the module
version reflect the version of the underlying GNU Readline library (major,
minor and patch level), while any additional fourth number distinguishes
different module updates based on the same Readline library.

This module is usually unnecessary on Linux and other Unix systems with default
readline support. An exception is if you have a Python distribution that does
not include GNU Readline due to licensing restrictions (such as ActiveState's
ActivePython in the past). If you are using Windows, which also ships without
GNU Readline, you might want to consider using the `pyreadline`_ module instead,
which is a readline replacement written in pure Python that interacts with the
Windows clipboard.

The latest development version is available from the `GitHub repository`_.

.. _GNU Readline: http://www.gnu.org/software/readline/
.. _Editline: http://www.thrysoee.dk/editline/
.. _pip: http://www.pip-installer.org/
.. _IPython: http://ipython.org/
.. _prompt_toolkit: http://python-prompt-toolkit.readthedocs.io/en/stable/
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _pyreadline: http://pypi.python.org/pypi/pyreadline
.. _GitHub repository: http://github.com/ludwigschwardt/python-gnureadline
