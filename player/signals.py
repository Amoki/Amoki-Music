# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from player.models import Room, events


@receiver(pre_save, sender=Room)
def add_event(sender, instance, **kwargs):
	events[instance.name] = None
