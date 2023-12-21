from django import forms

from games.models import Game


class UploadFileForm(forms.Form):
    file = forms.FileField()


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['team_1', 'team_1_score', 'team_2', 'team_2_score']
