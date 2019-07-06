from django.urls import path
from .views import EventListCreateAPI, EventListDestroyAPI


app_name = 'events'


urlpatterns = [
    path('events/', EventListCreateAPI.as_view(), name='event_create'),
    path('erase/', EventListDestroyAPI.as_view(), name='delete_event'),
]