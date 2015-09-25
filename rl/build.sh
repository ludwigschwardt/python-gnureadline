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
	detected_arches="Compiler supports architectures:"
	echo $'#include <stdio.h>\nint main() {\n  printf("Hello world\\n");\n}' > test.c
	# Find out which architectures are supported by doing a test compile AND link
	for arch in i386 x86_64 ppc ppc64; do
		arch_flag=' -arch '$arch
		if ${CC-cc} $arch_flag test.c 2> /dev/null; then
			CFLAGS+=$arch_flag
			detected_arches+=' '$arch
		fi
	done
	rm -f test.c test.o a.out
	echo $detected_arches
	# Don't set sysroot anymore (should be fine for OS X 10.6+)
	export CFLAGS
fi

rm -rf readline-lib
tar xzvf readline-6.3.tar.gz
mv readline-6.3 readline-lib
cd readline-lib
patch -p0 < ../readline63-001
patch -p0 < ../readline63-002
patch -p0 < ../readline63-003
patch -p0 < ../readline63-004
patch -p0 < ../readline63-005
patch -p0 < ../readline63-006
patch -p0 < ../readline63-007
patch -p0 < ../readline63-008
# Force compiler to CC/cc in the case of Darwin
./configure CPPFLAGS='-DNEED_EXTERN_PC -fPIC' $cc_override
# Only the static libraries are required
make static
