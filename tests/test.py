import sys
from os import path


def test_import_new():
    """import gnureadline without touching sys.path"""
    import gnureadline


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

    import gnureadline
    assert readline.parse_and_bind is gnureadline.parse_and_bind


def test_history_manipulation():
    """Basic readline functionality checks taken from Lib/test/test_readline.py."""
    import gnureadline

    gnureadline.clear_history()
    gnureadline.add_history("first line")
    gnureadline.add_history("second line")

    assert gnureadline.get_history_item(0) is None
    assert gnureadline.get_history_item(1) == "first line"
    assert gnureadline.get_history_item(2) == "second line"

    gnureadline.replace_history_item(0, "replaced line")
    assert gnureadline.get_history_item(0) is None
    assert gnureadline.get_history_item(1) == "replaced line"
    assert gnureadline.get_history_item(2) == "second line"

    assert gnureadline.get_current_history_length() == 2

    gnureadline.remove_history_item(0)
    assert gnureadline.get_history_item(0) is None
    assert gnureadline.get_history_item(1) == "second line"

    assert gnureadline.get_current_history_length() == 1
