from .models import SeatTrip


def group_seats_by_row(trip):
    rows = []
    rows_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    for row in rows_letters:
        seat_trip = SeatTrip.objects.filter(trip=trip)
        result = seat_trip.filter(seat__row=row).order_by("seat__seat_number")
        for re in result:
            if re.is_sold:
                print(f"{re.trip.departure_time}:{re.seat}")
        info = {
            "seats": result,
            "count": len(result),
            "letter": row,
        }
        rows.append(info)

    return rows


def convert_seat_data(trip, selected_seats):
    data_seats = []
    for seat in selected_seats:
        info = {
            "row": seat[0],
            "number": seat[1:],
            "price": trip.route.price,
        }
        data_seats.append(info)

    return data_seats


def get_total_price(seats):
    total_price = 0
    for seat in seats:
        total_price += seat["price"]
    return total_price
