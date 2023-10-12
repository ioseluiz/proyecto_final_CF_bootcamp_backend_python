from django.http import HttpResponseRedirect
from django.shortcuts import render



from .forms import SearchForm

def home_view(request):

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check wether it's valid:
        if form.is_valid():
            return HttpResponseRedirect("/results/")
        
    # if a GET method we'll create a blank form
    else:
        form = SearchForm()

    return render(request, "trips/index.html",{"form": form})


