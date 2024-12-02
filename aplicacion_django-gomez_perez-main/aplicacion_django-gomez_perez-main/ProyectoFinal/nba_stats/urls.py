from django.urls import path
from nba_stats import views

app_name="nba_stats"
urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("players/", views.players, name="players"),
    path("player_detail/<int:player_id>", views.player_detail, name="player_detail"),
    path("teams/", views.teams, name="teams"),
    path("ranking/", views.ranking, name="ranking"),
    path("searchteam/", views.searchteam, name="searchteam"),
    path("lista_jugadores/", views.lista_jugadores, name="lista_jugadores"),
    path('calendar_teams/', views.generate_calendar, name='generate_calendar'),

    # path('pie-chart/', views.pie_chart, name='pie-chart'),
    # path("player_image/<str:player_name>/", views.player_images, name="player_image"),
]