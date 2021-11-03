from django.contrib import admin

from tasks_api.models import Task, Comment, Section, Project, Label, Color

admin.site.register(Task)
admin.site.register(Color)
admin.site.register(Label)
admin.site.register(Project)
admin.site.register(Section)
admin.site.register(Comment)
