from django.shortcuts import render
from .models import Projects, Task
def start(request):

    projects = Projects.objects.all()

    return render(request, "main_management.html", {"projects": projects})

def zadania(request, nr_projekt):
    pass

def add_task(request):
    pass

def edytuj_task(request):
    pass

def check_task(request):
    pass

def add_projekt(requests):
    pass

def done_task(request):
    pass

def remove_task(request):
    pass






