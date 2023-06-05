from django.contrib.auth.models import AbstractUser, User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


# Create your models here.

class ChampionShip(models.Model):
    name = models.CharField(max_length=20)
    #    teams = models.ManyToManyField(Team, related_name='championships')
    year = models.PositiveSmallIntegerField(default=timezone.now().year)
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.name# + '(' + str(self.year) + ')'

    class Meta:
        ordering = ['name', 'year']


class Team(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    main_sponsor: str = models.CharField(default=None, null=True, max_length=50)
    img = models.ImageField(upload_to='team_images/', blank=True, null=True)
    championships = models.ForeignKey(ChampionShip, on_delete=models.PROTECT, related_name='teams', null=True,
                                      blank=True)

    def __str__(self):
        return self.name + ' di ' + self.city + ', ' + self.main_sponsor

    def get_punti(self, calendario_id):
        calendario = Calendario.objects.get(pk=calendario_id)
        punti = 0
        vittorie = 0
        sconfitte = 0

        for giornata in Giornata.objects.filter(calendario_id=calendario_id):
            for partita in Match.objects.filter(giornata_id=giornata.pk):
                if self.pk == partita.teamA.id:
                    if partita.pointsA > partita.pointsB and partita.tabellinoB:
                        punti += 2
                        vittorie += 1
                    elif partita.pointsA < partita.pointsB:
                        sconfitte += 1

                if self.pk == partita.teamB.id:
                    if partita.pointsA < partita.pointsB and partita.tabellinoA:
                        punti += 2
                        vittorie += 1
                    elif partita.pointsA > partita.pointsB:
                        sconfitte += 1


        return punti, vittorie, sconfitte

    def get_media_punti_partita(self):
        punti_segnati = 0
        punti_subiti = 0
        num_partite_giocate = 0

        for partita in Match.objects.filter(teamA_id=self.pk):
                punti_segnati += partita.pointsA
                punti_subiti += partita.pointsB
                num_partite_giocate += 1

        for partita in Match.objects.filter(teamB_id=self.pk):
                punti_segnati += partita.pointsB
                punti_subiti += partita.pointsA
                num_partite_giocate += 1
        num_partite_giocate = 1 if num_partite_giocate == 0 else num_partite_giocate

        return round(punti_segnati / num_partite_giocate, 3), round(punti_subiti / num_partite_giocate, 2)

    def get_best_marcatore_rimbalzista_assistman(self):
        best ={'punti': [None, 0], 'rimbalzi': [None, 0], 'assists': [None, 0]}
        for player in self.players.all():
            punti, rimbalzi, assists = player.get_total_points()
            if punti > best['punti'][1]:
                best['punti'][1] = punti
                best['punti'][0] = player
            if rimbalzi > best['rimbalzi'][1]:
                best['rimbalzi'][1] = rimbalzi
                best['rimbalzi'][0] = player
            if assists > best['assists'][1]:
                best['assists'][1] = assists
                best['assists'][0] = player
        return best['punti'][0], best['rimbalzi'][0], best['assists'][0]

    class Meta:
        ordering = ['name']


class Coach(models.Model):
    name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    birth_date = models.DateField(default='01/01/2001')
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='coaches')
    profile_img = models.ImageField(upload_to='staff_images/', blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + self.last_name + ', ' + self.team.name


class Player(models.Model):
    name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    role = models.CharField(max_length=15, default='Guardia')
    birth_date = models.DateField(default='01/01/2001')
    number: int = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='players')
    profile_img = models.ImageField(upload_to='player_images/', blank=True, null=True)

    def __str__(self):
        return self.last_name + ' ' + self.name + ' #' + str(self.number)

    def get_partite(self):
        partite = []
        for match in Match.objects.filter(teamA=self.team) | Match.objects.filter(teamB=self.team):
            partite.append(match)
        return partite
    def get_partite_in_casa(self):
        partite = []
        partite_giocate = []
        for match in self.team.teamA.all():
            partite.append(match)
            if match.tabellinoA:
                for stat in match.tabellinoA.get_stats():
                    if stat:
                        if self.pk == stat.player_id:
                            partite_giocate.append(match)
        return partite, partite_giocate

    def get_partite_in_trasferta(self):
        partite = []
        partite_giocate = []
        for match in self.team.teamB.all():
            partite.append(match)
            if match.tabellinoB:
                for stat in match.tabellinoB.get_stats():
                    if stat:
                        if self.pk == stat.player_id:
                            partite_giocate.append(match)
        return partite, partite_giocate

    def get_total_points(self):
        points = 0
        rebounds = 0
        blocks = 0
        for stat in self.stats.all():
            if stat.valid:
                points += stat.points
                blocks += stat.blocks
                rebounds += stat.rebounds

        return points, rebounds, blocks

    def get_total_matches(self):
        counter = 0
        for stat in self.stats.all():
            counter += 1
        return counter

    class Meta:
        ordering = ['last_name', 'name']


