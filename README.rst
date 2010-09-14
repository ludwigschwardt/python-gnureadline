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
