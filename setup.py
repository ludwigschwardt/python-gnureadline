#!/usr/bin/env python

import os
import sys
import glob
import distutils

from setuptools import setup, Extension

if sys.platform == 'win32':
    sys.exit('error: this module is not meant to work on Windows')

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

VERSION = '6.2.2'
DESCRIPTION = 'The standard Python readline extension statically linked against the GNU readline library.'
LONG_DESCRIPTION = README + '\n\n' + NEWS
CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: C',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# If we are on Mac OS 10.5 or later, attempt a universal binary, which is the way
# the original system version of readline.so was compiled. Set up flags here.
UNIVERSAL = ''
platform = distutils.util.get_platform()
if platform.startswith('macosx'):
    osx_version = platform.split('-')[1]
    if osx_version == '10.5':
        UNIVERSAL = '-isysroot /Developer/SDKs/MacOSX10.5.sdk -arch i386 -arch ppc -arch x86_64 -arch ppc64'
    elif osx_version == '10.6':
        # Starting with 10.6 (Snow Leopard), only Intel architecture is supported
        UNIVERSAL = '-isysroot /Developer/SDKs/MacOSX10.6.sdk -arch i386 -arch x86_64'
    elif osx_version > '10.6':
        # Starting with 10.7 (Lion) and Xcode 4.3, the developer sysroot is inside the Xcode.app - ignore it
        UNIVERSAL = '-arch i386 -arch x86_64'

# Since we have the latest readline (post 4.2), enable all readline functionality
# These macros can be found in pyconfig.h.in in the main directory of the Python tarball
DEFINE_MACROS = [
    ('HAVE_RL_CALLBACK', None),
    ('HAVE_RL_CATCH_SIGNAL', None),
    ('HAVE_RL_COMPLETION_APPEND_CHARACTER', None),
    ('HAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK', None),
    ('HAVE_RL_COMPLETION_MATCHES', None),
    ('HAVE_RL_COMPLETION_SUPPRESS_APPEND', None),
    ('HAVE_RL_PRE_INPUT_HOOK', None),
]

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
        print("\n============ Building the readline library ============\n")
        os.system('cd rl && /bin/bash ./build.sh')
        print("\n============ Building the readline extension module ============\n")
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
    maintainer="Ludwig Schwardt; Sridhar Ratnakumar",
    maintainer_email="ludwig.schwardt@gmail.com; github@srid.name",
    url="http://github.com/ludwigschwardt/python-readline",
    license="GNU GPL",
    platforms=['MacOS X', 'Posix'],
    include_package_data=True,
    ext_modules=[
        Extension(name="readline",
                  sources=["Modules/%s.x/readline.c" % (sys.version_info[0],)],
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
