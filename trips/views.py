from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

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
    #print(date_requested)
    #print(type(date_requested))
    # Get route from terminal_from and terminal_to
    route = Route.objects.get(origin=terminal_from, destination=terminal_to)
    #print(route)
    # Get trips for that route
    trips = Trip.objects.filter(route=route, departure_time__date=date_requested)
    #print(trips)

    for trip in trips:
        date = trip.departure_time.date()
        departure = trip.departure_time.time()

        info = {
            'id': trip.id,
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
@user_passes_test(lambda user: user.is_superuser)
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
        Trip.objects.create(departure_time=trip_datetime,
                            route=trip_route,
                            bus=trip_bus)
        
        trips = Trip.objects.all()
        context['trips'] = trips
        return render(request, 'trips/components/table-trips.html',context)
        

def update_trip(request, pk):
    print(pk)
    context = {}
    try:
        trip = Trip.objects.get(id=pk)
    except:
        raise "Trip not found"
    
    context['trip'] = trip
    return render(request, 'trips/components/trip_edit.html',context)

def delete_trip(request, pk):
    Trip.objects.get(id=pk).delete()
    trips = Trip.objects.all()
    context = {'trips': trips}
    return render(request, "trips/components/table-trips.html",context)

@login_required
def select_seat(request, pk):
    context = {}
    row_seat = {}
    rows = []
    
    trip = Trip.objects.get(id=pk)
    # Get the tickets for the trip
    rows_letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]
    for row in rows_letters:
        seat_trip = SeatTrip.objects.filter(trip=trip)
        result = seat_trip.filter(seat__row=row)
        #print(result)
        for re in result:
            if re.is_sold:
                print(f"{re.trip.departure_time}:{re.seat}")
        info = {
            'seats':result,
            'count': len(result),
            'letter': row,
        }
        rows.append(info)
    
    context['trip'] = trip
    context['rows'] = rows
    return render(request, "trips/seat-selection.html", context)


def payment_view(request, pk):
    context = {}
    # Get Trip
    trip = Trip.objects.get(id=pk)
    seats_string = request.POST.get('selected-seats')
    selected_seats =seats_string.split(",")
    data_seats = []
    total_price = 0
    for seat in selected_seats:
      info = {
          "row": seat[0],
          "number": seat[1:],
          "price": trip.route.price,
      }
      total_price += trip.route.price
      data_seats.append(info)
    #print(data_seats)
    context['seats'] = data_seats
    context['total_price'] = total_price
    context['date'] = trip.departure_time
    context['route_origin'] = trip.route.origin
    context['route_destination'] = trip.route.destination
    context['trip_id'] = pk
    context['seats_string'] = seats_string

    

    return render(request, 'trips/components/payment.html', context)


def recipe_view(request, pk):
    context = {}
    # Get Trip
    trip = Trip.objects.get(id=pk)
    # Read seats-string
    seats_string = request.POST.get('seats')
    selected_seats =seats_string.split(",")
    data_seats = []
    total_price = 0
    for seat in selected_seats:
      info = {
          "row": seat[0],
          "number": seat[1:],
          "price": trip.route.price,
      }
      total_price += trip.route.price
      data_seats.append(info)

    # Update is_sold in SeatTrip
    seats_objects = SeatTrip.objects.filter(trip=trip)
    print(seats_objects)
    for seat in data_seats:
        print(seat['row'])
        bought_seat = seats_objects.filter(seat__row=seat['row']).filter(seat__seat_number=seat['number'])
        print(bought_seat)
        bought_seat.update(is_sold=True)
        print('Seat Updated...')

    

    context['seats'] = data_seats
    context['total_price'] = total_price
    context['date'] = trip.departure_time
    context['route_origin'] = trip.route.origin
    context['route_destination'] = trip.route.destination
    context['trip_id'] = pk
    context['seats_string'] = seats_string
    context['date'] = datetime.now()


    return render(request, 'trips/components/recipe.html', context)



