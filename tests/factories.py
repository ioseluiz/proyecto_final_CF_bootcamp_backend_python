import factory

from accounts.models import CustomUser
from trips.models import Route, Terminal


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    password = "test"
    username = "test"
    email = "test@test.com"
    is_superuser = True
    is_staff = True


class TerminalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Terminal

    name = "TestName"

class Terminal1Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = Terminal

    name = "TestName1"

class RouteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Route

    origin = factory.SubFactory(TerminalFactory)
    distance = 370
    duration = 5.0
    price = 12.0