class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    points = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    rebounds = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    blocks = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    valid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.player) + ', ' + str(self.points) + ', ' + str(self.rebounds) + ', ' + str(self.blocks)


class Tabellino(models.Model):
    stat1 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat1', blank=True, null=True)
    stat2 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat2', blank=True, null=True)
    stat3 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat3', blank=True, null=True)
    stat4 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat4', blank=True, null=True)
    stat5 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat5', blank=True, null=True)
    stat6 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat6', blank=True, null=True)
    stat7 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat7', blank=True, null=True)
    stat8 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat8', blank=True, null=True)
    stat9 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat9', blank=True, null=True)
    stat10 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat10', blank=True, null=True)
    stat11 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat11', blank=True, null=True)
    stat12 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='stat12', blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'Tabellino #' + str(self.pk)

    def get_stats(self):
        return [self.stat1, self.stat2, self.stat3, self.stat4, self.stat5, self.stat6, self.stat7, self.stat8,
                self.stat9, self.stat9, self.stat10, self.stat11, self.stat12]

    class Meta:
        verbose_name_plural = 'Tabellini'


class Calendario(models.Model):
    championship = models.OneToOneField(ChampionShip, related_name='calendario', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.championship)

    def get_classifica(self):
        classifica = []
        squadra_punti_w_l = []  # w:win l:loss
        for team in self.championship.teams.all():
            punti, vittorie, sconfitte = team.get_punti(self.pk)
            squadra_punti_w_l.append([team.id, punti, vittorie, sconfitte])

        squadra_punti_w_l.sort(key=lambda x: x[1], reverse=True)
        for obj in squadra_punti_w_l:
            classifica.append(obj[0])
        return squadra_punti_w_l

    class Meta:
        verbose_name_plural = 'Calendari'


class Giornata(models.Model):
    num = models.IntegerField()
    calendario = models.ForeignKey(Calendario, related_name='giornate', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.calendario) + ', ' + str(self.num) + ' giornata'

    class Meta:
        verbose_name_plural = 'Giornate'
        ordering = ['num']


class Match(models.Model):
    date = models.DateTimeField(null=True)
    #    championship = models.ForeignKey(ChampionShip, on_delete=models.CASCADE, blank=False, null=False)
    teamA = models.ForeignKey(Team, related_name='teamA', on_delete=models.CASCADE, blank=False, null=False)
    teamB = models.ForeignKey(Team, related_name='teamB', on_delete=models.CASCADE, blank=False, null=False)
    tabellinoA = models.OneToOneField(Tabellino, on_delete=models.SET_NULL, related_name='partitaA', blank=True,
                                      null=True)
    tabellinoB = models.OneToOneField(Tabellino, on_delete=models.SET_NULL, related_name='partitaB', blank=True,
                                      null=True)
    pointsA = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    pointsB = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    location = models.CharField(max_length=50)
    giornata = models.ForeignKey(Giornata, related_name='partite', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '(' + str(self.date.day) + '/' + str(self.date.month) + '/' + str(self.date.year) + ')   ' + str(
            self.pointsA) + ' :' + self.teamA.name + ' - ' + self.teamB.name + ': ' + str(self.pointsB)

    class Meta:
        ordering = ['date']


class Commento(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='commenti')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.CharField(max_length=500)
    date = models.DateField(null=True)

    def __str__(self):
        return self.comment



class Like(models.Model):
    comment = models.ForeignKey(Commento, on_delete=models.CASCADE, related_name="likes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class DisLike(models.Model):
    comment = models.ForeignKey(Commento, on_delete=models.CASCADE, related_name="dislikes")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

