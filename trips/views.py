from django.shortcuts import render
from django.views.generic import ListView

from .models import Route

class HomeView(ListView):
    model = Route
    template_name = "trips/index.html"
