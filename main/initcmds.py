from .models import *
from django.core.files import File
from django.contrib.auth.models import Group


def create_groups():
    players = Group(name='Players')
    # players.permissions.add()
    players.save()


def check_matches():
    for match in Match.objects.all():
        pointsA = 0
        pointsB = 0
        if match.tabellinoA:
            for stat in match.tabellinoA.get_stats():
                if stat:
                    pointsA += stat.points
            match.pointsA = pointsA
        if match.tabellinoB:
            for stat in match.tabellinoB.get_stats():
                if stat:
                    pointsB += stat.points
            match.pointsB = pointsB
        match.save()


# Una sorta di garbage collector di stat e tabellini non agganciati più a niente
def check_stats():
    for stat in Stat.objects.all():
        if not stat.valid:
            stat.delete()

    for tabellino in Tabellino.objects.all():
        delete = True
        for match in Match.objects.all():
            if tabellino == match.tabellinoA or tabellino == match.tabellinoB:
                delete = False
                break
        if delete:
            tabellino.delete()

    for stat in Stat.objects.all():
        delete = True
        for tabellino in Tabellino.objects.all():
            if stat in tabellino.get_stats():
                delete = False
                break
        if delete:
            stat.delete()

    for match in Match.objects.all():
        if match.tabellinoA is None:
            match.pointsA = 0
            match.save()
        if not match.tabellinoB:
            match.pointsB = 0
            match.save()

    check_matches()
def erase_db():
    print('DATABASE ERASE')
    Match.objects.all().delete()
    Tabellino.objects.all().delete()
    Stat.objects.all().delete()
    Giornata.objects.all().delete()
    Calendario.objects.all().delete()
    Player.objects.all().delete()
    Team.objects.all().delete()
    ChampionShip.objects.all().delete()


def init_db():
    if ChampionShip.objects.all().count() > 0:
        return

    A1 = ChampionShip(name='Serie A1', location='Italia', year=2023)
    A1.save()
    cA1 = Calendario(championship=A1)
    cA1.save()
    A2 = ChampionShip(name='Serie A2', location='Italia', year=2023)
    A2.save()
    cA2 = Calendario(championship=A2)
    cA2.save()
    B1 = ChampionShip(name='Serie B1', location='Italia', year=2023)
    B1.save()
    cB1 = Calendario(championship=B1)
    cB1.save()
    B2 = ChampionShip(name='Serie B2', location='Italia', year=2023)
    B2.save()
    cB2 = Calendario(championship=B2)
    cB2.save()

    C = ChampionShip(name='Serie C', location='Italia', year=2023)
    C.save()
    cC = Calendario(championship=C)
    cC.save()
    gC = Giornata(num=1, calendario=cC)
    gC.save()
    D = ChampionShip(name='Serie D', location='Italia', year=2023)
    D.save()
    cD = Calendario(championship=D)
    cD.save()

    # Serie A1
    Reggiana = Team(name='Pallacanestro Reggiana', main_sponsor='UnaHotels', city='Reggio Emilia', championships=A1)
    Reggiana.save()
    Milano = Team(name='OlimpiaMilano', main_sponsor='Emporio Armani', city='Milano', championships=A1)
    Milano.save()
    Virtus = Team(name='Virtus Bologna', main_sponsor='Segafredo', city='Bologna', championships=A1)
    Virtus.save()
    Brindisi = Team(name='Pallacanestro Brindisi', main_sponsor='Happy Casa', city='Brindisi', championships=A1)
    Brindisi.save()

    # Serie A2

    # Serie B1

    # Serie B2

    # Serie C
    Novellara = Team(name='Pallacanestro Novellara', main_sponsor='Max Devil', city='Novellara', championships=C,
                     img=File(open('static/img/team_000296_2023_CS_PallacanestroNovellara.jpg', 'rb')))
    Novellara.save()
    g4 = Player(name='Nicolo', last_name='Ferrari', birth_date='1999-9-12', number=4, team=Novellara)
    g4.save()
    g5 = Player(name='Matteo', last_name='Frediani', birth_date='2004-12-09', number=5, team=Novellara)
    g5.save()
    g6 = Player(name='Marco', last_name='Morini', birth_date='2002-03-04', number=6, team=Novellara)
    g6.save()

    ReBasket = Team(name='ReBasket', main_sponsor='None', city='Reggio Emilia', championships=C,
                    img=File(open('static/img/team_022281_2023_CS_RebasketCastelnovoSotto.jpg', 'rb')))
    ReBasket.save()
    g16 = Player(name='Riccardo', last_name='Amadio', birth_date='1993-01-02', number=16, team=ReBasket)
    g16.save()
    g17 = Player(name='Riccardo', last_name='Bertolini', birth_date='1993-01-02', number=17, team=ReBasket)
    g17.save()
    Correggio = Team(name='Pallacanestro Correggio', main_sponsor='SPAL', city='Correggio', championships=C)
    Correggio.save()
