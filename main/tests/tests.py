from django.test import TestCase, Client
from main.models import *
from main.views import *

class ViewTestcase(TestCase):
    def setUp(self):
        self.client = Client()
        self.teamA = Team.objects.create()