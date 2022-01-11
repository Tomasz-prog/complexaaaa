from django.urls import path
from .views import main

app_name = 'culture'
urlpatterns = [
    path('main', main, name="main")
]
