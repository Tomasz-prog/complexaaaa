from django.urls import path
from .views import start, zadania, add_task, add_projekt, remove_task, delete_task, check_task, done_task

app_name = 'management'
urlpatterns = [
    path('start', start, name="start"),
    path('zadania/<int:projekt_id>', zadania, name="zadania"),
    path('add_task', add_task, name="add_task"),
    path('add_projekt', add_projekt, name="add_projekt"),
    path('remove_task/<int:zadanie_id>', remove_task, name="remove_task"),
    path('delete_task/<int:projekt_id>', delete_task, name="delete_task"),
    path('check_task/<int:zadanie_id>', check_task, name="check_task"),
    path('done_task/<int:projekt_id>', done_task, name="done_task"),
]
