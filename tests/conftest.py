from pytest_factoryboy import register

from tests.factories import TerminalFactory, Terminal1Factory, RouteFactory, UserFactory

register(TerminalFactory)
register(Terminal1Factory)
register(RouteFactory)
register(UserFactory)