import _gnureadline

# future imports of 'readline' should get gnureadline
import sys
sys.modules['readline'] = _gnureadline
del sys

# import everything from the extension
from _gnureadline import *

