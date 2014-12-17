# -*- coding: utf-8 -*-
from django.test import TestCase

from player.models import Room


class TestSignals(TestCase):
    def reload(self, item):
        """
        Reload an item from DB
        """
        return item.__class__.objects.get(pk=item.pk)

    def test_update_token_on_password_change(self):
        r = Room(name="test", password="123")
        r.save()

        first_token = r.token

        r.password = 'wqe'
        r.save()

        self.assertNotEqual(self.reload(r).token, first_token)
