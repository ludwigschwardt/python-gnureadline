Stand-alone readline module
===========================

Some platforms, such as Mac OS X, do not ship with `GNU readline`_ installed.
The readline extension module in the standard library of Mac "system" Python
uses NetBSD's `editline`_ (libedit) library instead, which is a readline
replacement with a less restrictive software license.

As the alternatives to GNU readline do not have fully equivalent functionality,
it is useful to add proper readline support to these platforms. This module
achieves this by bundling the standard Python readline module with the GNU
readline source code, which is compiled and statically linked to it. The end
result is a package which is simple to install and requires no extra shared
libraries.

The module can be used with both Python 2.x and 3.x, and has been tested with
Python versions 2.5, 2.6, 2.7 and 3.1. The major and minor numbers of the module
version reflect the version of the underlying GNU readline library, while the
third (patch) number distinguishes different module updates based on the same
readline library.

This module is usually unnecessary on Linux and other Unix systems with default
readline support. An exception is if you have a Python distribution that does
not include GNU readline due to licensing restrictions (such as ActiveState's
`ActivePython`_). If you are using Windows, which also ships without GNU 
readline, you might want to consider using the `pyreadline`_ module instead, 
which is a readline replacement written in pure Python that interacts with the
Windows clipboard. 

The latest development version is available from the `GitHub repository`_.

.. _GNU readline: http://www.gnu.org/software/readline/
.. _editline: http://www.thrysoee.dk/editline/
.. _ActivePython: http://community.activestate.com/faq/why-doesnt-activepython-u
.. _pyreadline: http://pypi.python.org/pypi/pyreadline
.. _GitHub repository: http://github.com/ludwigschwardt/python-readline
