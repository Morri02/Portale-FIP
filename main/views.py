from django.core.mail.backends import console
from django.db.models import Q
from django.shortcuts import render, redirect
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
        if stat.valid:
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


def create_tabellinoA(request, match_id):
    return create_tabellino(request, match_id, 'A')

def create_tabellinoB(request, match_id):
    return create_tabellino(request, match_id, 'B')

def create_tabellino(request, match_id, lettera):
    #TODO Fai una view per fare update del tabellino
    partita = Match.objects.get(pk=match_id)
    template_name = 'create_tabellino' + lettera +'.html'
    print(template_name)

    if request.method == 'POST':
        list_inputs = []
        list_stats = []
        for i in range(0, 12):
            list_inputs.append([request.POST.get('player' + str(i + 1)), request.POST.get('points' + str(i + 1)),
                                request.POST.get('rebounds' + str(i + 1)), request.POST.get('blocks' + str(i + 1))])
            if not list_inputs[i][0]:
                break
            player_id = get_pk_player(list_inputs[i][0])
            list_stats.append(Stat(player_id=player_id, points=int(list_inputs[i][1]), rebounds=int(list_inputs[i][2]),
                                   blocks=int(list_inputs[i][3])))
            list_stats[i].save()

#       Inserimento stats nel tabellino
        tabellino = Tabellino()
        tabellino.stat1 = list_stats[0]
        list_stats[0].valid = True
        list_stats[0].save()
        tabellino.save()

#       Salvataggio nel team DB
        total_points = 0
        for stat in list_stats:
            total_points += stat.points
        if lettera == 'A':
            partita.tabellinoA = tabellino
            partita.pointsA = total_points
        elif lettera == 'B':
            partita.tabellinoB = tabellino
            partita.pointsB = total_points
        print(total_points)
        partita.save()

        print(str(list_stats))
        return render(request, 'match_detail.html', context={'match_id': match_id, 'partita': partita})
        #return redirect("/main/detail/match/" + str(match_id))
    else:
        form = CreateTabellinoForm()


    context = {'form': form,
               'players': Player.objects.filter(team_id=partita.teamA.id) if lettera == 'A' else Player.objects.filter(team_id=partita.teamB.id),
               'match_id': match_id,
               'partita': partita,
               'range': [i for i in range(1, 13)]}

    return render(request, template_name=template_name, context=context)


def get_pk_player(player):
    l = player.split()
    players = Player.objects.filter(name=l[0], last_name=l[1], number=int(l[2].replace('#', '')))
    player_id = 0
    if players.count() > 1:
        print('Errore')
    for player in players:
        player_id = player.pk
    return player_id


class DetailMatchView(DetailView):
    model = Match
    template_name = 'match_detail.html'
    context_object_name = 'partita'


class ListMatchView(ListView):
    model = Match
    template_name = 'list_matches.html'
    context_object_name = 'partite'
