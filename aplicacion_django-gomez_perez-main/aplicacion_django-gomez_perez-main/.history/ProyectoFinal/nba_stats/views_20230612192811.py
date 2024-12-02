from django.shortcuts import render,redirect
from io import BytesIO
import base64
import matplotlib.pyplot as plt
#from ProyectoFinal.apis.statspandas import calculate_efficiency_rating
import numpy as np
#from ProyectoFinal.apis.statspandasv2 import format_player_stats
from .models import Player,Team,Standing
from django.http import HttpResponse,HttpResponseRedirect
import requests
import urllib
from django.contrib.auth.decorators import login_required
from .forms import Conference
from apis.NBA_API import *

##Librerias para imagen 
from PIL import Image,ImageOps
import base64
from io import BytesIO
###LISTA PARA GUARDAR JUGADORES
lista_dict_estadisticas=[]

# Create your views here.
def home(request):
    global lista_dict_estadisticas
    lista_dict_estadisticas.clear()
    return render(request,"nba_stats/home.html")

def generate_calendar(request):
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        season = request.POST.get('season')

        games = get_games_by_team_and_season(team_id, season)
        credentials_file_path = "ProyectoFinal/credenciales/credenciales.json"  # Ruta al archivo JSON de credenciales actualizado
        goocalendar = Goocalendar(credentials_file_path)
        goocalendar.process_games(games)

        # Obtén el enlace del calendario y los eventos creados
        calendar_link = goocalendar.get_calendar_link()
        event_links = goocalendar.get_event_links()

        context = {
            'calendar_link': calendar_link,
            'event_links': event_links
        }

        return render(request, 'calendar.html', context)

    return render(request, 'searchteamsseasons.html')


def formatear_imagen(url):
      response = requests.get(url)
      image = Image.open(BytesIO(response.content))
      border_size = 20  # Tamaño del marco en píxeles
      border_color = (255, 0, 0)
      image_with_border = ImageOps.expand(image, border=border_size, fill=border_color)
      resized_image = image_with_border.resize((300, 300))
      buffered = BytesIO()
      resized_image.save(buffered, format="JPEG")
      base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
      return base64_image


def obtener_estadisticas_jugador(json_estadisticas):
    global lista_dict_estadisticas
    df=pd.json_normalize(json_estadisticas,sep="-")
    nombre_jugador=df['player-firstname'][0]+' '+df['player-lastname'][0]
    equipo=df['team-name'][0]
    numeric_cols = df.select_dtypes(include=[int, float])
    medias=numeric_cols.drop(columns=['team-id','player-id','game-id']).mean()
    medias=pd.DataFrame(medias)
    tabla_medias=medias.copy()
    tabla_medias.columns=[nombre_jugador]
    tabla_medias=medias.to_html()
    estadisticas_partido = df.filter(regex="^(?!team\-)")
    estadisticas_partido = estadisticas_partido.filter(regex="^(?!player\-)")
    estadisticas_partido['comment']=estadisticas_partido['comment'].fillna('Sin comentario')
    estadisticas_partido=estadisticas_partido.fillna(0)
    tabla_estadisticas_partido=estadisticas_partido.to_html()
    url_imagen=search_player_images(nombre_jugador+' '+equipo)
    imagen=formatear_imagen(url_imagen)



    diccionario={'nombre':nombre_jugador,
                 'tabla_estadisticas':tabla_estadisticas_partido,
                 'tabla_medias':tabla_medias,
                 'imagen':imagen,
                 'estadisticas_partido':estadisticas_partido,
                 'medias':medias,
                #  'grafica_medias':grafica_medias,
                #  'grafica_estadisticas':grafica_estadisticas
                 }

    añadir_elemento_lista_jugadores(diccionario)


def añadir_elemento_lista_jugadores(diccionario):
    global lista_dict_estadisticas
    if len(lista_dict_estadisticas)==2:
        del lista_dict_estadisticas[0]
        lista_dict_estadisticas.insert(1,diccionario)
    else:
         lista_dict_estadisticas.append(diccionario)    
