from pygments.style import Style

from hiss.themes.tomorrow import Tomorrow


def test_wow_what_a_stupid_test():
    assert isinstance(Tomorrow(), Style)
