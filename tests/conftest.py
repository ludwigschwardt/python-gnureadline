import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--readline-is-ours",
        action="store_true",
        default=False,
        help="identity test passes if readline == gnureadline",
    )
    parser.addoption(
        "--readline-is-not-ours",
        action="store_true",
        default=False,
        help="identity test passes if readline != gnureadline",
    )


@pytest.fixture
def expect_readline_to_be_ours(request):
    """Expect readline == gnureadline, readline != gnureadline or neither."""
    if request.config.getoption("--readline-is-ours"):
        return True
    if request.config.getoption("--readline-is-not-ours"):
        return False
    return None
