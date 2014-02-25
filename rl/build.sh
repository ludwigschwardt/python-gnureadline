#! /bin/bash
set -e

# If we are on Mac OS X, try to do a universal build, as this will allow the
# Python extension to pick the architectures it needs from the static library
if [ `uname` == "Darwin" ]; then
	detected_arches="Detected architectures:"
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
tar xzvf readline-6.2.tar.gz
mv readline-6.2 readline-lib
cd readline-lib
patch -p0 < ../readline62-001
patch -p0 < ../readline62-002
patch -p0 < ../readline62-003
patch -p0 < ../readline62-004
patch -p0 < ../readline62-005a
./configure CPPFLAGS='-DNEED_EXTERN_PC -fPIC'
make
