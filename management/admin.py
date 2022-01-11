from django.contrib import admin
from .models import Task, Projects
#
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'created', 'modified', 'branch', 'weight',
#                     'level', 'status', 'projekt']
#     search_fields = ['title', 'projekt']
#     list_filter = ['branch', 'weight', 'level', 'projekt']

admin.site.register(Task)
admin.site.register(Projects)