from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from player.models import Room, generate_token, events


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
        events[instance.name] = None
