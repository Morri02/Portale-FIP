import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from django.contrib import messages


def about(request):
    return render(request, 'about.html')


def home_page(request):
    if request.GET.get('login') == 'ok':
        return render(request, 'home_page.html', context={'benvenuto': request.user.username})
    if request.GET.get('logout') == 'ok':
        return render(request, 'registration/prova.html')
    return render(request, 'home_page.html')


@user_passes_test(lambda u: u.is_staff)
def test_base(request):
    return render(request, 'base.html')


########################################################################################################################
# Retrieve functions
@require_GET
def get_teams(request):
    championship = request.GET.get('championship')
    if championship == '':
        teams = Team.objects.all()
    elif championship:
        teams = Team.objects.filter(championships_id__exact=championship)
    else:
        teams = Team.objects.none()

    team_data = [{'id': '', 'name': 'Tutte le Squadre'}] + [{'id': team.id, 'name': team.name} for team in teams]

    return JsonResponse({'teams': team_data})


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
                form.fields['team'].choices = [('', 'Tutte le Squadre')]
                teams = Team.objects.filter(championships_id__exact=championship)
                form.fields['team'].choices += [(team.id, team.name) for team in teams]
                players = players.filter(team__in=ChampionShip.objects.get(pk=championship).teams.all())
            if team != '':
                players = players.filter(team__exact=team)
            if name:
                players = players.filter(name__istartswith=name)
            if last_name:
                players = players.filter(last_name__istartswith=last_name)

    else:
        form = PlayerSearchForm()

    context = {'form': form,
               'players': players,
               }
    return render(request, 'player_search.html', context)


########################################################################################################################
# Player


class ListPlayerView(ListView):
    model = Player
    template_name = 'list_player.html'


class DetailPlayerView(DetailView):
    model = Player
    template_name = 'detail_player.html'
    context_object_name = 'giocatore'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        points, rebounds, assists = self.get_object().get_total_points()
        counter = self.get_object().get_total_matches()

        partite_in_casa, partite_in_casa_giocate = self.get_object().get_partite_in_casa()
        partite_in_trasferta, partite_in_trasferta_giocate = self.get_object().get_partite_in_trasferta()

        ctx['media_punti'] = round(points / counter, 2) if counter != 0 else 0
        ctx['media_rimbalzi'] = round(rebounds / counter, 2) if counter != 0 else 0
        ctx['media_assist'] = round(assists / counter, 2) if counter != 0 else 0
        ctx['points'] = points
        ctx['rebounds'] = rebounds
        ctx['blocks'] = assists
        ctx['partite_in_casa'] = partite_in_casa
        ctx['partite_in_casa_giocate'] = partite_in_casa_giocate
        ctx['partite_in_trasferta'] = partite_in_trasferta
        ctx['partite_in_trasferta_giocate'] = partite_in_trasferta_giocate
        ctx['partite'] = self.object.get_partite()
        return ctx


class DeletePlayerView(UserPassesTestMixin, DeleteView):
    model = Player
    template_name = 'delete_player.html'
    success_url = reverse_lazy('main:dashboard')
    context_object_name = 'player'

    def test_func(self):
        return self.request.user.is_staff


