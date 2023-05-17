from django.core.mail.backends import console
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .forms import *


# Create your views here.

def home_page(request):
    return render(request, 'home_page.html')


def test_base(request):
    return render(request, 'base.html')


def register_page(request):
    return render(request, 'register.html')


def get_teams(request):
    championship = request.GET.get('championship')
    if championship == '':
        teams = Team.objects.all()
    elif championship:
        teams = Team.objects.filter(championships_id__exact=championship)
    else:
        teams = Team.objects.none()

    for team in teams:
        print(str(team))

    team_data = [{'id': team.id, 'name': team.name} for team in teams] + [{'id': '', 'name': 'All Teams'}]

    # Return the team data as JSON response
    return JsonResponse({'teams': team_data})


def player_search(request):
    players = Player.objects.all()

    if request.method == 'POST':
        form = PlayerSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            last_name = form.cleaned_data.get('last_name')
            team = form.cleaned_data.get('team')
            championship = form.cleaned_data.get('championship')

            if championship != '':
                players = players.filter(team__in=ChampionShip.objects.get(pk=championship).teams.all())
            if team != '':
                players = players.filter(team__exact=team)
            if name:
                players = players.filter(name__icontains=name)
            if last_name:
                players = players.filter(last_name__icontains=last_name)
    else:
        form = PlayerSearchForm()

    context = {'form': form,
               'players': players,
               }
    return render(request, 'player_search.html', context)


class ListPlayerView(ListView):
    model = Player
    template_name = 'list_player.html'


class ListTeamView(ListView):
    model = Team
    template_name = 'list_teams.html'
    context_object_name = 'teams'


class ListChampionshipView(ListView):
    model = ChampionShip
    template_name = 'list_championships.html'
    context_object_name = 'championships'


class DetailPlayerView(DetailView):
    model = Player
    template_name = 'detail_player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        points, rebounds, blocks = count_points(ctx['player'].pk)
        ctx['points'] = points
        ctx['rebounds'] = rebounds
        ctx['blocks'] = blocks
        return ctx


class DetailTeamView(DetailView):
    model = Team
    template_name = 'detail_team.html'
    context_object_name = 'team'


class CreatePlayerView(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('main:homepage')
    template_name = 'create_player.html'


class DeletePlayerView(DeleteView):
    model = Player
    template_name = 'delete_player.html'
    success_url = reverse_lazy('main:list-players')


class UpdatePlayerView(UpdateView):
    model = Player
    fields = '__all__'
    template_name = 'update_player.html'

    def get_success_url(self):
        return reverse_lazy('main:player-detail', args=[self.object.pk])


class CreateMatchView(CreateView):
    template_name = 'create_match.html'
    form_class = CreateMatchForm
    success_url = reverse_lazy('main:homepage')


def count_points(pk):
    player = get_object_or_404(Player, pk=pk)
    points = 0
    rebounds = 0
    blocks = 0
    for stat in player.stats.all():
        if stat.valid :
            points += stat.points
            blocks += stat.blocks
            rebounds += stat.rebounds

    return points, rebounds, blocks


class CreateStatView(CreateView):
    model = Stat
    template_name = 'create_stat.html'
    fields = '__all__'
    success_url = reverse_lazy('main:homepage')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['players'] = Player.objects.all()
        return ctx


def create_stat(request):
    ctx = {'players': Player.objects.all()}
    if request.method == 'POST':
        pass

    return render(request, 'create_stat.html', ctx)