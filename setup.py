#!/usr/bin/env python

import os
import os.path
import sys
import distutils

# Ensure that the correct version of setuptools is installed
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, Extension

VERSION = '2.6.5' + '.dev'
DESCRIPTION = "GNU readline support for Python on platforms without readline."
LONG_DESCRIPTION = """
Some platforms, such as Mac OS X, do not ship with GNU readline installed. The
readline extension module in the standard library of Mac 'system' Python uses
NetBSD's editline (libedit) library instead, which is a readline replacement with 
a less restrictive software license.

As the alternatives to GNU readline do not have fully equivalent functionality,
it is useful to add proper readline support to these platforms. This module 
achieves this by bundling the standard Python readline module with the GNU readline 
source code, which is compiled and statically linked to it. The end result is an
egg which is simple to install, with no extra shared libraries required.

The 2.6.4 version of this module is intended for use on Mac OS 10.6 (Snow Leopard),
which ships with Python 2.6. It should also work on Tiger and Leopard with Python
2.5, and may even work on Linux. It is built against GNU readline 6.0 with the
latest patches.

This module is completely unnecessary on Linux and other Unix systems with default 
readline support. If you are using Windows, which also ships without GNU readline,
you might want to consider using the pyreadline module instead, which is a readline 
replacement written in pure Python that interacts with the Windows clipboard. 
"""

CLASSIFIERS = filter(None, map(str.strip,
"""                 
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Natural Language :: English
Operating System :: MacOS :: MacOS X
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines()))

# If we are on Mac OS 10.5 or later, attempt a universal binary, which is the way
# the original system version of readline.so was compiled. Set up flags here.
UNIVERSAL = ''
if distutils.util.get_platform().find('macosx-10.5') == 0:
    UNIVERSAL = '-isysroot /Developer/SDKs/MacOSX10.5.sdk ' + \
                '-arch i386 -arch ppc -arch x86_64 -arch ppc64'
elif distutils.util.get_platform().find('macosx-10.6') == 0:
    # Snow Leopard has only 3 architectures
    UNIVERSAL = '-isysroot /Developer/SDKs/MacOSX10.6.sdk ' + \
                '-arch i386 -arch ppc -arch x86_64'

# Since we have the latest readline (post 4.2), enable all readline functionality
# These macros can be found in pyconfig.h.in in the main directory of the Python tarball
DEFINE_MACROS = [('HAVE_RL_CALLBACK', None),
                 ('HAVE_RL_CATCH_SIGNAL', None),
                 ('HAVE_RL_COMPLETION_APPEND_CHARACTER', None),
                 ('HAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK', None),
                 ('HAVE_RL_COMPLETION_MATCHES', None),
                 ('HAVE_RL_COMPLETION_SUPPRESS_APPEND', None),
                 ('HAVE_RL_PRE_INPUT_HOOK', None)]

# Check if any of the distutils commands involves building the module,
# and check for quiet vs. verbose option
building = False
verbose = True
for s in sys.argv[1:]:
    if s.startswith('bdist') or s.startswith('build') or s.startswith('install'):
        building = True
    if s in ['--quiet', '-q']:
        verbose = False
    if s in ['--verbose', '-v']:
        verbose = True
    
# Build readline first, if it is not there and we are building the module
if building and not os.path.exists('readline/libreadline.a'):
    if verbose:
        print "\n============ Building the readline library ============\n"
        os.system('cd rl && /bin/bash ./build.sh')
        print "\n============ Building the readline extension module ============\n"
    else:
        os.system('cd rl && /bin/bash ./build.sh > /dev/null 2>&1')        
    # Add symlink that simplifies include and link paths to real library
    if not (os.path.exists('readline') or os.path.islink('readline')):
        os.symlink(os.path.join('rl','readline-lib'), 'readline')

setup(
    name="readline",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    maintainer="Ludwig Schwardt",
    maintainer_email="ludwig.schwardt@gmail.com",
    url="http://pypi.python.org/pypi/readline",
    license="GNU GPL",
    platforms=['MacOS'],
    ext_modules=[
        Extension(name="readline",
                  sources=["Modules/readline.c"],
                  include_dirs=['.'],
                  define_macros=DEFINE_MACROS,
                  extra_compile_args=['-Wno-strict-prototypes'] + UNIVERSAL.split(),
                  extra_link_args=UNIVERSAL.split(),
                  extra_objects=['readline/libreadline.a', 'readline/libhistory.a'], 
                  libraries=['ncurses']
        ),
    ],
    zip_safe=False,
)
