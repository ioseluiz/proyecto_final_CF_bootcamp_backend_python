
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # User management
    path('accounts/',include("django.contrib.auth.urls")),
    # Local apps
]
