from django.test import TestCase as DjangoTestCase
from music.models import Room, Events


class TestCase(DjangoTestCase):
    def reload(self, item):
        """
        Reload an item from DB
        """
        return item.__class__.objects.get(pk=item.pk)

    def setUp(self):
        self.room = Room(name="a", password="a")
        self.room.save()

    def tearDown(self):
        for room, event in Events.get_all().items():
            if event is not None:
                event.cancel()

