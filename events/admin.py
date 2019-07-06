from django.contrib import admin

from .models import Actor, Event, Type, Repo

admin.site.register((Actor, Event, Type, Repo))
