from django.urls import path

from nba_stats import views

app_name="nba_stats"
urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("players/", views.players, name="players"),
    path("teams/", views.teams, name="teams"),
    path("ranking/", views.ranking, name="ranking"),
    path("busquedasequipos/", views.searchteam, name="sear"),   
    # path('pie-chart/', views.pie_chart, name='pie-chart'),
    # path("player_image/<str:player_name>/", views.player_images, name="player_image"),
]