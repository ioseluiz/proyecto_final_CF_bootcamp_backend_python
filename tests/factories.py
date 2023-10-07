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

# class RouteFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Route
    
#     distance = 300.59
#     duration = 4.2

    