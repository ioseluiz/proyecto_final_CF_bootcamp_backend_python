from django.db.models.signals import post_save
from django.dispatch import receiver
from trips.models import Bus, Seat, Trip, SeatTrip



# Autogenerate seats instances when a bus instance is created
@receiver(post_save, sender=Bus)
def create_bus_seats(sender, instance,created, **kwargs):
    seats = []
    rows = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]
    if created:
        for i in range(1,14):
            if i<13:
                for j in range(1,5):
                    seats.append(Seat(seat_number=j, row=rows[i-1], bus=instance))
            else:
                for j in range(1,6):
                    seats.append(Seat(seat_number=j, row=rows[i-1], bus=instance))
        Seat.objects.bulk_create(seats)
        #Seat.objects.bulk_create([Seat(seat_number=x,bus=instance) for x in range(1,instance.total_seats + 1)])
        print("Bus creado exitosamente...por lo tanto se crean los asientos correspondientes...")
    else:
        print("Bus updated")

# Autogenerate tickets instances when a trip is created
@receiver(post_save, sender=Trip)
def create_tickets(sender, instance, created, **kwargs):
    if created:
        # get bus of trip instance
        trip_bus = instance.bus
        seats = Seat.objects.filter(bus=trip_bus)
        print(seats)


        SeatTrip.objects.bulk_create([SeatTrip(seat=seat, trip=instance) for seat in seats])