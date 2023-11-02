import uuid
from datetime import timedelta
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.timezone import now

from accounts.models import CustomUser

BUS_TYPES = (
    (53,53),
)
 
class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Bus(models.Model):
    license_plate = models.CharField(unique=True, max_length=6, validators=[MinLengthValidator(4)])
    total_seats = models.IntegerField(choices=BUS_TYPES)
    brand = models.CharField(max_length=30)
    company= models.ForeignKey(Company, on_delete=models.CASCADE,related_name="owner_bus")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.license_plate}"
    
class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    row = models.CharField(max_length=1)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="bus_seat")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Bus:{ self.bus.license_plate} Seat No. {self.row}-{self.seat_number}"
    


class Terminal(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    origin = models.ForeignKey(Terminal,on_delete=models.CASCADE, related_name='terminal_origin')
    destination = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='terminal_destination')
    distance = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.DecimalField(max_digits=10, decimal_places=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.origin.name} - {self.destination.name}"

class Trip(models.Model):
    departure_time = models.DateTimeField()
    route = models.ForeignKey(Route,on_delete=models.CASCADE, related_name='trip_route')
    #company = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trip_company')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bus_assignes')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
     
    @property
    def calc_distance(self):
        duration = self.route.duration
        return self.departure_time + timedelta(hours=duration)

    def __str__(self):
        return f"Trip: {self.bus.license_plate} - {self.departure_time} for Route {self.route}"
    
class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number_seats = models.PositiveIntegerField()
    total_price = models.FloatField()
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.order_number}"

class SeatTrip(models.Model):
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE, related_name="seat_bus")
    trip = models.ForeignKey(Trip,on_delete=models.CASCADE, related_name="trip_seat")
    is_sold = models.BooleanField(default=False)
    order = models.ForeignKey(Order,on_delete=models.CASCADE, related_name="order_seat_trip",blank=True,null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trip.departure_time}, Route: {self.trip.route.origin}-{self.trip.route.destination}"
    






