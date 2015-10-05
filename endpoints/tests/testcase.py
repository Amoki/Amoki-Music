from django.test import TestCase
from rest_framework.test import APIClient
from player.models import Room, events


class EndpointTestCase(TestCase):
    def reload(self, item):
        """
        Reload an item from DB
        """
        return item.__class__.objects.get(pk=item.pk)

    def setUp(self):
        self.r = Room(name="a", password="a")
        self.r.save()

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.reload(self.r).token)

    def tearDown(self):
        for room, event in events.items():
            if event is not None:
                event.cancel()
