from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

#TODO: Fare una dashboard amministratore


def home_page(request):
    if request.GET.get('login') == 'ok':
        return render(request, 'home_page.html', context={'benvenuto': request.user.username})
    return render(request, 'home_page.html')


def test_base(request):
    return render(request, 'base.html')


# JavaScript retrieve functions

@user_passes_test(lambda u: u.is_staff)
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


@user_passes_test(lambda u: u.is_staff)
def get_all_matches(request):
    partite = Match.objects.all()

    print('all')
    for partita in partite:
        data = [{'id': partita.id, 'partita': partita.teamA.name + '-' + partita.teamB.name}]

    return JsonResponse({'data': data})


@user_passes_test(lambda u: u.is_staff)
def get_matches_by_giornata(request, giornata_id):
    partite = Match.objects.filter(giornata_id=giornata_id)

    print('day')

    return JsonResponse({'partite': partite})


# Actual views

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
                form.fields['team'].choices = [('', 'All teams')]
                teams = Team.objects.filter(championships_id__exact=championship)
                form.fields['team'].choices += [(team.id, team.name) for team in teams]
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
    context_object_name = 'giocatore'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        points, rebounds, blocks = self.get_object().get_total_points()
        counter = self.get_object().get_total_matches()
        ctx['media_punti'] = points / counter if counter != 0 else 0
        ctx['points'] = points
        ctx['rebounds'] = rebounds
        ctx['blocks'] = blocks
        return ctx


class DetailTeamView(DetailView):
    model = Team
    template_name = 'detail_team.html'
    context_object_name = 'squadra'


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
    #TODO: Da rendere disponibile all'admin


def aggiorna_classifica(calendario_id):
    classifica = []
    calendario = Calendario.objects.get(pk=calendario_id)
    teams = Team.objects.filter(championships_id=calendario.championship.id)
    squadra_punti_w_l = []  # w:win l:loss
    for team in teams:
        punti, vittorie, sconfitte = team.get_punti(calendario_id)
        squadra_punti_w_l.append([team.id, punti, vittorie, sconfitte])

    squadra_punti_w_l.sort(key=lambda x: x[1], reverse=True)
    print(str(squadra_punti_w_l))
    for obj in squadra_punti_w_l:
        classifica.append(obj[0])
    print('Classifica aggiornata:' + str(classifica))
    return squadra_punti_w_l


class DetailCalendarioView(DetailView):
    model = Calendario
    template_name = 'detail_calendario.html'
    context_object_name = 'calendario'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        squadra_punti_w_l = self.get_object().get_classifica()
        classifica = []
        pos = 1
        for obj in squadra_punti_w_l:
            classifica.append([pos, Team.objects.get(pk=obj[0]), obj[1], obj[2], obj[3]])
            pos += 1
        ctx['classifica'] = classifica
        qs = Giornata.objects.filter(calendario_id=self.get_object().pk)
        for obj in qs:
            giornata = obj
        ctx['giornata'] = giornata
        return ctx


@login_required
def create_tabellinoA(request, match_id):
    return create_tabellino(request, match_id, 'A')


@login_required
def create_tabellinoB(request, match_id):
    return create_tabellino(request, match_id, 'B')


def inserisci_statistiche(tabellino, list_stats):
    try:
        if list_stats[0]:
            tabellino.stat1 = list_stats[0]
            list_stats[0].valid = True
            list_stats[0].save()
        if list_stats[1]:
            tabellino.stat2 = list_stats[1]
            list_stats[1].valid = True
            list_stats[1].save()
        if list_stats[2]:
            tabellino.stat3 = list_stats[2]
            list_stats[2].valid = True
            list_stats[2].save()
        if list_stats[3]:
            tabellino.stat4 = list_stats[3]
            list_stats[3].valid = True
            list_stats[3].save()
        if list_stats[4]:
            tabellino.stat5 = list_stats[4]
            list_stats[4].valid = True
            list_stats[4].save()
        if list_stats[5]:
            tabellino.stat6 = list_stats[5]
            list_stats[5].valid = True
            list_stats[5].save()
        if list_stats[6]:
            tabellino.stat7 = list_stats[6]
            list_stats[6].valid = True
            list_stats[6].save()
        if list_stats[7]:
            tabellino.stat8 = list_stats[7]
            list_stats[7].valid = True
            list_stats[7].save()
        if list_stats[8]:
            tabellino.stat9 = list_stats[8]
            list_stats[8].valid = True
            list_stats[8].save()
        if list_stats[9]:
            tabellino.stat10 = list_stats[9]
            list_stats[9].valid = True
            list_stats[9].save()
        if list_stats[10]:
            tabellino.stat11 = list_stats[10]
            list_stats[10].valid = True
            list_stats[10].save()
        if list_stats[11]:
            tabellino.stat12 = list_stats[11]
            list_stats[11].valid = True
            list_stats[11].save()

    except Exception:
        return


@login_required
def create_tabellino(request, match_id, lettera):
    partita = Match.objects.get(pk=match_id)
    template_name = 'create_tabellino' + lettera + '.html'

    if request.method == 'POST':
        list_inputs = []
        list_stats = []
        last_index = 0
        for i in range(0, 12):
            player = request.POST.get('player' + str(i + 1))
            points = request.POST.get('points' + str(i + 1))
            rebounds = request.POST.get('rebounds' + str(i + 1))
            blocks = request.POST.get('blocks' + str(i + 1))
            list_inputs.append([player, points, rebounds, blocks])


            player_id = list_inputs[i][0]
            points = int(points) if points else 0
            rebounds = int(rebounds) if rebounds else 0
            blocks = int(blocks) if blocks else 0
            if player_id != '':
                list_stats.append(Stat(player_id=player_id, points=points, rebounds=rebounds,
                                   blocks=blocks))
            else:
                list_stats.append(None)
                continue

            list_stats[i].save()

        # Inserimento stats nel tabellino
        tabellino = Tabellino()
        tabellino.save()
        inserisci_statistiche(tabellino, list_stats)
        tabellino.save()

        #       Salvataggio nel team DB
        total_points = 0
        for stat in list_stats:
            if stat:
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
        # return render(request, 'match_detail.html', context={'match_id': match_id, 'partita': partita})
        return redirect("/main/detail/match/" + str(match_id))

    context = {'players': Player.objects.filter(team_id=partita.teamA.id) if lettera == 'A' else Player.objects.filter(
                   team_id=partita.teamB.id),
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




def create_nuovo_tabellinoA(request, match_id):
    return create_nuovo_tabellino(request, match_id, 'A')


def create_nuovo_tabellinoB(request, match_id):
    return create_nuovo_tabellino(request, match_id, 'B')



def create_nuovo_tabellino(request, match_id, lettera):
    partita = Match.objects.get(pk=match_id)
    if lettera == 'A':
        for stat in partita.tabellinoA.get_stats():
            stat.delete()
        partita.tabellinoA.delete()
    else:
        for stat in partita.tabellinoB.get_stats():
            stat.delete()
        partita.tabellinoB.delete()

    return create_tabellino(request, match_id, lettera)

class DetailMatchView(DetailView):
    model = Match
    template_name = 'match_detail.html'
    context_object_name = 'partita'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.get_object().tabellinoA:
            ctx['statsA'] = self.get_object().tabellinoA.get_stats()
        if self.get_object().tabellinoB:
            ctx['statsB'] = self.get_object().tabellinoB.get_stats()
        return ctx


class ListMatchView(ListView):
    model = Match
    template_name = 'list_matches.html'
    context_object_name = 'partite'


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("main:homepage")
