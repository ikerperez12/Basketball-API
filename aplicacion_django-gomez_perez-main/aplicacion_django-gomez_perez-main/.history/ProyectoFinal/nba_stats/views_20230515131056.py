from django.shortcuts import render
from .models import Player,Team,Standing
from django.http import HttpResponse,HttpResponseRedirect
import requests
import matplotlib.pyplot as plt
import io
import urllib
from apis.NBA_API import *


from .forms import Conference
# Create your views here.

def home(request):
    return render(request,"nba_stats/home.html")

def players(request):
    return render(request,"nba_stats/players.html")


def player_stats(request):
    players = get_player_stats()
    for player in players:
        name = player['first_name'] + ' ' + player['last_name']
        team = player['team']['full_name']
        points = player['stats']['pts']
        rebounds = player['stats']['reb']
        assists = player['stats']['ast']
        Player.objects.create(name=name, team=team, points=points, rebounds=rebounds, assists=assists)
    players = Player.objects.all()
    context = {'players': players}
    return render(request, 'player_stats.html', context)

def team_stats(request):
    teams = get_player_stats()
    for team in teams:
        name = team['full_name']
        abbreviation = team['abbreviation']
        city = team['city']
        conference = team['conference']['name']
        division = team['division']['name']
        points = team['stats']['pts']
        rebounds = team['stats']['reb']
        assists = team['stats']['ast']
        steals = team['stats']['stl']
        blocks = team['stats']['blk']
        Team.objects.create(name=name, abbreviation=abbreviation, city=city, conference=conference, division=division, points=points, rebounds=rebounds, assists=assists, steals=steals, blocks=blocks)
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'team_stats.html', context)


# def teams(request):
#     # hacer una solicitud HTTP GET a la API
#     url = "https://api-nba-v1.p.rapidapi.com/teams"
    
#     headers = {
#             "X-RapidAPI-Key": "8817801bf2mshb20e23e57fd4d5fp1a5a79jsn9a7dc2502f46",
#             "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
#     }
    
#     response = requests.get(url,headers=headers)
#         # asegurarse de que la solicitud fue exitosa (código de estado 200)
#     if response.status_code == 200:
#         # cargar los datos JSON de la respuesta de la API
#         json_data = response.json()

#         # extraer la lista de objetos de equipo del objeto JSON
#         teams=json_data.get('response',[])

#         # pasar la lista de equipos como contexto a la plantilla
#         return render(request, 'nba_stats/teams.html', {'teams': teams})

#     # si la solicitud no fue exitosa, mostrar un mensaje de error
#     else:
#         error_message = 'Error al cargar los datos de la API'
#         return HttpResponse("Error")



def teams(request):
    teams=get_teams()
    return render(request, 'nba_stats/teams.html', {'teams': teams})

def searchteam(request):
    busquedaeq
def ranking(request):
    ranking=get_standings(2021)
    return render(request,"nba_stats/ranking.html",context={"ranking":ranking})


def player_efficiency_view(request):
    players = Player.objects.all()

    # Crear una instancia de la clase StatsPanda
    sp = StatsPanda()

    # Calcular el índice de eficiencia para cada jugador
    player_efficiencies = []
    for player in players:
        player_df = sp.get_player_stats(player.id, "2019-20")  # DataFrame para una temporada dada
        efficiency_rating = sp.calc_player_efficiency_rating(player_df)
        player_efficiencies.append((player, efficiency_rating))

    # Añadir los resultados al contexto de la plantilla
    context = {
        "player_efficiencies": player_efficiencies
    }

    return render(request, "player_efficiency.html", context)


def standings(request):
    eastern_teams = Team.objects.filter(conference='east').order_by('-conference_rank')
    western_teams = Team.objects.filter(conference='west').order_by('-conference_rank')
    standings = Standings.objects.all()
    context = {'eastern_teams': eastern_teams,
               'western_teams': western_teams,
               'standings': standings}
    return render(request, 'standings.html', context)

def team_efficiency_rating_view(request, team_name, season_year):
    # Obtener los datos de estadísticas de jugadores para el equipo y temporada dada
    # utilizando la API de la NBA y la biblioteca Pandas...

    # Calcular el índice de eficiencia del equipo
    efficiency_rating = calc_team_efficiency_rating(get)

    # Obtener el objeto Team correspondiente al nombre del equipo
    team = Team.objects.get(name=team_name)

    # Actualizar el índice de eficiencia del equipo en la base de datos
    team.efficiency_rating = efficiency_rating
    team.save()

    # Renderizar una plantilla HTML con la información de eficiencia del equipo
    return render(request, 'team_efficiency_rating.html', {'team_name': team_name, 'season_year': season_year, 'efficiency_rating': efficiency_rating})




def pie_chart(request):
    df = standingspandas.get_standings(2021)
    fig = standingspandas.create_pie_chart_by_conference(df)

    # Guardar gráfico en un objeto StringIO
    buffer = io.StringIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Convertir el objeto StringIO a un objeto de imagen de bytes y enviarlo al navegador
    image_png = buffer.getvalue()
    buffer.close()
    return HttpResponse(image_png, content_type="image/png")


def player_image(request, player_name):
    players = get_player_stats(player_name)
    if players:
        player = players[0]
        firstname = player["firstname"]
        lastname = player["lastname"]
        player_name = f"{firstname} {lastname}"
        image_url = search_player_images(player_name)
        if image_url:
            context = {"player_name": player_name, "image_url": image_url}
            return render(request, "player_image.html", context)
    return render(request, "player_image.html")