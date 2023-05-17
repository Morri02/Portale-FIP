from django.db import models


# Create your models here.

class ChampionShip(models.Model):
    name = models.CharField(max_length=20)
#    teams = models.ManyToManyField(Team, related_name='championships')
    year = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.name + '(' + str(self.year) + ')'


class Team(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    main_sponsor: str = models.CharField(default=None, null=True, max_length=50)
    img = models.ImageField(upload_to='team_images/', blank=True, null=True)
    championships = models.ForeignKey(ChampionShip, on_delete=models.PROTECT, related_name='teams', null=True, blank=True)

    def __str__(self):
        return self.name + ' of ' + self.city + ', ' + self.main_sponsor


class Player(models.Model):
    name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    birth_date = models.DateTimeField()
    number: int = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='players')
    profile_img = models.ImageField(upload_to='player_images/', blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + self.last_name + ' #' + str(self.number)




class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='stats')
    points = models.PositiveSmallIntegerField(blank=False, null=False, default=0)
    rebounds = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    blocks = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    valid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.player) + ', ' + str(self.points)


class Tabellino(models.Model):
    statA1 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA1')
    statA2 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA2', blank=True, null=True)
    statA3 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA3', blank=True, null=True)
    statA4 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA4', blank=True, null=True)
    statA5 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA5', blank=True, null=True)
    statA6 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA6', blank=True, null=True)
    statA7 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA7', blank=True, null=True)
    statA8 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA8', blank=True, null=True)
    statA9 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA9', blank=True, null=True)
    statA10 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA10', blank=True, null=True)
    statA11 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA11', blank=True, null=True)
    statA12 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statA12', blank=True, null=True)

    statB1 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB1')
    statB2 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB2', blank=True, null=True)
    statB3 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB3', blank=True, null=True)
    statB4 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB4', blank=True, null=True)
    statB5 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB5', blank=True, null=True)
    statB6 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB6', blank=True, null=True)
    statB7 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB7', blank=True, null=True)
    statB8 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB8', blank=True, null=True)
    statB9 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB9', blank=True, null=True)
    statB10 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB10', blank=True, null=True)
    statB11 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB11', blank=True, null=True)
    statB12 = models.OneToOneField(Stat, on_delete=models.CASCADE, related_name='statB12', blank=True, null=True)

    def __str__(self):
        return 'Tabellino '


class Calendario(models.Model):

    championship = models.OneToOneField(ChampionShip, related_name='calendario', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.championship)

    class Meta:
        verbose_name_plural = 'Calendari'


class Giornata(models.Model):
    num = models.IntegerField()
    calendario = models.ForeignKey(Calendario, related_name='giornate', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.calendario) + ', ' + str(self.num) + ' giornata'


class Match(models.Model):
    date = models.DateTimeField(null=True)
#    championship = models.ForeignKey(ChampionShip, on_delete=models.CASCADE, blank=False, null=False)
    teamA = models.ForeignKey(Team, related_name='teamA', on_delete=models.CASCADE, blank=False, null=False)
    teamB = models.ForeignKey(Team, related_name='teamB', on_delete=models.CASCADE, blank=False, null=False)
    pointsA = models.PositiveSmallIntegerField(blank=True, null=True)
    pointsB = models.PositiveSmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=50)
    tabellino = models.OneToOneField(Tabellino, on_delete=models.PROTECT, related_name='partita', blank=True, null=True)
    giornata = models.ForeignKey(Giornata, related_name='partite', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.teamA.name + ' - ' + self.teamB.name