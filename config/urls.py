from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # User management
    path('accounts/', include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    # Local apps
    path('',include('trips.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
