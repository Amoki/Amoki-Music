# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from player.models import Room, events, generate_token


@receiver(pre_save, sender=Room)
def add_event(sender, instance, **kwargs):
    events[instance.name] = None


@receiver(pre_save, sender=Room)
def update_token_on_password_change(sender, instance, **kwargs):
    if instance.pk:
        if instance.password != Room.objects.get(pk=instance.pk).password:
            instance.token = generate_token()
