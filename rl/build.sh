#! /bin/bash
set -e

# If we are on Mac OS X, look for the latest SDK and do a universal build
if [ `uname` == "Darwin" ]; then
  LATEST_SDK=''
  for sdk_dir in /Developer/SDKs/*; do
    LATEST_SDK=$sdk_dir
  done
  # Do not add -isysroot on 10.4, as old systems with XCode < 2.4 do not like it
  if [[ $LATEST_SDK == /Developer/SDKs/MacOSX10.4u.sdk ]]; then
    CFLAGS=''
    LDFLAGS=''
  elif [[ $LATEST_SDK ]]; then
    CFLAGS='-isysroot '${LATEST_SDK}
    LDFLAGS='-syslibroot,'${LATEST_SDK}
  fi
  # Add all architectures that we find asm support for in gcc
  if [ -d /usr/libexec/gcc/darwin ]; then
    archs=''
    for as_path in /usr/libexec/gcc/darwin/*; do
      architecture=${as_path##*/}
      if (gcc -v -arch ${architecture} > /dev/null 2>&1); then
        CFLAGS+=' -arch '${architecture}
        LDFLAGS+=' -arch '${architecture}
        archs+=' '${architecture}
      fi
    done
    echo 'Building readline library with architectures:'${archs}
  fi
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