@login_required
def players(request):
    if request.method=='POST':
        nombre_jugador=request.POST.get('player_name','')
        if nombre_jugador=='':
            return render(request,"nba_stats/players.html")
        else:
            lista_jugadores=obtener_jugadores(nombre_jugador)
            context={'players':lista_jugadores}
            return render(request,"nba_stats/lista_jugadores.html",context)   
    else:
        return render(request,"nba_stats/players.html")     



def searchteam(request):
    if request.method == 'POST':
        nombre = request.POST.get('team_name', '')
        if nombre=='':
            return render(request,"nba_stats/searchteam.html")
    ##Descomentar esta linea  para hacer consultas
        #teams = search_team(nombre)
        #players = search_players_by_team_id(teams[0]['id'])
        #Fucion para probar la respuesta de la pagina pero sin llamar al API
        players=[{'id': 75, 'firstname': 'Jaylen', 'lastname': 'Brown', 'birth': {'date': '1996-10-24', 'country': 'USA'},
                   'nba': {'start': 2016, 'pro': 5}, 'height': {'feets': '6', 'inches': '6', 'meters': '1.98'}, 
                   'weight': {'pounds': '223', 'kilograms': '101.2'}, 'college': 'California', 'affiliation': 'California/USA', 
                   'leagues': {'standard': {'jersey': 7, 'active': True, 'pos': 'G-F'}}}, {'id': 71, 'firstname': 'Malcolm', 'lastname': 
                                                                                           'Brogdon', 'birth': {'date': '1992-12-11', 'country': 'USA'}, 'nba': {'start': 2016, 'pro': 5}, 'height': {'feets': '6', 'inches': '5', 'meters': '1.96'}, 'weight': {'pounds': '229', 'kilograms': '103.9'}, 'college': 'Virginia', 'affiliation': 'Virginia/USA', 'leagues': {'standard': {'jersey': 13, 'active': True, 'pos': 'G'}}}, {'id': 310, 'firstname': 'Jake', 'lastname': 'Layman', 'birth': {'date': '1994-03-07', 'country': 'USA'}, 'nba': {'start': 2016, 'pro': 5}, 'height': {'feets': '6', 'inches': '8', 'meters': '2.03'}, 'weight': {'pounds': '209', 'kilograms': '94.8'}, 'college': 'Maryland', 'affiliation': 'Maryland/USA', 'leagues': {'standard': {'jersey': 10, 'active': True, 'pos': 'F'}, 'vegas': {'jersey': 10, 'active': True, 'pos': 'F'}}}, {'id': 882, 'firstname': 'Jayson', 'lastname': 'Tatum', 'birth': {'date': '1998-03-03', 'country': 'USA'}, 'nba': {'start': 2017, 'pro': 4}, 'height': {'feets': '6', 'inches': '8', 'meters': '2.03'}, 'weight': {'pounds': '210', 'kilograms': '95.3'}, 'college': 'Duke', 'affiliation': 'Duke/USA', 'leagues': {'standard': {'jersey': None, 'active': True, 'pos': 'F-G'}}}, {'id': 806, 'firstname': 'Justin', 'lastname': 'Jackson', 'birth': {'date': '1995-03-28', 'country': 'USA'}, 'nba': {'start': 2017, 'pro': 0}, 'height': {'feets': None, 'inches': None, 'meters': None}, 'weight': {'pounds': None, 'kilograms': None}, 'college': 'North Carolina', 'affiliation': 'North Carolina/USA', 'leagues': {'standard': {'jersey': 44, 'active': True, 'pos': 'F'}, 'sacramento': {'jersey': 25, 'active': True, 'pos': 'F'}, 'vegas': {'jersey': 52, 'active': True, 'pos': 'F'}}}, {'id': 897, 'firstname': 'Derrick', 'lastname': 'White', 'birth': {'date': '1994-07-02', 'country': 'USA'}, 'nba': {'start': 2017, 'pro': 4}, 'height': {'feets': '6', 'inches': '4', 'meters': '1.93'}, 'weight': {'pounds': '190', 'kilograms': '86.2'}, 'college': 'Colorado', 'affiliation': 'Colorado/USA', 'leagues': {'standard': {'jersey': 9, 'active': True, 'pos': 'G'}, 'vegas': {'jersey': 4, 'active': True, 'pos': 'G'}, 'utah': {'jersey': 4, 'active': True, 'pos': 'G'}}}, {'id': 819, 'firstname': 'Luke', 'lastname': 'Kornet', 'birth': {'date': '1995-07-15', 'country': 'USA'}, 'nba': {'start': 2017, 'pro': 4}, 'height': {'feets': '7', 'inches': '2', 'meters': '2.18'}, 'weight': {'pounds': '250', 'kilograms': '113.4'}, 'college': 'Vanderbilt', 'affiliation': 'Vanderbilt/USA', 'leagues': {'standard': {'jersey': 40, 'active': True, 'pos': 'C-F'}, 'vegas': {'jersey': 2, 'active': True, 'pos': 'F-C'}}}, {'id': 1045, 'firstname': 'Robert', 'lastname': 'Williams III', 'birth': {'date': '1997-10-17', 'country': 'USA'}, 'nba': {'start': 2018, 'pro': 3}, 'height': {'feets': '6', 'inches': '9', 'meters': '2.06'}, 'weight': {'pounds': '237', 'kilograms': '107.5'}, 'college': 'Texas A&M', 'affiliation': 'Texas A&M/USA', 'leagues': {'standard': {'jersey': 44, 'active': True, 'pos': 'C-F'}, 'vegas': {'jersey': 44, 'active': True, 'pos': 'C'}}}, {'id': 1873, 'firstname': 'Mfiondu', 'lastname': 'Kabengele', 'birth': {'date': None, 'country': None}, 'nba': {'start': 0, 'pro': 0}, 'height': {'feets': None, 'inches': None, 'meters': None}, 'weight': {'pounds': None, 'kilograms': None}, 'college': None, 'affiliation': None, 'leagues': {'standard': {'jersey': 27, 'active': True, 'pos': 'C'}, 'vegas': {'jersey': 28, 'active': True, 'pos': 'F-C'}}}, {'id': 1891, 'firstname': 'Luka', 'lastname': 'Samanic', 'birth': {'date': None, 'country': None}, 'nba': {'start': 0, 'pro': 0}, 'height': {'feets': None, 'inches': None, 'meters': None}, 'weight': {'pounds': None, 'kilograms': None}, 'college': None, 'affiliation': None, 'leagues': {'standard': {'jersey': 99, 'active': False, 'pos': None}, 'utah': {'jersey': 19, 'active': True, 'pos': 'F'}, 'vegas': {'jersey': 19, 'active': True, 'pos': 'F'}}}, {'id': 1901, 'firstname': 'Grant', 'lastname': 'Williams', 'birth': {'date': '1998-11-30', 'country': 'USA'}, 'nba': {'start': 2019, 'pro': 2}, 'height': {'feets': '6', 'inches': '6', 'meters': '1.98'}, 'weight': {'pounds': '236', 'kilograms': '107.0'}, 'college': 'Tennessee', 'affiliation': 'Tennessee/USA', 'leagues': {'standard': {'jersey': 12, 'active': True, 'pos': 'F'}, 'vegas': {'jersey': 40, 'active': True, 'pos': 'F'}}}, {'id': 2635, 'firstname': 'Payton', 'lastname': 'Pritchard', 'birth': {'date': '1998-01-28', 'country': 'USA'}, 'nba': {'start': 2020, 'pro': 1}, 'height': {'feets': '6', 'inches': '1', 'meters': '1.85'}, 'weight': {'pounds': '195', 'kilograms': '88.5'}, 'college': 'Oregon', 'affiliation': 'Oregon/USA', 'leagues': {'standard': {'jersey': 11, 'active': True, 'pos': 'G'}, 'vegas': {'jersey': 11, 'active': True, 'pos': 'G'}}}, {'id': 2654, 'firstname': 'Brodric', 'lastname': 'Thomas', 'birth': {'date': '1997-01-28', 'country': 'USA'}, 'nba': {'start': 2020, 'pro': 1}, 'height': {'feets': '6', 'inches': '5', 'meters': '1.96'}, 'weight': {'pounds': '185', 'kilograms': '83.9'}, 'college': 'Truman State', 'affiliation': 'Truman State/USA', 'leagues': {'standard': {'jersey': 97, 'active': True, 'pos': 'G'}, 'vegas': {'jersey': 97, 'active': True, 'pos': 'G'}}}, {'id': 2798, 'firstname': 'Justin', 'lastname': 'Champagnie', 'birth': {'date': '2001-06-29', 'country': 'USA'}, 'nba': {'start': 2021, 'pro': 0}, 'height': {'feets': '6', 'inches': '6', 'meters': '1.98'}, 'weight': {'pounds': '206', 'kilograms': '93.4'}, 'college': 'Pittsburgh', 'affiliation': 'Pittsburgh/USA', 'leagues': {'standard': {'jersey': 11, 'active': True, 'pos': 'G-F'}, 'vegas': {'jersey': 11, 'active': True, 'pos': 'F'}}}, {'id': 2812, 'firstname': 'Sam', 'lastname': 'Hauser', 'birth': {'date': '1997-12-08', 'country': 'USA'}, 'nba': {'start': 2021, 'pro': 0}, 'height': {'feets': '6', 'inches': '7', 'meters': '2.01'}, 'weight': {'pounds': '217', 'kilograms': '98.4'}, 'college': 'Virginia', 'affiliation': 'Virginia/USA', 'leagues': {'standard': {'jersey': 30, 'active': True, 'pos': 'F'}, 'vegas': {'jersey': 30, 'active': True, 'pos': 'F'}}}, {'id': 3429, 'firstname': 'JD', 'lastname': 'Davison', 'birth': {'date': None, 'country': None}, 'nba': {'start': 0, 'pro': 0}, 'height': {'feets': None, 'inches': None, 'meters': None}, 'weight': {'pounds': None, 'kilograms': None}, 'college': None, 'affiliation': None, 'leagues': {'standard': {'jersey': 20, 'active': True, 'pos': 'G'}}}, {'id': 248, 'firstname': 'Al', 'lastname': 'Horford', 'birth': {'date': '1986-06-03', 'country': 'Dominican Republic'}, 'nba': {'start': 2007, 'pro': 14}, 'height': {'feets': '6', 'inches': '9', 'meters': '2.06'}, 'weight': {'pounds': '240', 'kilograms': '108.9'}, 'college': 'Florida', 'affiliation': 'Florida/Dominican Republic', 'leagues': {'standard': {'jersey': 42, 'active': True, 'pos': 'C-F'}}}, {'id': 181, 'firstname': 'Danilo', 'lastname': 'Gallinari', 'birth': {'date': '1988-08-08', 'country': 'Italy'}, 'nba': {'start': 2008, 'pro': 12}, 'height': {'feets': '6', 'inches': '10', 'meters': '2.08'}, 'weight': {'pounds': '236', 'kilograms': '107.0'}, 'college': 'Olimpia Milano', 'affiliation': 'Olimpia Milano/Italy', 'leagues': {'standard': {'jersey': 8, 'active': True, 'pos': 'F'}, 'africa': {'jersey': 8, 'active': True, 'pos': 'F'}}}, {'id': 208, 'firstname': 'Blake', 'lastname': 'Griffin', 'birth': {'date': '1989-03-16', 'country': 'USA'}, 'nba': {'start': 2010, 'pro': 11}, 'height': {'feets': '6', 'inches': '9', 'meters': '2.06'}, 'weight': {'pounds': '250', 'kilograms': '113.4'}, 'college': 'Oklahoma', 'affiliation': 'Oklahoma/USA', 'leagues': {'standard': {'jersey': 91, 'active': True, 'pos': 'F'}}}, {'id': 384, 'firstname': 'Mike', 'lastname': 'Muscala', 'birth': {'date': '1991-07-01', 'country': 'USA'}, 'nba': {'start': 2013, 'pro': 8}, 'height': {'feets': '6', 'inches': '10', 'meters': '2.08'}, 'weight': {'pounds': '240', 'kilograms': '108.9'}, 'college': 'Bucknell', 'affiliation': 'Bucknell/USA', 'leagues': {'standard': {'jersey': 33, 'active': True, 'pos': 'F-C'}}}, {'id': 486, 'firstname': 'Marcus', 'lastname': 'Smart', 'birth': {'date': '1994-03-06', 'country': 'USA'}, 'nba': {'start': 2014, 'pro': 7}, 'height': {'feets': '6', 'inches': '4', 'meters': '1.93'}, 'weight': {'pounds': '220', 'kilograms': '99.8'}, 'college': 'Oklahoma State', 'affiliation': 'Oklahoma State/USA', 'leagues': {'standard': {'jersey': 36, 'active': True, 'pos': 'G'}}}, {'id': 533, 'firstname': 'Noah', 'lastname': 'Vonleh', 'birth': {'date': None, 'country': None}, 'nba': {'start': 0, 'pro': 0}, 'height': {'feets': None, 'inches': None, 'meters': None}, 'weight': {'pounds': None, 'kilograms': None}, 'college': None, 'affiliation': None, 'leagues': {'standard': {'jersey': 4, 'active': True, 'pos': 'F'}}}]
        teams=[{'id': 2, 'name': 'Celtics', 'nickname': 'BOS', 'city': 'Boston', 'logo': 'https://upload.wikimedia.org/wikipedia/fr/thumb/6/65/Celtics_de_Boston_logo.svg/1024px-Celtics_de_Boston_logo.svg.png'}]
        return render(request, 'nba_stats/searchteam.html', {'teams': teams,'players':players})    
    return render(request,"nba_stats/searchteam.html")


