History
=======

6.3.8 (2017-10-20)
------------------

* #42, #44: Address compiler issues (avoid Cygwin, fix multi-arch on gcc)
* #40: Make GPLv3 license explicit
* #39: Look for bash shell in more places
* Uses Python 2.x readline.c from hg 2.7 branch (95814:192f9efe4a38)
* Uses Python 3.x readline.c from hg 3.4 / 3.5 branch (95813:ec6ed10d611e)
* Updated to build against readline 6.3 (patch-level 8)

6.3.3 (2014-04-08)
------------------

* Major rework of OS X build process (detect arches, no custom flags)
* #20, #22, #28: Various issues addressed by new streamlined build
* #28: Use $CC or cc to compile libreadline instead of default gcc
* #35: Workaround for clang from Xcode 5.1 and Mac OS X 10.9.2
* Uses Python 3.4 readline.c from hg 3.4 branch (89086:3110fb3095a2)
* Updated to build against readline 6.3 (patch-level 3)

6.2.5 (2014-02-19)
------------------

* Renamed module to *gnureadline* to improve installation with pip
* #23, #25-27, #29-33: Tweaks and package reworked to gnureadline
* Uses Python 2.x readline.c from hg 2.7 branch (89084:6b10943a5916)
* Uses Python 3.x readline.c from hg 3.3 branch (89085:6adac0d9b933)
* Updated to build against readline 6.2 (patch-level 5)

6.2.4.1 (2012-10-22)
--------------------

* #21: Fixed building on Python.org 3.3 / Mac OS 10.8

6.2.4 (2012-10-17)
------------------

* #15: Improved detection of compilers before Xcode 4.3
* Uses Python 3.x readline.c from v3.3.0 tag (changeset 73997)
* Updated to build against readline 6.2 (patch-level 4)

6.2.2 (2012-02-24)
------------------

* #14: Fixed compilation with Xcode 4.3 on Mac OS 10.7
* Updated to build against readline 6.2 (patch-level 2)

6.2.1 (2011-08-31)
------------------

* #10: Fixed '_emacs_meta_keymap' missing symbol on Mac OS 10.7
* #7: Fixed SDK version check to work with Mac OS 10.7 and later
* Uses Python 2.x readline.c from release27-maint branch (r87358)
* Uses Python 3.x readline.c from release32-maint branch (r88446)

6.2.0 (2011-06-02)
------------------

* #5: Removed '-arch ppc' on Mac OS 10.6, as Snow Leopard supports Intel only
* Updated to build against readline 6.2 (patch-level 1)

6.1.0 (2010-09-20)
------------------

* Changed version number to reflect readline version instead of Python version
* #4: Updated to build against readline 6.1 (patch-level 2)
* #2: Python 3 support
* Uses Python 2.x readline.c from release27-maint branch (r83672)
* Uses Python 3.x readline.c from r32a2 tag (r84541)
* Source code moved to GitHub
* Additional maintainer: Sridhar Ratnakumar

2.6.4 (2009-11-26)
------------------

* Added -fPIC to compiler flags to fix linking error on 64-bit Ubuntu
* Enabled all readline functionality specified in pyconfig.h macros
* Uses readline.c from Python svn trunk (r75725), which followed 2.6.4 release
* Patched readline.c to replace Py_XDECREF calls with the safer Py_CLEAR
* Fixed compilation error on Mac OS 10.4 with XCode older than version 2.4

2.6.1 (2009-11-18)
------------------

* Updated package to work with Mac OS 10.6 (Snow Leopard), which ships with
  Python 2.6.1
* Uses readline.c from Python 2.6.1 release
* Backported "spurious trailing space" bugfix from Python svn trunk (see e.g.
  https://bugs.launchpad.net/python/+bug/470824 for details on bug)
* Updated to build against readline 6.0 (patch-level 4)
* Now builds successfully on Linux (removed Mac-specific flags in this case),
  and still supports Mac OS 10.4 and 10.5

2.5.1 (2008-05-28)
------------------

* Updated package to work with Mac OS 10.5 (Leopard), which ships with Python
  2.5.1
* Uses readline.c from Python 2.5.1 release
* Updated to build against readline 5.2 (patch-level 12)
* New maintainer: Ludwig Schwardt

2.4.2 (2005-12-26)
------------------

* Original package by Bob Ippolito, supporting Python 2.3 / 2.4 on Mac OS 10.3
  (Panther) and 10.4 (Tiger)
* Builds against readline 5.1
