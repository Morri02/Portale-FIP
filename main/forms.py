from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

from .models import *


class PlayerSearchForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, min_length=3, required=False)
    last_name = forms.CharField(label="Last Name", max_length=100, min_length=3, required=False)
    championship = forms.ChoiceField(choices=[], required=False)
    team = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['championship'].choices = self.get_championship_choices()
        self.fields['team'].choices = self.get_team_choices()

    def get_championship_choices(self):
        championships = ChampionShip.objects.all()
        choices = [('', 'All championships')]
        choices += [(championship.id, championship.name) for championship in championships]
        return choices

    def get_team_choices(self):
        teams = Team.objects.all()
        choices = [('', 'All teams')]
        choices += [(team.id, team.name) for team in teams]
        return choices


class CreateMatchForm(forms.ModelForm):

    def clean(self):
        #
        # if self.cleaned_data['giornata'].calendario.championship == self.cleaned_data['teamA'].championships:
        #     self.add_error("teamA", "Non può essere in quel calendario")
        # if self.cleaned_data['giornata'].calendario.championship == self.cleaned_data['teamB'].championships:
        #     self.add_error("teamB", "Non può essere in quel calendario")
        # if self.cleaned_data['teamA'].teamA.championships == self.cleaned_data['teamB'].teamB.championships:
        #     self.add_error("teamB", "Not in the same championship")
        #
        # if self.cleaned_data['teamA'] == self.cleaned_data['teamB']:
        #     self.add_error("teamB", "Non può giocare con sè stessa")

        return self.cleaned_data

    class Meta:
        model = Match
        fields = '__all__'


class CreateTabellinoForm(forms.ModelForm):

    def clean(self):
        pass

    class Meta:
        model = Tabellino
        fields = '__all__'


class CreateUserPlayer(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name='Players')
        g.user_set.add(user)
        return user