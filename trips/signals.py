from django.db.models.signals import post_save
from django.dispatch import receiver
from trips.models import Bus, Seat, Trip, SeatTrip



# Autogenerate seats instances when a bus instance is created
@receiver(post_save, sender=Bus)
def create_bus_seats(sender, instance,created, **kwargs):
    if created:
        Seat.objects.bulk_create([Seat(seat_number=x,bus=instance) for x in range(1,instance.total_seats + 1)])
        print("Bus creado exitosamente...por lo tanto se crean los asientos correspondientes...")
