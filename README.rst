Stand-alone GNU readline module
===============================

First... STOP
-------------

Consider this: do you really need this package in 2022? You typically don't if

- you use the Python provided by a standard Linux distribution like Ubuntu,
  Debian, CentOS, etc. *(It already uses the proper readline.)*
- you run **Windows**
  *(It won't work! Try* `pyreadline`_ or `prompt_toolkit`_ *instead.)*
- you use the Python provided by **Homebrew** or Fink on macOS
  *(It has real readline already!)*
- you want it for `IPython`_
  *(It switched to* `prompt_toolkit`_ *in version 5.0.)*
- you use a Python distribution like Anaconda or Enthought / Canopy
  *(Again, real readline.)*

You might need it if

- you use Python provided by MacPorts or the system on macOS
  *(Python compiled against libedit.)*
- you use a Python distribution like ActivePython on Linux or macOS
  *(This used to ship without readline.)*
- you want to get the latest bug fixes and features in either the readline
  library or its Python module *(Typically when stuck on older systems.)*

Still interested?
-----------------

Some platforms, such as macOS, do not ship with `GNU readline`_ installed.
The readline extension module in the standard library of Mac "system" Python
uses NetBSD's `editline`_ (libedit) library instead, which is a readline
replacement with a less restrictive software license.

As the alternatives to GNU readline do not have fully equivalent functionality,
it is useful to add proper readline support to these platforms. This module
achieves this by bundling the standard Python readline module with the GNU
readline source code, which is compiled and statically linked to it. The end
result is a package which is simple to install and requires no extra shared
libraries.

The module is called *gnureadline* so as not to clash with the readline module
in the standard library. This keeps polite installers such as `pip`_ happy and
is sufficient for shells such as `IPython`_. **Please take note that IPython
does not depend on gnureadline anymore since version 5.0 as it now uses**
`prompt_toolkit`_ **instead.**

A typical use case is::

.. code-block:: python

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
Python versions 2.6, 2.7, and 3.2 to 3.10. The first three numbers of the module
version reflect the version of the underlying GNU readline library (major,
minor and patch level), while any additional fourth number distinguishes
different module updates based on the same readline library.

This module is usually unnecessary on Linux and other Unix systems with default
readline support. An exception is if you have a Python distribution that does
not include GNU readline due to licensing restrictions (such as ActiveState's
ActivePython in the past). If you are using Windows, which also ships without
GNU readline, you might want to consider using the `pyreadline`_ module instead,
which is a readline replacement written in pure Python that interacts with the
Windows clipboard.

The latest development version is available from the `GitHub repository`_.

.. _GNU readline: http://www.gnu.org/software/readline/
.. _editline: http://www.thrysoee.dk/editline/
.. _pip: http://www.pip-installer.org/
.. _IPython: http://ipython.org/
.. _prompt_toolkit: http://python-prompt-toolkit.readthedocs.io/en/stable/
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _pyreadline: http://pypi.python.org/pypi/pyreadline
.. _GitHub repository: http://github.com/ludwigschwardt/python-gnureadline