def ranking(request):
    df=get_standings(2022)
    rank_east =df.loc[df['conference.name'] == 'east'].sort_values('conference.rank')
    rank_west =df.loc[df['conference.name'] == 'west'].sort_values('conference.rank')
    columnas_seleccionadas = ['conference.rank','team.name','conference.win','conference.loss']
    rank_east=rank_east[columnas_seleccionadas]
    rank_west=rank_west[columnas_seleccionadas]
    ranking_general=pd.concat([rank_west,rank_east])
    ranking_general=ranking_general.sort_values(by=['conference.rank','conference.win'],ascending=[True,False])
    ranking_general=ranking_general[columnas_seleccionadas]
    rank_east=rank_east.to_html()
    rank_west=rank_west.to_html()
    ranking_general=ranking_general.to_html()
    return render(request,"nba_stats/ranking.html",context={"rank_east":rank_east,'rank_west':rank_west,'ranking_general':ranking_general})

def generar_grafica_medias():
    global lista_dict_estadisticas
    medias_1=lista_dict_estadisticas[0]['medias']
    medias_2=lista_dict_estadisticas[1]['medias']
    nombre_indices=medias_1[0].index
    indices=np.arange(len(nombre_indices))
    values1=medias_1[0].values
    values2=medias_2[0].values
    plt.figure(figsize=(10, 6))
    bar_width = 0.35  # Ancho de las barras
    plt.bar(indices, values1,bar_width,label=lista_dict_estadisticas[0]['nombre'],color="blue")
    plt.bar(indices+bar_width,values2,bar_width,label=lista_dict_estadisticas[1]['nombre'],color="green")
    plt.xticks(indices, nombre_indices)
    plt.xlabel('Estadísticas')
    plt.ylabel('Valor')
    plt.title('Estadísticas del jugador')
    plt.xticks(rotation=90)
    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la gráfica a base64
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')    
    return graphic
    
    
