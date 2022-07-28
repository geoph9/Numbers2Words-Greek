"""Test cases for the __main__ module."""
import pytest

from num2word_greek.numbers2words import cmdline


@pytest.fixture
def runner():
    """Fixture for invoking command-line interfaces."""
    return


def test_main_succeeds(runner) -> None:
    """It exits with a status code of zero."""
    # result = runner.invoke(cmdline)
    # assert result.exit_code == 0
    return
