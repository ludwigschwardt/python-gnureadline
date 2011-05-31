#! /bin/bash
set -e

# If we are on Mac OS X, look for the latest SDK and do a universal build
if [ `uname` == "Darwin" ]; then
  LATEST_SDK=''
  for sdk_dir in /Developer/SDKs/*; do
    LATEST_SDK=$sdk_dir
  done
  if [[ $LATEST_SDK == /Developer/SDKs/MacOSX10.4u.sdk ]]; then
    CFLAGS=''
    LDFLAGS=''
  elif [[ $LATEST_SDK ]]; then
    CFLAGS='-isysroot '${LATEST_SDK}
    LDFLAGS='-syslibroot,'${LATEST_SDK}
  fi
  # Add all architectures that we find support for in gcc
  for architecture in i386 x86_64 ppc ppc64; do 
    if (gcc -v -arch ${architecture}); then
      CFLAGS+=' -arch '${architecture}
      LDFLAGS+=' -arch '${architecture}
    fi
  done
  export CFLAGS
  export LDFLAGS
fi

rm -rf readline-lib
tar xzvf readline-6.2.tar.gz
mv readline-6.2 readline-lib
cd readline-lib
patch -p0 < ../readline62-001
./configure CPPFLAGS='-DNEED_EXTERN_PC -fPIC'
make
