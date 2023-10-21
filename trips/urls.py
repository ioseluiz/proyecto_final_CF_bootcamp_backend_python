from django.urls import path

from . import views

urlpatterns = [
    path("",views.home_view, name="homepage"),
    path("search-results/",views.search_results_view, name="search-results"),
    path("admin-trips",views.trips_admin_view, name="trips-admin"),
    path("create/", views.create_trip, name="trip-create"),
    # path("<int:pk/update",views.update_trip, name="trip-update"),
    path("<int:pk>/delete",views.delete_trip, name="trip-delete"),
    

]