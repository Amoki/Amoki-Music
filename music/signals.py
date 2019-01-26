from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from music.models import Room, generate_token, Events, MusicQueue
from music.serializers import RoomSerializer


@receiver(pre_save, sender=Room)
def update_token_on_password_change(sender, instance, **kwargs):
    # first save() of a room don't have pk (not in BD).
    # This if is used to skip the signal of this first call.
    # (Room.objects.get need to have a valid pk argument)
    if instance.pk:
        if instance.password != Room.objects.get(pk=instance.pk).password:
            instance.token = generate_token()


@receiver(post_save, sender=Room)
def create_room_event(sender, instance, created, **kwargs):
    if created:
        Events.set(instance, None)


@receiver(post_save, sender=MusicQueue)
def update_room_state(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"room_{instance.room_id}",
        {"type": "room_message", "message": RoomSerializer(instance.room).data},
    )
    print("STATE_UPDATED")

