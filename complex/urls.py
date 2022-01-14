from django.contrib import admin
from django.urls import path, include
from .views import glowna

app_name = 'complex'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pressure/',include('pressure.urls')),
    path('culture/',include('culture.urls')),
    path('management/',include('management.urls')),
    path('kitchen/',include('kitchen.urls')),
    path('', glowna)
]
