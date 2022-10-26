from django.contrib import admin

from task.models import Task, Comment, Section, Project, Label, Activity, ProjectUser

admin.site.register(Task)
admin.site.register(Activity)
admin.site.register(Label)
admin.site.register(Project)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(ProjectUser)
