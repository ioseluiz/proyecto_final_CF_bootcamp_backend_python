import uuid, json
from datetime import datetime
from django.http import QueryDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Trip, SeatTrip, Route, Bus, Order
from .utils import convert_seat_data, get_total_price, group_seats_by_row

from .forms import SearchForm


def home_view(request):
    context = {}
    form = SearchForm()
    context["form"] = form
    return render(request, "trips/index.html", context)


def search_results_view(request, *args, **kwargs):
    trip_data = []  # list of dictionaries
    context = {}
    info = {}
    # Read POST request parameters
    terminal_from = request.POST.get("name_from")
    terminal_to = request.POST.get("name_to")
    date_requested = request.POST.get("date")  # str
    # Convert str to datetime
    date_requested = datetime.strptime(date_requested, "%Y-%m-%d").date()
    # Get route from terminal_from and terminal_to
    route = Route.objects.get(origin=terminal_from, destination=terminal_to)
    # print(route)
    # Get trips for that route
    trips = Trip.objects.filter(route=route, departure_time__date=date_requested)
    # print(trips)

    for trip in trips:
        date = trip.departure_time.date()
        departure = trip.departure_time.time()

        info = {
            "id": trip.id,
            "date": date,
            "departure_time": departure,
            "origin": trip.route.origin,
            "destination": trip.route.destination,
            "duration": trip.route.duration,
            "price": trip.route.price,
            "available_seats": len(
                SeatTrip.objects.filter(trip=trip).filter(is_sold=False)
            ),
        }
        trip_data.append(info)

    context["trips"] = trip_data

    return render(request, "trips/components/trips-list-elements.html", context)


# CRUD Model Trips
@user_passes_test(lambda user: user.is_superuser)
def trips_admin_view(request):
    context = {}
    routes = Route.objects.all()
    buses = Bus.objects.all()
    trips = Trip.objects.all()
    context["routes"] = routes
    context["buses"] = buses
    context["trips"] = trips
    return render(request, "trips/admin_trips.html", context)


def create_trip(request):
    context = {}
    if request.POST:
        # Read parameters
        trip_datetime = request.POST.get("trip_datetime")  # str
        trip_datetime = datetime.strptime(trip_datetime, "%Y-%m-%dT%H:%M")
        trip_route = request.POST.get("trip_route")
        trip_route = Route.objects.get(id=trip_route)
        trip_bus = request.POST.get("trip_bus")
        trip_bus = Bus.objects.get(id=trip_bus)
        Trip.objects.create(
            departure_time=trip_datetime, route=trip_route, bus=trip_bus
        )

        trips = Trip.objects.all()
        context["trips"] = trips
        return render(request, "trips/components/table-trips.html", context)


def update_trip(request, pk):
    print(pk)
    context = {}
    if request.method == "PUT":
        print(request)
        body_unicode = request.body.decode("utf-8")
        print(body_unicode)
        # parse body parameters
        put = QueryDict(request.body)
        trip_datetime = put.get("trip_datetime")
        trip_route = put.get("trip_route")
        trip_bus = put.get("trip_bus")

    try:
        Trip.objects.filter(id=pk).update(
            departure_time=trip_datetime,
            route=trip_route,
            bus=trip_bus,
        )
    except:
        raise "Trip not found"

    trips = Trip.objects.all().order_by("departure_time")
    context = {"trips": trips}

    return render(request, "trips/components/table-trips.html", context)


def delete_trip(request, pk):
    Trip.objects.get(id=pk).delete()
    trips = Trip.objects.all()
    context = {"trips": trips}
    return render(request, "trips/components/table-trips.html", context)


@login_required
def select_seat(request, pk):
    context = {}
    row_seat = {}
    rows = []
    trip = Trip.objects.get(id=pk)
    rows = group_seats_by_row(trip)
    context["trip"] = trip
    context["rows"] = rows
    return render(request, "trips/seat-selection.html", context)


def payment_view(request, pk):
    context = {}
    # Get Trip
    trip = Trip.objects.get(id=pk)
    seats_string = request.POST.get("selected-seats")
    selected_seats = seats_string.split(",")

    # Convert Seat Data
    data_seats = convert_seat_data(trip, selected_seats)
    total_price = get_total_price(data_seats)

    # Context Data
    context["seats"] = data_seats
    context["total_price"] = total_price
    context["date"] = trip.departure_time
    context["route_origin"] = trip.route.origin
    context["route_destination"] = trip.route.destination
    context["trip_id"] = pk
    context["seats_string"] = seats_string

    return render(request, "trips/components/payment.html", context)


def recipe_view(request, pk):
    context = {}
    # Get Trip
    trip = Trip.objects.get(id=pk)
    # Read seats-string
    seats_string = request.POST.get("seats")
    selected_seats = seats_string.split(",")
    number_seats = len(selected_seats)
    data_seats = []

    # Convert Seat Data
    data_seats = convert_seat_data(trip, selected_seats)
    total_price = get_total_price(data_seats)

    # Update is_sold in SeatTrip
    seats_objects = SeatTrip.objects.filter(trip=trip)
    print(seats_objects)
    for seat in data_seats:
        print(seat["row"])
        bought_seat = seats_objects.filter(seat__row=seat["row"]).filter(
            seat__seat_number=seat["number"]
        )
        print(bought_seat)
        bought_seat.update(is_sold=True)
        print("Seat Updated...")

    # Create Order
    Order.objects.create(
        order_number=uuid.uuid4(),
        user=request.user,
        total_price=total_price,
        number_seats=number_seats,
    )

    # Context Data
    context["seats"] = data_seats
    context["total_price"] = total_price
    context["date"] = trip.departure_time
    context["route_origin"] = trip.route.origin
    context["route_destination"] = trip.route.destination
    context["trip_id"] = pk
    context["seats_string"] = seats_string
    context["date"] = datetime.now()

    return render(request, "trips/components/recipe.html", context)
