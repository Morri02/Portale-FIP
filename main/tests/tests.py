from django.test import TestCase, Client

from main.models import *
from main.views import *

from django.test import TestCase, Client
from main.models import *
from main.views import *
from main.urls import *


# Create your tests here.

class MatchTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_1', password='test_1')

        self.client = Client()

        self.campionato = ChampionShip.objects.create(name='Serie C', location='Italia', year=2023)
        self.calendario = Calendario.objects.create(championship=self.campionato)
        self.team_novellara = Team.objects.create(name='Pallacanestro Novellara', main_sponsor='Max Devil',
                                                  city='Novellara', championships=self.campionato, img=File(
                open('static/img/team_000296_2023_CS_PallacanestroNovellara.jpg', 'rb')))
        self.team_rebasket = Team.objects.create(name='ReBasket', main_sponsor='MLSerramenti',
                                                 city='Reggio Emilia', championships=self.campionato, img=File(
                open('static/img/team_022281_2023_CS_RebasketCastelnovoSotto.jpg', 'rb')))

        self.giocatore1 = Player.objects.create(
            name='Marco', last_name='Morini',
            birth_date=timezone.make_aware(timezone.datetime(2002, 3, 4), timezone.get_default_timezone(), is_dst=None),
            number=6, team=self.team_novellara
        )

        self.giocatore2 = Player.objects.create(
            name='Matteo', last_name='Frediani',
            birth_date=timezone.make_aware(timezone.datetime(2004, 12, 24), timezone.get_default_timezone(),
                                           is_dst=None),
            number=5, team=self.team_novellara
        )

        self.giocatore3 = Player.objects.create(
            name='Riccardo', last_name='Amadio',
            birth_date=timezone.make_aware(timezone.datetime(1999, 11, 11), timezone.get_default_timezone(),
                                           is_dst=None),
            number=11, team=self.team_rebasket
        )

        self.giocatore4 = Player.objects.create(
            name='Gianmarco', last_name='Bertolini',
            birth_date=timezone.make_aware(timezone.datetime(1992, 1, 21), timezone.get_default_timezone(),
                                           is_dst=None),
            number=17, team=self.team_rebasket
        )

        self.giornata1 = Giornata.objects.create(num=1, calendario=self.calendario)
        self.partita = Match.objects.create(date=timezone.now(), teamA=self.team_novellara, teamB=self.team_rebasket,
                                            location='Novellara', giornata=self.giornata1)

    def test_tabellinoA(self):
        # Effettua il login come utente
        self.client.login(username='test_1', password='test_1')

        # Simula l'azione dell'utente che crea un tabellino per la partita
        tabellino1 = {
            'player1': self.giocatore1.pk, 'points1': 10, 'rebounds1': 12, 'blocks1': 5,
            'player2': self.giocatore2.pk, 'points2': 12, 'rebounds2': 3, 'blocks2': 10,
        }
        for i in range(3, 13):
            tabellino1['player' + str(i)] = ''
            tabellino1['points' + str(i)] = ''
            tabellino1['rebounds' + str(i)] = ''
            tabellino1['blocks' + str(i)] = ''

        response = self.client.post(reverse('main:create-tabellinoA', args=[self.partita.id]), tabellino1)
        # Verifica se la risposta HTTP è corretta (ad esempio, reindirizzamento a una pagina successiva)
        self.assertEqual(response.status_code, 302)

        # Recupera le istanze
        partita = Match.objects.get(id=self.partita.id)
        tabellino = Tabellino.objects.get(partitaA=self.partita)

        # Calcola la somma dei punti nel tabellino
        tabellino_points_sum = sum([stat.points if stat else 0 for stat in tabellino.get_stats()])

        # Verifica se la somma dei punti nel tabellino è uguale al valore della variabile points della partita
        self.assertEqual(tabellino_points_sum, partita.pointsA)
        self.assertEqual(22, partita.pointsA)
        # Giocatore 1
        self.assertEqual(tabellino.stat1.player.id, self.giocatore1.id)
        self.assertEqual(tabellino.stat1.points, 10)
        self.assertEqual(tabellino.stat1.rebounds, 12)
        self.assertEqual(tabellino.stat1.blocks, 5)
        # Giocatore 2
        self.assertEqual(tabellino.stat2.player.id, self.giocatore2.id)
        self.assertEqual(tabellino.stat2.points, 12)
        self.assertEqual(tabellino.stat2.rebounds, 3)
        self.assertEqual(tabellino.stat2.blocks, 10)

    def test_tabellinoB(self):
        # Effettua il login come utente
        self.client.login(username='test_1', password='test_1')

        # Simula l'azione dell'utente che crea un tabellino per la partita
        tabellino1 = {
            'player1': self.giocatore3.pk, 'points1': 10, 'rebounds1': 12, 'blocks1': 5,
            'player2': self.giocatore4.pk, 'points2': 12, 'rebounds2': 3, 'blocks2': 10,
        }
        for i in range(3, 13):
            tabellino1['player' + str(i)] = ''
            tabellino1['points' + str(i)] = ''
            tabellino1['rebounds' + str(i)] = ''
            tabellino1['blocks' + str(i)] = ''

        response = self.client.post(reverse('main:create-tabellinoB', args=[self.partita.id]), tabellino1)
        # Verifica se la risposta HTTP è corretta (ad esempio, reindirizzamento a una pagina successiva)
        self.assertEqual(response.status_code, 302)

        # Recupera le istanze
        partita = Match.objects.get(id=self.partita.id)
        tabellino = Tabellino.objects.get(partitaB=self.partita)

        # Calcola la somma dei punti nel tabellino
        tabellino_points_sum = sum([stat.points if stat else 0 for stat in tabellino.get_stats()])

        # Verifica se la somma dei punti nel tabellino è uguale al valore della variabile points della partita
        self.assertEqual(tabellino_points_sum, partita.pointsB)
        self.assertEqual(22, partita.pointsB)
        # Giocatore 3
        self.assertEqual(tabellino.stat1.player.id, self.giocatore3.id)
        self.assertEqual(tabellino.stat1.points, 10)
        self.assertEqual(tabellino.stat1.rebounds, 12)
        self.assertEqual(tabellino.stat1.blocks, 5)

        # Giocatore 4
        self.assertEqual(tabellino.stat2.player.id, self.giocatore4.id)
        self.assertEqual(tabellino.stat2.points, 12)
        self.assertEqual(tabellino.stat2.rebounds, 3)
        self.assertEqual(tabellino.stat2.blocks, 10)

        # Controllo che non possa inserire un nuovo tabellino solo perchè si èsalvato l'URL
        response = self.client.post(reverse('main:create-tabellinoB', args=[self.partita.id]), tabellino1)
        self.assertEqual(response.status_code, 403)

    def test_commento_e_like_dislike(self):
        self.client.login(username='test_1', password='test_1')

        response = self.client.post(reverse('main:add-comment', args=[self.partita.id]), {'content': 'Test Commenti'})

        # Verifica se la risposta HTTP è corretta (ad esempio, reindirizzamento a una pagina successiva)
        self.assertEqual(response.status_code, 302)

        comment = Commento.objects.get(created_by=self.user.id, match_id=self.partita.id)

        self.assertEqual('Test Commenti', comment.comment)

        response = self.client.post(reverse('main:like-comment'), {'comment_id': comment.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comment.likes.count(), 1)

        response = self.client.post(reverse('main:dislike-comment'), {'comment_id': comment.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(comment.likes.count(), 0)
        self.assertEqual(comment.dislikes.count(), 1)


class DashBoardTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='admin')
        self.client = Client()
        self.campionato = ChampionShip.objects.create(name='Serie C', location='Italia', year=2023)
        self.calendario = Calendario.objects.create(championship=self.campionato)

        self.team_novellara = Team.objects.create(name='Pallacanestro Novellara', main_sponsor='Max Devil',
                                                  city='Novellara', championships=self.campionato, img=File(
                open('static/img/team_000296_2023_CS_PallacanestroNovellara.jpg', 'rb')))
        self.team_rebasket = Team.objects.create(name='ReBasket', main_sponsor='MLSerramenti',
                                                 city='Reggio Emilia', championships=self.campionato, img=File(
                open('static/img/team_022281_2023_CS_RebasketCastelnovoSotto.jpg', 'rb')))

        self.giocatore1 = Player.objects.create(
            name='Marco', last_name='Morini',
            birth_date=timezone.make_aware(timezone.datetime(2002, 3, 4), timezone.get_default_timezone(), is_dst=None),
            number=6, team=self.team_novellara
        )

        self.giocatore2 = Player.objects.create(
            name='Matteo', last_name='Frediani',
            birth_date=timezone.make_aware(timezone.datetime(2004, 12, 24), timezone.get_default_timezone(),
                                           is_dst=None),
            number=5, team=self.team_novellara
        )

        self.giocatore3 = Player.objects.create(
            name='Riccardo', last_name='Amadio',
            birth_date=timezone.make_aware(timezone.datetime(1999, 11, 11), timezone.get_default_timezone(),
                                           is_dst=None),
            number=11, team=self.team_rebasket
        )

        self.giocatore4 = Player.objects.create(
            name='Gianmarco', last_name='Bertolini',
            birth_date=timezone.make_aware(timezone.datetime(1992, 1, 21), timezone.get_default_timezone(),
                                           is_dst=None),
            number=17, team=self.team_rebasket
        )

        self.giornata1 = Giornata.objects.create(num=1, calendario=self.calendario)

        self.statA1 = Stat.objects.create(player=self.giocatore1, points=10, rebounds=12, blocks=5)
        self.statA2 = Stat.objects.create(player=self.giocatore2, points=12, rebounds=1, blocks=8)
        self.statB1 = Stat.objects.create(player=self.giocatore3, points=10, rebounds=12, blocks=5)
        self.statB2 = Stat.objects.create(player=self.giocatore4, points=12, rebounds=1, blocks=8)
        self.tabellinoA = Tabellino.objects.create(stat1=self.statA1, stat2=self.statA2)
        self.tabellinoB = Tabellino.objects.create(stat1=self.statB1, stat2=self.statB2)

        self.partita = Match.objects.create(date=timezone.now(), teamA=self.team_novellara, teamB=self.team_rebasket,
                                            tabellinoA=self.tabellinoA, tabellinoB=self.tabellinoB,
                                            location='Novellara', giornata=self.giornata1)

    def test_creazione_giornata(self):
        self.client.login(username='admin', password='admin')

        #       Creo altre due giornate(la 2 e la 3)
        response = self.client.post(reverse('main:create-giornata', args=[self.campionato.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('main:create-giornata', args=[self.campionato.id]))
        self.assertEqual(response.status_code, 302)

        giornata2 = Giornata.objects.get(calendario_id=self.calendario.id, num=2)
        self.assertIsNotNone(giornata2)
        giornata3 = Giornata.objects.get(calendario_id=self.calendario.id, num=3)
        self.assertIsNotNone(giornata3)

        # Cancello la prima
        giornata2.delete()
        response = self.client.post(reverse('main:create-giornata', args=[self.campionato.id]))
        self.assertEqual(response.status_code, 302)
        giornata2 = Giornata.objects.get(calendario_id=self.calendario.id, num=2)
        self.assertIsNotNone(giornata2)
        self.assertFalse(Giornata.objects.filter(calendario_id=self.calendario.id, num=4).exists())

    def test_cancellazione_tabellino(self):
        self.client.login(username='admin', password='admin')

        response = self.client.post(reverse('main:delete-tabellino', args=[self.tabellinoA.id]))
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.partita.pointsA, 0)
        self.assertIsNotNone(self.tabellinoA)
