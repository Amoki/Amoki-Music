from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from music.models import Room, Events, MusicQueue
from music.serializers import RoomSerializer


@receiver(post_save, sender=Room)
def create_room_event(sender, instance, created, **kwargs):
    if created:
        Events.set(instance, None)


@receiver(post_save, sender=Room)
def on_room_change(sender, instance, created, **kwargs):
    instance.send_state()

@receiver(m2m_changed, sender=MusicQueue)
def queue_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        instance.send_state()
    elif action == "post_remove":
        music_remove = model
        if instance.current_music:
            instance.add_music(instance.current_music)
        elif instance.shuffle:
            next_music = instance.select_random_music()
            instance.add_music(next_music)
        else:
            instance.send_state()
