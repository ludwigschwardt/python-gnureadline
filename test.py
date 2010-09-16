import sys
from os import path


# Put site-packages in front of sys.path so we don't end up importing the global
# readline.so
sys.path = (
    [p for p in sys.path if 'site-packages' in p] + \
    [p for p in sys.path if 'site-packages' not in p])


def test_import():
    """A very basic unittest; can we 'import readline'?"""
    msg = r'''
readline.so was not installed properly into site-packages.
'import readline' imports %s
sys.path:\n%s'''
    import readline
    assert 'site-packages' in path.dirname(readline.__file__), \
            msg % (readline.__file__, '\n'.join(sys.path))
