#
# Install readline override code and explain what happened.
#
# Run this as `python -m override_readline`, picking the appropriate Python
# executable. This runs on both Python 2.7 and 3.x, hence the use of `io`,
# `os.path` and explicit Unicode.
#
# First target sitecustomize.py (better for venvs and system-wide overrides)
# and then fall back to usercustomize.py if we don't have permission.
#
# Based on the script in https://stackoverflow.com/a/38606990. Thanks, Alastair!
#

import importlib
import io
import os
import os.path
import site


HEADER = """
This script will attempt to install an override in Python's site customization
modules that replaces the default readline module with gnureadline.

First check the existing readline module and its replacement
------------------------------------------------------------
"""

OVERRIDE = u"""
# Added by override_readline script in gnureadline package

import sys

def add_override_message_to_hook():
    try:
        old_hook = sys.__interactivehook__
    except AttributeError:
        return
    def hook():
        old_hook()
        print("Using GNU readline instead of the default readline (see {filename})")
    sys.__interactivehook__ = hook

try:
    import gnureadline as readline
    add_override_message_to_hook()
except ImportError:
    import readline
sys.modules["readline"] = readline

# End of override_readline block
"""


def check_module(module_name):
    """Attempt to import `module_name` and report basic features."""
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print("Module {name}: not found".format(name=module_name))
        return None
    style = "libedit" if "libedit" in module.__doc__ else "GNU readline"
    kwargs = dict(name=module_name, style=style, path=module.__file__)
    print("Module {name}: based on {style}, {path}".format(**kwargs))
    return module


def install_override(customize_path):
    """Add override to specified customization module and report back."""
    site_directory, customize_filename = os.path.split(customize_path)
    banner = "\nAdd override to {filename}\n--------------------------------\n"
    print(banner.format(filename=customize_filename))
    if not os.path.exists(site_directory):
        os.makedirs(site_directory)
        print("Created site directory at {dir}".format(dir=site_directory))
    file_mode = "r+t" if os.path.exists(customize_path) else "w+t"
    with io.open(customize_path, file_mode) as customize_file:
        if file_mode == "w+t":
            print("Created customize module at {path}".format(path=customize_path))
        existing_text = customize_file.read()
        override = OVERRIDE.format(filename=customize_filename)
        if override in existing_text:
            print("Readline override already enabled, nothing to do")
        else:
            # File pointer should already be at the end of the file after read()
            customize_file.write(override)
            kwargs = dict(filename=customize_filename)
            print("The following override was added to {filename}:".format(**kwargs))
            print("\n    ".join(override.split("\n")))
            print("Feel free to remove this (or even the entire file) if not needed anymore.")
            print("(It is also pretty harmless to leave it in there...)")


def override_usercustomize():
    if not site.ENABLE_USER_SITE:
        print(
            "Could not override usercustomize.py because user site "
            "directory is not enabled (maybe you are in a virtualenv?)"
        )
        return False
    try:
        import usercustomize
    except ImportError:
        path = os.path.join(site.getusersitepackages(), "usercustomize.py")
    else:
        path = usercustomize.__file__
    try:
        install_override(path)
    except OSError:
        print("Could not override usercustomize.py because file open/write failed")
        return False
    else:
        return True


def override_sitecustomize():
    try:
        import sitecustomize
    except ImportError:
        path = os.path.join(site.getsitepackages()[0], "sitecustomize.py")
    else:
        path = sitecustomize.__file__
    try:
        install_override(path)
    except OSError:
        print("Could not override sitecustomize.py because file open/write failed")
        return False
    else:
        return True


print(HEADER)
readline = check_module("readline")
gnureadline = check_module("gnureadline")
if not gnureadline:
    raise RuntimeError("Please install gnureadline first")
if readline == gnureadline:
    print("It looks like readline is already overridden, but let's make sure")

if not override_usercustomize():
    override_sitecustomize()
