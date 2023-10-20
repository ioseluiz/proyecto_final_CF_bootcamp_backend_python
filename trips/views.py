from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage

from .models import Trip, SeatTrip, Route, Bus

from .forms import SearchForm

def home_view(request):

    context = { }

    form = SearchForm()
    context['form'] = form
    

    return render(request, "trips/index.html",context)


def search_results_view(request, *args, **kwargs):
    trip_data = [] # list of dictionaries
    context = {}
    info = {}
    # Read POST request parameters
    terminal_from = request.POST.get('name_from')
    terminal_to = request.POST.get('name_to')
    date_requested = request.POST.get('date') #str
    # Convert str to datetime
    date_requested = datetime.strptime(date_requested,"%Y-%m-%d").date()
    print(date_requested)
    print(type(date_requested))
    # Get route from terminal_from and terminal_to
    route = Route.objects.get(origin=terminal_from, destination=terminal_to)
    print(route)
    # Get trips for that route
    trips = Trip.objects.filter(route=route, departure_time__date=date_requested)
    print(trips)

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

    return render(request, 'trips/components/trips-list-elements.html', context)

def trips_admin_view(request):
    context = { }
    routes = Route.objects.all()
    buses = Bus.objects.all()
    trips = Trip.objects.all()
    context['routes'] = routes
    context['buses'] = buses
    context['trips'] = trips
    return render(request, 'trips/admin_trips.html',context)


def list_trips(request):
    pass


def create_trip(request):
    pass

def update_trip(request):
    pass

def delete_trip(request):
    pass



