from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from events.models import Event
from events.serializers import EventSerializer

EVENT_LIST_CREATE_URL = reverse('events:create')
EVENTS_DELETE_URL = reverse('events:delete')


def url_event_list_filtered_by_repo_id(repo_id):
    """
    Return event list filtered by repo_id url
    """
    return reverse('events:filter_repo', args=[repo_id])


def url_event_list_filtered_by_actor_id(actor_id):
    """
    Return event list filtered by repo_id url
    """
    return reverse('events:filter_actor', args=[actor_id])


def url_event_list_filtered_by_repo_id_and_actor_id(repo_id, actor_id):
    """
    Return event list filtered by repo_id url
    """
    return reverse('events:filter_repo_actor', args=[repo_id, actor_id])


def create_event(**params):
    return Event.objects.create(**params)


class EventListCreateTest(TestCase):
    """
    Test event create and list view
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "id": 1,
            "type": {
                "name": "commercial"
            },
            "actor": {
                "login": "1111",
                "avatar_url": "http://i.dailymail.co.uk/i/pix/2015/09/01/18/2BE1E88B00000578-3218613-image-m-5_1441127035222.jpg"
            },
            "repo": {
                "name": "Blog project",
                "url": "https://www.google.com"
            }
        }

    def test_event_create_success(self):
        """
        Event creation with valid payload is successful
        """
        res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_event_get_list(self):
        """
        Test event return list on get method

        """
        self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        res = self.client.get(EVENT_LIST_CREATE_URL)
        events = Event.objects.all().order_by('id')
        serializer = EventSerializer(events, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_event_creation_with_invalid_payloads(self):
        """
        Test event creation with invalid payload
        """
        res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        res2 = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res2.status_code, status.HTTP_400_BAD_REQUEST)


class EventFilteredListTest(TestCase):
    """
    Test event filter by repo_id and or actor id
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            "id": 1,
            "type": {
                "name": "commercial"
            },
            "actor": {
                "login": "1111",
                "avatar_url": "http://i.dailymail.co.uk/i/pix/2015/09/01/18/2BE1E88B00000578-3218613-image-m-5_1441127035222.jpg"
            },
            "repo": {
                "name": "Blog project",
                "url": "https://www.google.com"
            }
        }

    def test_event_filtered_by_repo_id(self):
        """
        Test event list filtered by repo_id
        """
        event_res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        repo_id = event_res.data['repo']['id']
        url = url_event_list_filtered_by_repo_id(repo_id)
        repo_filter = Event.objects.filter(repo__id=repo_id).order_by('id')
        serializer = EventSerializer(repo_filter, many=True)
        repo_id_filter_res = self.client.get(url)
        self.assertEqual(repo_id_filter_res.data, serializer.data)

    def test_event_filtered_by_invalid_repo_id(self):
        """
        Test event list filtered by invalid repo_id
        """
        self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        repo_id = 2
        url = url_event_list_filtered_by_repo_id(repo_id)
        repo_id_filter = self.client.get(url)
        self.assertTrue(repo_id_filter.status_code, status.HTTP_404_NOT_FOUND)

    def test_event_filtered_by_actor_id(self):
        """
        Test event list filtered by actor_id
        """
        event_res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        actor_id = event_res.data['actor']['id']
        url = url_event_list_filtered_by_actor_id(actor_id)
        actor_id_filter = self.client.get(url)
        actor_filter = Event.objects.filter(actor__id=actor_id).order_by('id')
        serializer = EventSerializer(actor_filter, many=True)
        self.assertEqual(actor_id_filter.data, serializer.data)

    def test_event_filtered_by_invalid_actor_id(self):
        """
        Test event list filtered by invalid actor_id
        """
        self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        actor_id = 2
        url = url_event_list_filtered_by_actor_id(actor_id)
        actor_id_filter = self.client.get(url)
        self.assertTrue(actor_id_filter.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtered_by_repo_id_and_actor_id(self):
        """
        Test event list filtered by valid repo_id and valid actor_id
        """
        event_res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        repo_id = event_res.data['repo']['id']
        actor_id = event_res.data['actor']['id']
        url = url_event_list_filtered_by_repo_id_and_actor_id(repo_id, actor_id)
        repo_actor_id_filter = self.client.get(url)
        event_repo_actot = Event.objects.filter(repo__id=repo_id, actor__id=actor_id).order_by('id')
        serializer = EventSerializer(event_repo_actot, many=True)
        self.assertEqual(repo_actor_id_filter.data, serializer.data)

    def test_filter_by_invalid_repo_id_and_valid_actor_id(self):
        """
        Test event list filtered by invalid repo_id and valid actor_id

        """
        event_res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        repo_id = 2
        actor_id = event_res.data['actor']['id']
        url = url_event_list_filtered_by_repo_id_and_actor_id(repo_id, actor_id)
        repo_actor_id_filter = self.client.get(url)
        self.assertTrue(repo_actor_id_filter.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_invalid_actor_id_and_valid_repo_id(self):
        """
        Test event list filtered by invalid actor_id and valid repo_id

        """
        event_res = self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        actor_id = 2
        repo_id = event_res.data['repo']['id']
        url = url_event_list_filtered_by_repo_id_and_actor_id(repo_id, actor_id)
        repo_actor_id_filter = self.client.get(url)
        self.assertTrue(repo_actor_id_filter.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_invalid_actor_id_and_invalid_repo_id(self):
        """
        Test event list filtered by invalid actor_id and invalid repo_id
        """
        self.client.post(EVENT_LIST_CREATE_URL, self.payload, format='json')
        repo_id = 2
        actor_id = 2
        url = url_event_list_filtered_by_repo_id_and_actor_id(repo_id, actor_id)
        res = self.client.get(url)
        self.assertTrue(res.status_code, status.HTTP_404_NOT_FOUND)


class EventsDeleteTest(TestCase):
    """
    Test all events delete
    """
    def setUp(self) -> None:
        self.client = APIClient()
        self.payload1 = {
            "id": 1,
            "type": {
                "name": "commercial"
            },
            "actor": {
                "login": "1111",
                "avatar_url": "http://i.dailymail.co.uk/i/pix/2015/09/01/18/2BE1E88B00000578-3218613-image-m-5_1441127035222.jpg"
            },
            "repo": {
                "name": "Blog project",
                "url": "https://www.google.com"
            }
        }

        self.payload2 = {
            "id": 2,
            "type": {
                "name": "commercial"
            },
            "actor": {
                "login": "1111",
                "avatar_url": "http://i.dailymail.co.uk/i/pix/2015/09/01/18/2BE1E88B00000578-3218613-image-m-5_1441127035222.jpg"
            },
            "repo": {
                "name": "Blog project",
                "url": "https://www.google.com"
            }
        }

    def test_delete_all_events(self):
        """
        Test events delete
        """
        self.client.post(EVENT_LIST_CREATE_URL, self.payload1, format='json')
        self.client.post(EVENT_LIST_CREATE_URL, self.payload2, format='json')
        res = self.client.delete(EVENTS_DELETE_URL)
        self.assertTrue(res.status_code, status.HTTP_200_OK)