def generar_grafica_estadisticas():
    global lista_dict_estadisticas
    if len(lista_dict_estadisticas) == 2:
        df1 = lista_dict_estadisticas[0]['estadisticas_partido']
        df2 = lista_dict_estadisticas[1]['estadisticas_partido']
        num_juegos = max(len(df1), len(df2))  # Número total de juegos
        df1 = df1.reindex(range(num_juegos)).fillna(0)
        df2 = df2.reindex(range(num_juegos)).fillna(0)

        # Configuración de la gráfica
        plt.figure(figsize=(20, 12))
        bar_width = 0.35  # Ancho de las barras
        index = np.arange(num_juegos)

        # Generar las barras para cada jugador
        plt.bar(index, df1["points"], bar_width, label=lista_dict_estadisticas[0]['nombre'], color="red")
        plt.bar(index + bar_width, df2["points"], bar_width, label=lista_dict_estadisticas[1]['nombre'], color="green")

        # Configuración de los ejes y etiquetas
        plt.xlabel("Juego")
        plt.ylabel("Puntos")
        plt.title("Comparación de Puntos por Partido")

        # Añade leyenda
        plt.legend()

        # Configuración de las etiquetas del eje x
        plt.xticks(index + bar_width / 2, range(1, num_juegos + 1), rotation=90)

        plt.tight_layout()
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Convertir la gráfica a base64
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')    
        return graphic




