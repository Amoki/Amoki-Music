from django import forms
from music.models import Room


class DuplicateForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Room.objects.all())
