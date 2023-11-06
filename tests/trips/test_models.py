import pytest

pytestmark = pytest.mark.django_db


class TestTerminalModel:
    def test_str_return(self, terminal_factory):
        terminal = terminal_factory(name="test-terminal")
        assert terminal.__str__() == "test-terminal"





