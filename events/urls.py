from django.urls import path
from .views import EventListCreateAPI, EventListDestroyAPI, EventLisFilterAPI


app_name = 'events'


urlpatterns = [
    path('events/', EventListCreateAPI.as_view(), name='create'),
    path('erase/', EventListDestroyAPI.as_view(), name='delete'),
    path('events/repos/<int:repo_id>/', EventLisFilterAPI.as_view(), name='filter_repo'),
    path('events/actors/<int:actor_id>/', EventLisFilterAPI.as_view(), name='filter_actor'),
    path('events/repos/<int:repo_id>/actors/<int:actor_id>/', EventLisFilterAPI.as_view(), name='filter_repo_actor')
]