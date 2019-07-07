from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView

from .models import Event
from .serializers import EventSerializer


class EventListCreateAPI(ListCreateAPIView):
    """
    List and Create APIView
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.AllowAny, ]


class EventListDestroyAPI(DestroyAPIView):
    """
    Destroy View of all events
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [permissions.AllowAny, ]

    def get_object(self):
        """
        Overriding to get all events
        self.queryset.all() added
        to overcome queryset laziness
        :return all event object
        """
        return self.queryset.all()

    def destroy(self, request, *args, **kwargs):
        """
        Overriding destroy method
        to change status code
        """
        response = super(EventListDestroyAPI, self).destroy(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

        # instance = self.get_object()
        # self.perform_destroy(instance)
        # return Response(status=status.HTTP_200_OK)


class EventLisFilterAPI(ListAPIView):
    """
    APIView for all filters
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny, ]

    def get_queryset(self):
        """
        ---
        request_serializer: EventSerializer
        response_serializer: EventSerializer
        :return: Filtered queryset by url kwargs
        """
        qs = Event.objects.all().order_by('id')
        repo_id = self.kwargs.get("repo_id")
        actor_id = self.kwargs.get('actor_id')
        if repo_id:
            qs = qs.filter(repo__id=repo_id).order_by('id')
        if actor_id:
            qs = qs.filter(actor__id=actor_id).order_by('id')
        return qs

    def list(self, request, *args, **kwargs):
        response = super(EventLisFilterAPI, self).list(request, *args, **kwargs)
        if not response.data:
            # Changing status code if filtered queryset is blank
            response.status_code = status.HTTP_404_NOT_FOUND
        return response
