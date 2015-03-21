# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from player.models import Room, events, generate_token
from music.models import Music


@receiver(pre_save, sender=Room)
def add_event(sender, instance, **kwargs):
    events[instance.name] = None


@receiver(pre_save, sender=Room)
def update_token_on_password_change(sender, instance, **kwargs):
    # first save() of a room don't have pk (not in BD).
    # This if is used to skip the signal of this first call.
    # (Room.objects.get need to have a valid pk argument)
    if instance.pk:
        if instance.password != Room.objects.get(pk=instance.pk).password:
            instance.token = generate_token()

@receiver(pre_save, sender=Music)
def update_duration(sender, instance, **kwargs):
    if instance.timer_end:
        new_duration = instance.duration - (instance.duration - instance.timer_end)
    new_duration = instance.duration - instance.timer_start

    if new_duration != instance.duration:
        instance.duration = new_duration
