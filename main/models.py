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
    championships = models.ForeignKey(ChampionShip, on_delete=models.PROTECT, related_name='teams', null=True,
                                      blank=True)

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

    def __str__(self):
        return 'Tabellino '

    class Meta:
        verbose_name_plural = 'Tabellini'


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

    class Meta:
        verbose_name_plural = 'Giornate'


class Match(models.Model):
    date = models.DateTimeField(null=True)
    #    championship = models.ForeignKey(ChampionShip, on_delete=models.CASCADE, blank=False, null=False)
    teamA = models.ForeignKey(Team, related_name='teamA', on_delete=models.CASCADE, blank=False, null=False)
    teamB = models.ForeignKey(Team, related_name='teamB', on_delete=models.CASCADE, blank=False, null=False)
    tabellinoA = models.OneToOneField(Tabellino, on_delete=models.PROTECT, related_name='partitaA', blank=True,
                                      null=True)
    tabellinoB = models.OneToOneField(Tabellino, on_delete=models.PROTECT, related_name='partitaB', blank=True,
                                      null=True)
    pointsA = models.PositiveSmallIntegerField(blank=True, null=True)
    pointsB = models.PositiveSmallIntegerField(blank=True, null=True)
    location = models.CharField(max_length=50)
    giornata = models.ForeignKey(Giornata, related_name='partite', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.teamA.name + ' - ' + self.teamB.name
