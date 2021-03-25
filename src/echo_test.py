"""
echo(echo.py) Gives access to echo
error(error.py) Gives access to error classes
pytest: Gives access to pytest command (for testing)
"""
import pytest
import echo
from error import InputError



def test_echo():
    """
    Testing successful uses of echo
    """
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    """
    Testing unsuccessful uses of echo
    """
    with pytest.raises(InputError):
        assert echo.echo("echo")
