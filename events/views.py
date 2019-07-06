from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView

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
        Django queryset is lazy so
        self.queryset.all() added
        to queryset
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