class UpdatePlayerView(UserPassesTestMixin, UpdateView):
    model = Player
    fields = '__all__'
    template_name = 'update_player.html'

    def get_success_url(self):
        return reverse_lazy('main:player-detail', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_staff


class CreatePlayerView(UserPassesTestMixin, CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('main:dashboard')
    template_name = 'create_player.html'

    def test_func(self):
        return self.request.user.is_staff


@user_passes_test(lambda u: u.is_staff)
def add_player(request, team_id):
    if request.method == 'POST':
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            player = Player(team_id=team_id)
            player.name = form.cleaned_data.get('name')
            player.last_name = form.cleaned_data.get('last_name')
            player.number = form.cleaned_data.get('number')
            player.role = form.cleaned_data.get('role')
            player.birth_date = form.cleaned_data.get('birth_date')
            player.profile_img = form.cleaned_data.get('profile_img')

            player.save()

            return redirect('main:dashboard')
        else:
            return render(request, 'add_player.html', context={'form': form})
    else:
        form = AddPlayerForm()

        return render(request, 'add_player.html', context={'form': form, 'squadra': Team.objects.get(pk=team_id)})


##################################################################################################################
# Coach


class DeleteCoachView(UserPassesTestMixin, DeleteView):
    model = Coach
    template_name = 'delete_coach.html'
    success_url = reverse_lazy('main:dashboard')
    context_object_name = 'coach'

    def test_func(self):
        return self.request.user.is_staff


class UpdateCoachView(UserPassesTestMixin, UpdateView):
    model = Coach
    fields = '__all__'
    template_name = 'update_coach.html'
    context_object_name = 'coach'

    def get_success_url(self):
        return reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff


class CreateCoachView(UserPassesTestMixin, CreateView):
    model = Coach
    fields = '__all__'
    success_url = reverse_lazy('main:dashboard')
    template_name = 'create_coach.html'

    def test_func(self):
        return self.request.user.is_staff


@user_passes_test(lambda u: u.is_staff)
def add_coach(request, team_id):
    if request.method == 'POST':
        form = AddCoachForm(request.POST)
        if form.is_valid():
            coach = Coach(team_id=team_id)
            coach.name = form.cleaned_data.get('name')
            coach.last_name = form.cleaned_data.get('last_name')
            coach.birth_date = form.cleaned_data.get('birth_date')
            coach.profile_img = form.cleaned_data.get('profile_img')

            coach.save()

            return redirect('main:dashboard')
        else:
            return render(request, 'add_coach.html', context={'form': form})
    else:
        form = AddCoachForm()

        return render(request, 'add_coach.html', context={'form': form, 'squadra': Team.objects.get(pk=team_id)})


########################################################################################################################
# Teams

class DeleteTeamView(UserPassesTestMixin, DeleteView):
    model = Team
    template_name = 'delete_team.html'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff

class UpdateTeamView(UserPassesTestMixin, UpdateView):
    model = Team
    fields = '__all__'
    template_name = 'update_team.html'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff

class CreateTeamView(UserPassesTestMixin, CreateView):
    model = Team
    fields = '__all__'
    template_name = 'create_team.html'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff


@user_passes_test(lambda u: u.is_staff)
def add_team(request, campionato_id):
    if request.method == 'POST':
        form = AddTeamForm(request.POST)
        if form.is_valid():
            team = Team(championships_id=campionato_id)
            team.name = form.cleaned_data.get('name')
            team.city = form.cleaned_data.get('city')
            team.main_sponsor = form.cleaned_data.get('main_sponsor')
            team.img = form.cleaned_data.get('img')

            team.save()

            return redirect('main:dashboard')
        else:
            return render(request, 'add_team.html',
                          context={'form': form, 'campionato': ChampionShip.objects.get(pk=campionato_id)})
    else:
        form = AddTeamForm()

        return render(request, 'add_team.html',
                      context={'form': form, 'campionato': ChampionShip.objects.get(pk=campionato_id)})


class ListTeamView(ListView):
    model = Team
    template_name = 'list_teams.html'
    context_object_name = 'teams'


class DetailTeamView(DetailView):
    model = Team
    template_name = 'detail_team.html'
    context_object_name = 'squadra'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        partite = []
        for giornata in self.object.championships.calendario.giornate.all():
            for partita in giornata.partite.all():
                if self.object == partita.teamA or self.object == partita.teamB:
                    partite.append(partita)
        partite.sort(key=lambda x: x.date)
        segnati, subiti = self.object.get_media_punti_partita()
        marcatore, rimbalzista, assistman = self.object.get_best_marcatore_rimbalzista_assistman()
        ctx['partite'] = partite
        ctx['media_punti_segnati'] = segnati
        ctx['media_punti_subiti'] = subiti
        ctx['miglior_marcatore'] = marcatore
        ctx['rimbalzista'] = rimbalzista
        ctx['assistman'] = assistman
        return ctx


########################################################################################################################
# Campionati

class UpdateChampView(UserPassesTestMixin, UpdateView):
    model = ChampionShip
    context_object_name = 'campionato'
    template_name = 'update_champ.html'
    success_url = reverse_lazy('main:dashboard')
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_staff


@user_passes_test(lambda u: u.is_staff)
def delete_champ_all(request, champ_id):
    champ = ChampionShip.objects.get(pk=champ_id)
    for team in champ.teams.all():
        team.delete()

    champ.delete()
    return redirect('main:dashboard')


class DeleteChampView(UserPassesTestMixin, DeleteView):
    model = ChampionShip
    template_name = 'delete_champ.html'
    context_object_name = 'champ'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff


class CreateChampView(UserPassesTestMixin, CreateView):
    model = ChampionShip
    template_name = 'create_champ.html'
    fields = '__all__'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        Calendario.objects.create(championship_id=self.object.id)

        return super().get_success_url()


class ListChampionshipView(ListView):
    model = ChampionShip
    template_name = 'list_championships.html'
    context_object_name = 'championships'


class DeleteGiornataView(UserPassesTestMixin, DeleteView):
    model = Giornata
    template_name = 'delete_giornata.html'
    context_object_name = 'giornata'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff


@user_passes_test(lambda u: u.is_staff)
def create_giornate(request, campionato_id):
    if request.method == 'POST':
        num_giornate = int(request.POST['num_giornate'])
        for _ in range(num_giornate):
            calendario = ChampionShip.objects.get(pk=campionato_id).calendario
            num = 0
            l = []
            for giornata in calendario.giornate.all():
                l.append(giornata.num)
            l.sort()
            for i in range(1, len(l) + 1):
                if i not in l:
                    num = i
                    break
            if num == 0:
                num = len(l) + 1
            giornata = Giornata(num=num, calendario_id=calendario.pk)
            giornata.save()

    return redirect('main:dashboard')


########################################################################################################################
# Statistiche e Calendario
class DeleteTabellinoView(UserPassesTestMixin, DeleteView):
    model = Tabellino
    template_name = 'delete_tabellino.html'
    context_object_name = 'tabellino'

    def get_success_url(self):
        t = self.get_object()
        try:
            if t.partitaA:
                partita = t.partitaA
        except Exception:
            pass
        try:
            if t.partitaB:
                partita = t.partitaB
        except Exception:
            pass
        return reverse('main:match-detail', args=[partita.pk])

    def form_valid(self, form):
        t = self.get_object()
        try:
            if t.partitaA:
                squadra = t.partitaA.teamA
                squadra.pointsA = 0
                squadra.save()
        except Exception:
            pass
        try:
            if t.partitaB:
                squadra = t.partitaB.teamB
                squadra.pointsB = 0
                squadra.save()
        except Exception:
            pass

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        t = self.get_object()
        try:
            if t.partitaA:
                ctx['partita'] = t.partitaA
        except Exception:
            pass
        try:
            if t.partitaB:
                ctx['partita'] = t.partitaB
        except Exception:
            pass
        return ctx


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
    error_str = "Non sei autorizzato a eseguire questa azione. Un tabellino è già stato inserito."
    if lettera == 'A':
        if partita.tabellinoA and not request.user.is_staff:
            return render(request, '403_forbidden.html', context={'errors': error_str})

    if lettera == 'B':
        if partita.tabellinoB and not request.user.is_staff:
            return HttpResponseForbidden(
                error_str)

    if partita.date >= timezone.now():
        return render(request, '403_forbidden.html',
                      context={'errors': 'La partita non è ancora stata giocata, come hai avuto questo link?!'})

    template_name = 'create_tabellino' + lettera + '.html'
    errors = []

    if request.method == 'POST':
        list_inputs = []
        list_stats = []
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

            if player == '' and (points != 0 or rebounds != 0 or blocks != 0):
                errors.append('Errore: Selezionare il giocatore ' + str(i))
                continue

            if points < 0 or rebounds < 0 or blocks < 0:
                errors.append(f'Errore: Il giocatore {i} aveva una statistica negativa')
                continue

            if player_id != '':
                duplicate = False
                for j in range(0, len(list_inputs) - 1):
                    if player_id == list_inputs[j][0]:
                        duplicate = True
                        break
                if not duplicate:
                    list_stats.append(Stat(player_id=player_id, points=points, rebounds=rebounds,
                                           blocks=blocks))
                else:
                    errors.append(f'Errore: Il giocatore {i} è stato inserito più di una volta')
                    list_stats.append(None)
                    continue
            else:
                list_stats.append(None)
                continue

            list_stats[i].save()

        if len(errors) == 0:
            # Inserimento stats nel tabellino
            tabellino = Tabellino(created_by=request.user)
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
            partita.save()
            return redirect('main:match-detail', pk=match_id)

    context = {'players': Player.objects.filter(team_id=partita.teamA.id) if lettera == 'A' else Player.objects.filter(
        team_id=partita.teamB.id),
               'match_id': match_id,
               'partita': partita,
               'range': [i for i in range(1, 13)],
               'errors': errors}

    return render(request, template_name=template_name, context=context)


def get_pk_player(player):
    l = player.split()
    players = Player.objects.filter(name=l[0], last_name=l[1], number=int(l[2].replace('#', '')))
    player_id = 0
    if players.count() > 1:
        -('Errore')
    for player in players:
        player_id = player.pk
    return player_id


@user_passes_test(lambda u: u.is_staff)
def create_nuovo_tabellinoA(request, match_id):
    return create_nuovo_tabellino(request, match_id, 'A')


@user_passes_test(lambda u: u.is_staff)
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


########################################################################################################################
# Matches

@user_passes_test(lambda u: u.is_staff)
def create_match(request, giornata_id):
    if request.method == 'POST':
        form = CreateMatchForm(request.POST)
        match = Match(giornata_id=giornata_id)
        if form.is_valid():
            teamA = form.cleaned_data.get('teamA')
            teamB = form.cleaned_data.get('teamB')
            date = form.cleaned_data.get('date')
            location = form.cleaned_data.get('location')
            match.teamA = teamA
            match.teamB = teamB
            match.date = date
            match.location = location
            match.save()
        else:
            form.fields['teamA'].queryset = Team.objects.filter(championships__calendario__giornate__exact=giornata_id)
            form.fields['teamB'].queryset = Team.objects.filter(championships__calendario__giornate__exact=giornata_id)
            return render(request, 'create_match.html',
                          context={'form': form, 'giornata': Giornata.objects.get(pk=giornata_id)})
        return redirect('main:dashboard')
    else:
        form = CreateMatchForm()
        form.fields['teamA'].queryset = Team.objects.filter(championships__calendario__giornate__exact=giornata_id)
        form.fields['teamB'].queryset = Team.objects.filter(championships__calendario__giornate__exact=giornata_id)

    return render(request, 'create_match.html',
                  context={'form': form, 'giornata': Giornata.objects.get(pk=giornata_id)})


# class CreateMatchView(UserPassesTestMixin, CreateView):
#     template_name = 'create_match.html'
#     form_class = CreateMatchForm
#     success_url = reverse_lazy('main:homepage')
#
#     def test_func(self):
#         return self.request.user.is_staff


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
        ctx['giocata'] = timezone.now() > self.object.date
        return ctx


class ListMatchView(ListView):
    model = Match
    template_name = 'list_matches.html'
    context_object_name = 'partite'


class UpdateMatchView(UserPassesTestMixin, UpdateView):
    model = Match
    template_name = 'update_match.html'
    context_object_name = 'match'
    success_url = reverse_lazy('main:dashboard')
    fields = ['date', 'location', 'giornata']

    def test_func(self):
        return self.request.user.is_staff


class DeleteMatchView(UserPassesTestMixin, DeleteView):
    model = Match
    template_name = 'delete_match.html'
    context_object_name = 'match'
    success_url = reverse_lazy('main:dashboard')

    def test_func(self):
        return self.request.user.is_staff


########################################################################################################################
# Admin

@user_passes_test(lambda u: u.is_staff)
def dashboard_view(request):
    context = {'squadre': Team.objects.all().order_by('name'),
               'giocatori': Player.objects.all().order_by('last_name'),
               'allenatori': Coach.objects.all().order_by('last_name'),
               'partite': Match.objects.all().order_by('date'),
               'campionati': ChampionShip.objects.all().order_by('name')}
    return render(request, 'dashboard.html', context)


########################################################################################################################
# Commenti
@user_passes_test(lambda u: u.is_staff)
def delete_comment(request, comment_id):
    commento = get_object_or_404(Commento, id=comment_id)

    if request.method == 'POST':
        commento.delete()
        return redirect('main:match-detail', pk=commento.match_id)
    return redirect('main:homepage')


@login_required
def add_comment(request, match_id):
    if request.method == 'POST':
        if request.POST.get('content'):
            comment = Commento(created_by=request.user)
            comment.match_id = match_id
            comment.comment = request.POST.get('content')
            comment.date = timezone.now()
            comment.save()
        else:
            messages.error(request, 'Il commento non può essere vuoto')
        return redirect('main:match-detail', pk=match_id)
    else:
        messages.error(request, 'Richiesta non valida')
        return redirect('main:match-detail', pk=match_id)


@require_POST
@csrf_exempt
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Commento.objects.get(id=comment_id)
    if request.user.is_authenticated:
        # Controllo se l'utente ha già messo like o dislike al commento
        user_liked = Like.objects.filter(comment=comment, created_by=request.user).exists()
        user_disliked = DisLike.objects.filter(comment=comment, created_by=request.user).exists()
        if user_liked:
            comment.likes.filter(created_by=request.user).delete()
        else:
            Like.objects.create(comment=comment, created_by=request.user)
            if user_disliked:
                comment.dislikes.filter(created_by=request.user).delete()

    likes_count = comment.likes.count()
    dislikes_count = comment.dislikes.count()
    response_data = {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'authenticated': request.user.is_authenticated
    }
    return JsonResponse(response_data)


@require_POST
@csrf_exempt
def dislike_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Commento.objects.get(pk=comment_id)
    if request.user.is_authenticated:
        user_disliked = DisLike.objects.filter(comment=comment, created_by=request.user).exists()
        user_liked = Like.objects.filter(comment=comment, created_by=request.user).exists()
        if user_disliked:
            comment.dislikes.filter(created_by=request.user).delete()
        else:
            DisLike.objects.create(comment=comment, created_by=request.user)
            if user_liked:
                comment.likes.filter(created_by=request.user).delete()

    likes_count = comment.likes.count()
    dislikes_count = comment.dislikes.count()
    response_data = {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'authenticated': request.user.is_authenticated
    }
    return JsonResponse(response_data)