def player_detail(request,player_id):
    global lista_dict_estadisticas
    ##Comentamos esto para leer el contenido desde un json en vez del api
    json_estadisticas=get_player_stadistics_by_id(player_id)
    if json_estadisticas:
        obtener_estadisticas_jugador(json_estadisticas)
        if(len(lista_dict_estadisticas)==2):
            grafica_medias=generar_grafica_medias()
            grafica_estadisticas=generar_grafica_estadisticas()
            context={'lista_jugadores': lista_dict_estadisticas,
                    'grafica_medias':grafica_medias,
                    'grafica_estadisticas':grafica_estadisticas
                    }
            return render(request,"nba_stats/player_detail.html",context=context)
        else:
            context={'lista_jugadores': lista_dict_estadisticas,
                    }
            return render(request,"nba_stats/player_detail.html",context=context)
    else:
        return render(request,"nba_stats/player_detail.html")


def lista_jugadores(request):
    if request.method=='POST':
        #Si enviamos el formulario con un nombre obtener_jugadores() filtra el apellido y nos devuelve una lista de jugadores
            players=obtener_jugadores(request.POST.get('player_name',''))
        #players=obtener_jugadores("Stephen Curry")
        #Si obtenemos 1 solo resultado mostramos las estadisticas de player_detail
            if len(players)==1:
                 return render(request,"nba_stats/lista_jugadores.html",{'players':players})
                # player=get_player_stadistics_by_id(players[0]['id'])
                # context=formatear_jugador(player)
                # return render(request,"nba_stats/player_detail.html",context=context)
        #Si obtenemos mas de 1 resultado mostraremos una lista de los jugadores     
            elif len(players)>1:
                return render(request,"nba_stats/lista_jugadores.html",{'players':players})
        #En otro caso mostraremos un error    
            else:
                return render(request,"nba_stats/lista_jugadores.html",{'errors':True})
    #Si recargamos la pagina, nos la muestra por defecto
    else:
        años=list(range(2015, 2023))
        return render(request,"nba_stats/lista_jugadores.html",{'años':años})

