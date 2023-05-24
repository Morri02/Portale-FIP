from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.contrib import admin
from .initcmds import *
from django.contrib.auth import views as auth_views



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
    path('create/player/', CreatePlayerView.as_view(), name='create-player'),
    path('add/player/<int:team_id>', add_player, name='add-player'),
    path('update/player/<int:pk>', UpdatePlayerView.as_view(), name='update-player'),
    path('delete/player/<int:pk>/', DeletePlayerView.as_view(), name='delete-player'),

    path('get_teams/', get_teams, name='get_teams'),

    path('player/search/', player_search, name='player_search'),

    #path('create/match/', CreateMatchView.as_view(), name='create-match'),
    path('create/match/<int:giornata_id>/', create_match, name='create-match'),

    path('create/giornata/<int:campionato_id>/', create_giornata, name='create-giornata'),
    path('delete/giornata/<int:pk>/', DeleteGiornataView.as_view(), name='delete-giornata'),

    path('create/team/', CreateTeamView.as_view(), name='create-team'),
    path('add/team/<int:campionato_id>', add_team, name='add-team'),
    path('update/team/<int:pk>', UpdateTeamView.as_view(), name='update-team'),
    path('delete/team/<int:pk>', DeleteTeamView.as_view(), name='delete-team'),

    #path('player<int:pk>/count/', count_points, name='points-count'),

    #path('create/stat/', CreateStatView.as_view(), name='create-stat'),
    path('create/tabellinoA/<int:match_id>/', create_tabellinoA, name='create-tabellinoA'),
    path('create/nuovo/tabellinoA/<int:match_id>/', create_tabellinoA, name='create-nuovo-tabellinoA'),
    path('create/tabellinoB/<int:match_id>/', create_tabellinoB, name='create-tabellinoB'),
    path('create/nuovo/tabellinoB/<int:match_id>/', create_tabellinoB, name='create-nuovo-tabellinoB'),


    path('detail/match/<int:pk>', DetailMatchView.as_view(), name='match-detail'),

    path('detail/campionato/<int:pk>', DetailCalendarioView.as_view(), name='detail-calendario'),

    #log in e out
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', UserCreateView.as_view(), name='signup'),

    path('dashboard/', dashboard_view, name='dashboard'),

    path('get/all/matches', get_all_matches, name='all-matches'),
    path('get/day<int:day_id>/matches', get_matches_by_giornata, name='day-matches'),

    path('add/comment/<int:match_id>', add_comment, name='add-comment'),
    path('delete/commento/<int:comment_id>/', delete_comment, name='delete-comment'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

check_stats()

# erase_db()
# init_db()