#!/usr/bin/env python

import os
import sys
from setuptools.command.build_ext import build_ext
import subprocess

from setuptools import setup, Extension

if sys.platform == 'win32':
    sys.exit('Error: this module is not meant to work on Windows (try pyreadline instead)')
elif sys.platform == 'cygwin':
    sys.exit('Error: this module is not needed for Cygwin (and probably does not compile anyway)')

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

VERSION = '8.1.2'
DESCRIPTION = 'The standard Python readline extension statically linked against the GNU readline library.'
LONG_DESCRIPTION = README + '\n\n' + NEWS
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: C',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Since we have the latest readline (post 4.2), enable all readline functionality
# These macros can be found in pyconfig.h.in in the main directory of the Python tarball
DEFINE_MACROS = [
    ('HAVE_RL_APPEND_HISTORY', None),
    ('HAVE_RL_CALLBACK', None),
    ('HAVE_RL_CATCH_SIGNAL', None),
    ('HAVE_RL_COMPDISP_FUNC_T', None),
    ('HAVE_RL_COMPLETION_APPEND_CHARACTER', None),
    ('HAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK', None),
    ('HAVE_RL_COMPLETION_MATCHES', None),
    ('HAVE_RL_COMPLETION_SUPPRESS_APPEND', None),
    ('HAVE_RL_PRE_INPUT_HOOK', None),
    ('HAVE_RL_RESIZE_TERMINAL', None),
    # Ensure that the local checkout of readline includes its own headers
    ('READLINE_LIBRARY', None),
]


def which_shell():
    valid_paths = ["/bin/bash", "/usr/local/bin/bash", "/bin/sh"]
    for path in valid_paths:
        if os.path.exists(path):
            return path
    raise IOError("No Shell Found")


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
    shell_path = which_shell()
    if verbose:
        print("\n============ Building the readline library ============\n")
        os.system('cd rl && %s ./build.sh' % shell_path)
        print("\n============ Building the readline extension module ============\n")
    else:
        os.system('cd rl && %s ./build.sh > /dev/null 2>&1' % shell_path)
    # Add symlink that simplifies include and link paths to real library
    if not (os.path.exists('readline') or os.path.islink('readline')):
        os.symlink(os.path.join('rl', 'readline-lib'), 'readline')


# Workaround for OS X 10.9.2 and Xcode 5.1+
# The latest clang treats unrecognized command-line options as errors and the
# Python CFLAGS variable contains unrecognized ones (e.g. -mno-fused-madd).
# See Xcode 5.1 Release Notes (Compiler section) and
# http://stackoverflow.com/questions/22313407 for more details. This workaround
# follows the approach suggested in http://stackoverflow.com/questions/724664.
class build_ext_subclass(build_ext):
    def build_extensions(self):
        if sys.platform == 'darwin':
            # Test the compiler that will actually be used to see if it likes flags
            proc = subprocess.Popen(self.compiler.compiler + ['-v'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)
            stdout, stderr = proc.communicate()
            clang_mesg = "clang: error: unknown argument: '-mno-fused-madd'"
            if proc.returncode and stderr.splitlines()[0].startswith(clang_mesg):
                for ext in self.extensions:
                    # Use temporary workaround to ignore invalid compiler option
                    # Hopefully -mno-fused-madd goes away before this workaround!
                    ext.extra_compile_args += ['-Wno-error=unused-command-line-argument-hard-error-in-future']
        build_ext.build_extensions(self)


# First try version-specific readline.c, otherwise fall back to major-only version
source = os.path.join('Modules', '%d.%d' % sys.version_info[:2], 'readline.c')
if not os.path.exists(source):
    source = os.path.join('Modules', '%d.x' % (sys.version_info[0],), 'readline.c')

setup(
    name="gnureadline",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    classifiers=CLASSIFIERS,
    maintainer="Ludwig Schwardt, Sridhar Ratnakumar",
    maintainer_email="ludwig.schwardt@gmail.com, srid@srid.ca",
    url="http://github.com/ludwigschwardt/python-gnureadline",
    include_package_data=True,
    py_modules=['readline', 'override_readline'],
    cmdclass={'build_ext': build_ext_subclass},
    ext_modules=[
        Extension(name="gnureadline",
                  sources=[source],
                  define_macros=DEFINE_MACROS,
                  extra_objects=['readline/libreadline.a', 'readline/libhistory.a'],
                  libraries=['ncurses']
                  ),
    ],
    zip_safe=False,
)
