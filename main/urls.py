from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.contrib import admin
from .initcmds import *

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', home_page, name='homepage'),
    path('list/players/', ListPlayerView.as_view(), name='list-players'),
    path('list/teams/', ListTeamView.as_view(), name='list-teams'),
    path('list/championships/', ListChampionshipView.as_view(), name='list-championships'),
    path('list/matches', ListMatchView.as_view(), name='list-matches'),
    path('players/<int:pk>/', DetailPlayerView.as_view(), name='player-detail'),
    path('teams/<int:pk>/', DetailTeamView.as_view(), name='team-detail'),
    path('testbase/', test_base, name='test-base'),
    path('register/', register_page, name='register'),
    path('login/', register_page, name='log-in'),
    path('create/player/', CreatePlayerView.as_view(), name='create-player'),
    path('update/player/<int:pk>', UpdatePlayerView.as_view(), name='update-player'),
    path('delete/player/<int:pk>/', DeletePlayerView.as_view(), name='delete-player'),

    path('get_teams/', get_teams, name='get_teams'),

    path('player/search/', player_search, name='player_search'),

    path('create/match/', CreateMatchView.as_view(), name='create-match'),

    #path('player<int:pk>/count/', count_points, name='points-count'),

    path('create/stat/', CreateStatView.as_view(), name='create-stat'),
    path('create/tabellino/<int:match_id>', create_tabellino, name='create-tabellino'),

    path('detail/match/<int:pk>', DetailMatchView.as_view(), name='match-detail')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

check_stats()

# erase_db()
# init_db()