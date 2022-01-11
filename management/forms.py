from django.forms import ModelForm
from .models import Task, Projects

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['title', 'task', 'branch', 'timeneed', 'weight', 'level', 'status', 'timedone']

class ProjektForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['project']