import sys
from os import path


def test_pkg_import():
    """import without touching sys.path"""
    from python_readline import readline


def test_import():
    """A very basic unittest; can we 'import readline'?"""
    msg = r'''
    readline.so was not installed properly into site-packages.
    'import readline' imports %s
    sys.path:\n%s'''
    # Put site-packages in front of sys.path so we don't end up importing the global
    # readline.so
    save_sys_path = list(sys.path)
    sys.path = (
        [p for p in sys.path if 'site-packages' in p] + \
        [p for p in sys.path if 'site-packages' not in p])
    
    import readline
    try:
        assert 'site-packages' in path.dirname(readline.__file__), \
            msg % (readline.__file__, '\n'.join(sys.path))
    finally:
        sys.path = save_sys_path
