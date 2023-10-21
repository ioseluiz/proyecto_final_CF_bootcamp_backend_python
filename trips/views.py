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


# CRUD Model Route


# CRUD Model Trips
def trips_admin_view(request):
    context = { }
    routes = Route.objects.all()
    buses = Bus.objects.all()
    trips = Trip.objects.all()
    context['routes'] = routes
    context['buses'] = buses
    context['trips'] = trips
    return render(request, 'trips/admin_trips.html',context)


def get_trip(request):
    pass
    


def create_trip(request):
    context = {}
    if request.POST:
        # Read parameters
        trip_datetime = request.POST.get('trip_datetime') #str
        print(trip_datetime)
        trip_datetime = datetime.strptime(trip_datetime, '%Y-%m-%dT%H:%M')
        trip_route = request.POST.get('trip_route')
        trip_route = Route.objects.get(id=trip_route)
        print(trip_route)
        trip_bus = request.POST.get('trip_bus')
        trip_bus = Bus.objects.get(id=trip_bus)
        # data = {
        #     'departure_time': trip_datetime,
        #     'route': trip_route,
        #     'trip_bus': trip_bus,
        # }
        # print(data)
        
        Trip.objects.create(departure_time=trip_datetime,
                            route=trip_route,
                            bus=trip_bus)
        
        trips = Trip.objects.all()
        context['trips'] = trips
        return render(request, 'trips/components/table-trips.html',context)
        

# def update_trip(request, pk):
#     trip = Trip.objects.get(id=pk)
#     if request.method == "PUT":
        
#         pass

def delete_trip(request, pk):
    Trip.objects.get(id=pk).delete()
    trips = Trip.objects.all()
    context = {'trips': trips}
    return render(request, "trips/components/table-trips.html",context)



