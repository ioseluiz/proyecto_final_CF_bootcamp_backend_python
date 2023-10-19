
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from .models import Trip, SeatTrip

from .forms import SearchForm

def home_view(request):

    context = { }
    trip_data = [] # list of dictionaries

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        context['form'] = form
        # check wether it's valid:
        if form.is_valid():
            return HttpResponseRedirect("/results/")
        
    # if a GET method we'll create a blank form
    else:
        info = {}
        form = SearchForm()
        context['form'] = form
        trips = Trip.objects.all()
        for trip in trips:
            date = trip.departure_time.date()
            departure = trip.departure_time.time()

            info = {
                'date': date,
                'departure_time': departure,
                'origin': trip.route.origin,
                'destination': trip.route.destination,
                'duration': trip.route.duration,
                'price': trip.route.price,
                'available_seats': len(SeatTrip.objects.filter(trip=trip).filter(is_sold=False)),
            }
            trip_data.append(info)

        context['trips'] = trip_data

    return render(request, "trips/index.html",context)


