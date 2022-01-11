from django.urls import path
from .views import main

app_name = 'pressure'
urlpatterns = [
    path('main/', main, name="main")
]
