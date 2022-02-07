from django.contrib import admin

from users.models import Team, MyUser

admin.site.register(Team)
admin.site.register(MyUser)
