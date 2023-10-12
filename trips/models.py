from django.db import models
from django.core.validators import MinLengthValidator

class Company(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Bus(models.Model):
    license_plate = models.CharField(unique=True, max_length=6, validators=[MinLengthValidator(4)])
    total_seats = models.IntegerField()
    brand = models.CharField(max_length=30)

    def __str__(self):
        return f"Bus with license_plate {self.license_plate}"
    
class Seat(models.Model):
    seat_number = models.IntegerField()

    def __str__(self):
        return f"Seat No. {self.seat_number}"


class Terminal(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Route(models.Model):
    distance = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.DecimalField(max_digits=10, decimal_places=1)
    origin = models.ForeignKey(Terminal,on_delete=models.CASCADE, related_name='terminal_origin')
    destination = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='terminal_destination')

    def __str__(self) -> str:
        return f"{self.origin.name} - {self.destination.name}"

class Trip(models.Model):
    departure_time = models.DateTimeField()
    route = models.ForeignKey(Route,on_delete=models.CASCADE, related_name='trip_route')

    def __str__(self):
        return f"Trip scheduled for {self.departure_time} for Route {self.route}"



