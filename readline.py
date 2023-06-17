#
# WARNING
# -------
#
# This module is meant for distributions like ActiveState Python that have
# no default readline module at all. Since there is no builtin readline that
# clashes with this, it is straightforward to enable readline support:
# simply install gnureadline and you are done.
#
# If your Python ships with readline, please don't see this module as an
# encouragement to move site-packages higher up in `sys.path` or to perform
# any other PYTHONPATH shenanigans in order to override the system readline.
# That decision will come back to haunt you.
#
# Instead, run the override_readline script that only overrides readline and
# nothing else, using site customization. Run `python -m override_readline`.
#
from gnureadline import *
from gnureadline import __doc__
