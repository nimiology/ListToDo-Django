from django.contrib import admin

from users.models import Setting, Team

admin.site.register(Setting)
admin.site.register(Team)
