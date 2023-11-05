from django.contrib import admin

from .models import Terminal, Route, Trip, Bus, Seat, Company, SeatTrip

admin.site.register(Terminal)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Bus)
admin.site.register(Seat)
admin.site.register(Company)
admin.site.register(SeatTrip)
