from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.forms import widgets
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
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    def clean(self):
        if self.cleaned_data['teamA'] == self.cleaned_data['teamB']:
            self.add_error("teamB", "Non può giocare con sè stessa")

        return self.cleaned_data

    class Meta:
        model = Match
        fields = ['date', 'teamA', 'teamB', 'location']


class AddPlayerForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Player
        fields = ['name', 'last_name', 'number', 'role', 'birth_date', 'profile_img']


class AddTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'city', 'img', 'main_sponsor']


class CreateTabellinoForm(forms.ModelForm):

    def clean(self):
        pass

    class Meta:
        model = Tabellino
        fields = '__all__'

