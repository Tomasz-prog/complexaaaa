from django.urls import path
from .views import formularz

app_name = 'kitchen'
urlpatterns = [
    path('formularz/', formularz, name="formularz")
]
