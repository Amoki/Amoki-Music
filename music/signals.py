from django.db.models.signals import pre_save
from django.dispatch import receiver
from music.models import Music


@receiver(pre_save, sender=Music)
def update_duration(sender, instance, **kwargs):
    instance.duration = instance.total_duration
    if instance.timer_end:
        instance.duration = instance.total_duration - (instance.total_duration - instance.timer_end)
    instance.duration -= instance.timer_start
