from django import forms

class GameForm(forms.Form):
    DIFFICULTY = (
      ('beginner','beginner'),
      ('intermediate','intermediate'),
      ('expert','expert'),
      )
    name = forms.CharField(label='Name', max_length=100)
    difficulty = forms.ChoiceField(choices=DIFFICULTY, required=True)