import sys
from os import path

import gnureadline

# Since the tests are non-interactive we don't expect readline to be imported.
# Unfortunately it manages to sneak in on Python 3.13.0 via pytest and pdb (see
# python/cpython#112948 and pytest/src/_pytest/debugging.py). Enforce its absence.
if 'readline' in sys.modules:
    del sys.modules['readline']


def import_alternative_readline_module():
    """This forcibly imports our alternative readline.py module over the standard one."""
    # This will check that the alternative readline.py installed by gnureadline
    # is accessible if it is in front of the standard library version.
    #
    # This is only to ensure that the package works out of the box on a system
    # without any readline in the standard library, like the old ActivePython.
    #
    # THIS IS NOT RECOMMENDED AS A SOLUTION TO OVERRIDE READLINE IN GENERAL...
    # See the override_readline.py module instead.
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
    return readline


def test_identity_of_readline_module(expect_readline_to_be_ours):
    """Check that `import readline` has the desired effect."""
    # If there is no explicit instruction, check the alternative readline.py module
    if expect_readline_to_be_ours is None:
        readline = import_alternative_readline_module()
    else:
        # Gnureadline provides fallback even if Python has no readline so this is safe
        import readline
    # Normal readline modules are extensions but our alternative module is pure Python
    if readline.__file__.endswith('readline.py'):
        # We are either forcing the alternative or there is no native readline.
        # Either way, we might as well accept that the module will be gnureadline.
        expect_readline_to_be_ours = True
    if expect_readline_to_be_ours:
        # Compare main method instead of module because it works for alternative module
        assert readline.parse_and_bind is gnureadline.parse_and_bind, \
            "Expected readline == gnureadline but they differ"
    else:
        assert readline.parse_and_bind is not gnureadline.parse_and_bind, \
            "Expected readline != gnureadline but they are the same"


def test_history_manipulation():
    """Basic readline functionality checks taken from Lib/test/test_readline.py."""
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
