from django.contrib import admin

from tasks.models import Task, Activity, Comment, Section, Project, Label, Color

admin.site.register(Task)
admin.site.register(Color)
admin.site.register(Label)
admin.site.register(Project)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Activity)