@login_required
def players2(request):
    if request.method == 'POST':
        nombre = request.POST.get('player_name', '')  # Obtiene el valor del campo 'nombre' del formulario
        try:
            id=get_player_by_name(nombre)[0]['id']
            player=get_player_stadistics_by_id(id)
            df=pd.json_normalize(player)
            traducciones = {
                'points': 'Puntos',
                'pos': 'Posición',
                'min': 'Minutos',
                'fgm': 'Tiros de Campo Convertidos',
                'fga': 'Tiros de Campo Intentados',
                'fgp': 'Porcentaje de Tiros de Campo',
                'ftm': 'Tiros Libres Convertidos',
                'fta': 'Tiros Libres Intentados',
                'ftp': 'Porcentaje de Tiros Libres',
                'tpm': 'Triples Convertidos',
                'tpa': 'Triples Intentados',
                'tpp': 'Porcentaje de Triples',
                'offReb': 'Rebotes Ofensivos',
                'defReb': 'Rebotes Defensivos',
                'totReb': 'Total de Rebotes',
                'assists': 'Asistencias',
                'pFouls': 'Faltas Personales',
                'steals': 'Robos de Balón',
                'turnovers': 'Pérdidas de Balón',
                'blocks': 'Tiros Bloqueados',
                'plusMinus': 'plusMinus',
                'comment': 'Comentario',
                'game.id': 'ID del Partido'
            }

            # Renombrar las columnas
            df = df.rename(columns=traducciones)

            ##Generamos Gráfica
            plt.plot(df['Puntos'])
            plt.xlabel('Partido')
            plt.ylabel('Puntos')
            plt.title('Puntos por Partido')
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            ##
            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')            

            # Rellenar los campos na
            df['Comentario'] = df['Comentario'].fillna('Sin comentarios')
            # Calcular el PER utilizando las estadísticas disponibles en el JSON
            df['PER'] = (1 / df['Minutos'].apply(convertir_tiempo_a_entero)) * (df['Puntos'] + (df['Tiros de Campo Convertidos'] * 0.85) + (df['Triples Convertidos'] * 0.53) + (df['Tiros Libres Convertidos'] * 0.44) + (df['Rebotes Ofensivos'] * 0.7) + (df['Rebotes Defensivos'] * 0.3) + df['Asistencias'] + df['Robos de Balón'] + df['Tiros Bloqueados'] - df['Pérdidas de Balón'])

                    #Calculamos las medias de la temporada
            # Calcular las medias y redondear a un decimal
            media_puntos = df['Puntos'].mean().round(1)
            media_asistencias = df['Asistencias'].mean().round(1)
            media_rebotes = df['Total de Rebotes'].mean().round(1)

            # Crear un nuevo DataFrame con las medias
            df_medias = pd.DataFrame({
                'Media Puntos': [media_puntos],
                'Media Asistencias': [media_asistencias],
                'Media Rebotes': [media_rebotes]
            })


            ##Nos quedamos con el nombre del jugador
            nombre=df['player.firstname'][0]+" "+df['player.lastname'][0]          
            ####Obtener las imagenes del API
            imagen=search_player_images(nombre)

            #Eliminamos las columnas que no nos interesan
            df = df.filter(regex="^(?!team\.)")
            df = df.filter(regex="^(?!player\.)")

            #Convertimos el dataframe a una tabla html        
            tabla=df.to_html(index=False)
            tabla_medias=df_medias.to_html(index=False)
 
            #Enviamos la tabla 
            return render(request,"nba_stats/players.html",context={'tabla':tabla,'tabla_medias':tabla_medias,'imagen':imagen,'grafica':graphic})
        except:
            raise "Error not found"
    return render(request,"nba_stats/players.html")

def player_stats(request):
    players_stats =get_player_stats()
    df_list = format_player_stats(players_stats)

    # Crear una lista de diccionarios donde cada diccionario representa un jugador y sus estadísticas
    players = []
    for df in df_list:
        player_dict = {key: val[0] for key, val in df.to_dict().items()}
        players.append(player_dict)

    # Pasar la lista de jugadores al contexto
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

def teams(request):
    teams=get_teams()
    return render(request, 'nba_stats/teams.html', {'teams': teams})





        


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
    
    standings_func = get_standings(2020)
   
    df = pd.DataFrame(standings_func,columns=['conference','name','rank'])

    east =df.query("conference == 'east'").sort_values('rank').set_index('rank').to_dict()
    west =df.query("conference == 'west'").sort_values('rank').set_index('rank').to_dict()
    context = {'eastern_teams': east,
               'western_teams': west,
               'standings': standings}
    return render(request, "nba_stats/ranking.html", context)

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