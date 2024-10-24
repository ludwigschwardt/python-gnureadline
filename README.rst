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

While a lot of effort has gone into making GNU Readline and Editline
interchangeable within Python, they are not fully equivalent. If you want
proper Readline support, this module provides it by bundling the standard
Python readline module with the GNU Readline source code, which is compiled
and statically linked to it. The end result is a package which is simple to
install and only requires the system-dependent ncurses library.

The module is called *gnureadline* so as not to clash with the existing
readline module in the standard library. It supports two general needs:

Code that explicitly imports readline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A typical use case is to override readline in your code like this:

.. code:: python

  try:
      import gnureadline as readline
  except ImportError:
      import readline

Tab completion in the standard interactive Python shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above trick does not fix tab completion in the Python shell because by
the time the shell prints its first output to the screen, it's too late...
One solution is to put this workaround in one of the customization modules
imported by the `site`_ module early on during the startup process.

This is conveniently done for you by installing *gnureadline* and running::

  <python> -m override_readline

where *<python>* is the specific Python interpreter you want to fix
(for example *python3*). The script first tries to add the workaround to
*usercustomize* and then falls back to *sitecustomize* if the user site is
not enabled (for example in virtualenvs). If you want to go straight to
*sitecustomize*, add the standard *-s* option::

  <python> -s -m override_readline

The script explains in detail what it is doing and also refuses to install
the workaround twice. Another benefit of *override_readline* is that the
interactive Python interpreter gains a helpful reminder on startup, like::

  Python 3.12.2 (main, Apr 17 2024, 20:25:57) [Clang 15.0.0 (clang-1500.0.40.1)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  Using GNU readline instead of the default readline (see sitecustomize.py)
  >>>

You don't have to run the *override_readline* script if *gnureadline* was
installed as a dependency of another package. It's only there to help you fix
tab completion in the standard Python shell.

While *usercustomize* and *sitecustomize* are associated with a specific
Python version, you can also fix tab completion for all Python versions
by adding the workaround to the *PYTHONSTARTUP* file (e.g. *~/.pythonrc*).
This requires some extra setup as seen in this `example pythonrc`_, which also
shows a way to maintain separate history files for libreadline and libedit.
The *PYTHONSTARTUP* file only affects the interactive shell, while
user / site customization affects general scripts using readline as well.
The Python Tutorial has a `section`_ describing these customization options.

**Please take note that** `IPython`_ **does not depend on gnureadline for tab
completion anymore. Since version 5.0 it uses** `prompt_toolkit`_ **instead.**

Versions
--------

The module can be used with both Python 2.x and 3.x, and has been tested with
Python versions 2.6, 2.7, and 3.2 to 3.13. The first three numbers of the
module version reflect the version of the underlying GNU Readline library
(major, minor and patch level), while any additional fourth number
distinguishes different module updates based on the same Readline library.

The latest development version is available from the `GitHub repository`_.

If you are using Windows, which also ships without GNU Readline, you might
want to consider using the `pyreadline3`_ module instead, which is a readline
replacement written in pure Python that interacts with the Windows clipboard.

**Please note that Python 3.13 introduced a new interactive interpreter.**
It reimplements some of the GNU Readline functionality in Python and thereby
bypasses it (for example when entering Ctrl-R to search the command history).
Its behaviour may be subtly different though. If you want to revert to the
old interpreter, set the environment variable `PYTHON_BASIC_REPL=1`.

.. _GNU Readline: http://www.gnu.org/software/readline/
.. _Editline: http://www.thrysoee.dk/editline/
.. _site: https://docs.python.org/library/site.html
.. _example pythonrc: https://github.com/ludwigschwardt/python-gnureadline/issues/62#issuecomment-1724103579
.. _section: https://python.readthedocs.io/en/latest/tutorial/appendix.html#interactive-mode
.. _IPython: http://ipython.org/
.. _prompt_toolkit: http://python-prompt-toolkit.readthedocs.io/en/stable/
.. _GitHub repository: http://github.com/ludwigschwardt/python-gnureadline
.. _pyreadline3: http://pypi.python.org/pypi/pyreadline3
