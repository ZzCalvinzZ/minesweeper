from django import forms
from django.core.validators import RegexValidator

class GameForm(forms.Form):
    DIFFICULTY = (
      ('beginner','beginner'),
      ('intermediate','intermediate'),
      ('expert','expert'),
      )

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    name = forms.CharField(label='Name', max_length=100, validators=[alphanumeric])
    difficulty = forms.ChoiceField(choices=DIFFICULTY, required=True)
