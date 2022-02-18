#! /bin/bash
set -e

# If we are on Mac OS X, try to do a universal build, as this will allow the
# Python extension to pick the architectures it needs from the static library
if [ `uname` == "Darwin" ]; then
	# Force the compiler to CC (or cc by default) to ensure that the architecture
	# flag detection is done on the same compiler that is used to compile libreadline.
	# Without this libreadline will default to gcc, which might not be the same as cc
	# and also does not support -arch if it is the real gcc. The Python extension module
	# will typically be compiled by clang on Darwin, which should be the default cc.
	osx_compiler=${CC-cc}
	cc_override="CC=$osx_compiler"
	echo "Using compiler $osx_compiler on OS X"
	# Parse output of cc -v to guess real compiler (works with clang and gcc, at least)
	echo "Guessing actual compiler:" `$osx_compiler -v 2>&1 | grep ' version '`
	detected_arches="Compiler supports architectures:"
	echo $'#include <stdio.h>\nint main() {\n  printf("Hello world\\n");\n}' > test.c
	# Find out which architectures are supported by doing a test compile AND link per arch
  arch_flags=''
	for arch in i386 x86_64 ppc ppc64; do
		arch_flag=' -arch '$arch
		if ${CC-cc} $arch_flag test.c 2> /dev/null; then
			arch_flags+=$arch_flag
			detected_arches+=' '$arch
		fi
	done
	echo $detected_arches
  # Verify the final arch flags (typically containing multiple architectures).
  # If it doesn't work, we probably have GNU gcc which cannot handle
  # i386 + x86_64 (in that order) - go for x86_64 only instead.
	if ! ${CC-cc} $arch_flags test.c 2> /dev/null; then
    if test "$arch_flags" == ' -arch i386 -arch x86_64'; then
      echo "Compiler (gcc?) fails with both i386 and x86_64 arches - do x86_64 only"
      arch_flags=' -arch x86_64'
    else
      echo "Compiler fails with multiple arches - go back to default architecture"
      arch_flags=''
    fi
	fi
	rm -f test.c test.o a.out
	# Don't set sysroot anymore (should be fine for OS X 10.6+)
  CFLAGS+=$arch_flags
	export CFLAGS
fi

rm -rf readline-lib
tar xzvf readline-8.1.tar.gz
mv readline-8.1 readline-lib
cd readline-lib
patch -p0 < ../readline81-001
patch -p0 < ../readline81-002
# Force compiler to CC/cc in the case of Darwin
./configure CPPFLAGS='-DNEED_EXTERN_PC -fPIC' $cc_override
# Only the static libraries are required
make static
