from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="homepage"),
    path("search-results/", views.search_results_view, name="search-results"),
    # Admin trips urls
    path("trips/admin", views.trips_admin_view, name="trips-admin"),
    path("trips/create", views.create_trip, name="trip-create"),
    path("trips/<int:pk>/update", views.update_trip, name="trip-update"),
    path("trips/<int:pk>/delete", views.delete_trip, name="trip-delete"),
    # Seat selection
    path("trips/<int:pk>/seats", views.select_seat, name="select-seat"),
    # Pay tickets
    path("trips/<int:pk>/payment", views.payment_view, name="payment-view"),
    path("trips/<int:pk>/recipe", views.recipe_view, name="recipe-view"),
]
