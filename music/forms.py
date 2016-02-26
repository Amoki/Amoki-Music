from player.models import Room
from django import forms


class DuplicateForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all())
