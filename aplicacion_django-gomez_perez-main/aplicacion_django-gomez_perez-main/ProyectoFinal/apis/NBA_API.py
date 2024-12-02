import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from apis.Goocalendar import *
from apis.BINGAPI import search_player_images
from PIL import Image,ImageOps
import numpy as np

# Información de autenticación
RAPIDAPI_KEY = "8d34ad3e40mshf83c619f5fffa69p1a39bbjsnbcf4cb9e6772"
RAPIDAPI_HOST = "api-nba-v1.p.rapidapi.com"

def convertir_minutos_a_num(minutos_str):
    data = {'min': [minutos_str]}
    df = pd.DataFrame(data)
    return df


def filtrar_nombre(nombre_completo):
    #Obtenemos el apellido
    nombre_separado=nombre_completo.split()
    if len(nombre_separado)==1:
        return nombre_separado[0]
    elif len(nombre_separado)==2:
        return nombre_separado[1]
    else:
        return ''
    
#Si solamente existe un jugador con ese apellido, lo mostramos directamente, sino, mostramos una lista con los jugadores y escogemos el que nosotros queramos.
def obtener_jugadores(nombre):
    apellido_de_busqueda=filtrar_nombre(nombre)
    #obtener los players aqui
    players=get_player_by_name(apellido_de_busqueda)
    #players=[{'id': 123, 'firstname': 'Seth', 'lastname': 'Curry', 'birth': {'date': '1990-08-23', 'country': 'USA'}, 'nba': {'start': 2013, 'pro': 7}, 'height': {'feets': '6', 'inches': '2', 'meters': '1.88'}, 'weight': {'pounds': '185', 'kilograms': '83.9'}, 'college': 'Duke', 'affiliation': 'Duke/USA', 'leagues': {'standard': {'jersey': 30, 'active': True, 'pos': 'G'}}}, {'id': 124, 'firstname': 'Stephen', 'lastname': 'Curry', 'birth': {'date': '1988-03-14', 'country': 'USA'}, 'nba': {'start': 2009, 'pro': 12}, 'height': {'feets': '6', 'inches': '2', 'meters': '1.88'}, 'weight': {'pounds': '185', 'kilograms': '83.9'}, 'college': 'Davidson', 'affiliation': 'Davidson/USA', 'leagues': {'standard': {'jersey': 30, 'active': True, 'pos': 'G'}}}]
    #players=[]
    if len(players)!=0:
        return players
    else:
        return []
##Funcion que convierte los tiempos de juego a enteros para 
##poder aplicar funciones de estadísticas avanzadas
def convertir_tiempo_a_entero(tiempo_str):
    if ':' in tiempo_str:
        minutos, segundos = map(int, tiempo_str.split(':'))
        tiempo_entero = minutos + segundos / 60
    else:
        tiempo_entero=int(tiempo_str)   
    return tiempo_entero


def formatear_jugador(player):
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
            nombre=df['player.firstname'][0]+" "+df['player.lastname'][0]+" "+df['team.name'][0]          
            ####Obtener las imagenes del API
            imagen=search_player_images(nombre)

            #Eliminamos las columnas que no nos interesan
            df = df.filter(regex="^(?!team\.)")
            df = df.filter(regex="^(?!player\.)")

            #Convertimos el dataframe a una tabla html        
            tabla=df.to_html(index=False)
            tabla_medias=df_medias.to_html(index=False)
            context={'tabla':tabla,'tabla_medias':tabla_medias,'imagen':imagen,'grafica':graphic}
            return context




#Recibe dos parámetros opcionales, id y season, que corresponden al id del jugador y la temporada
#Si no se encontraron estadísticas, la función retorna None y muestra un mensaje. De lo contrario,
# la función crea un DataFrame de pandas a partir de la respuesta JSON y lo retorna.
#USO EN STATSPANDAS.PY


def get_player_stats(id, season):
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    querystring = {"id": id, "season": season}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        # Guardar los datos en un archivo JSON para su posterior análisis
        with open('player_stats.json', 'w') as f:
            json.dump(data, f)

        return data
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None



# Recibe dos parámetros opcionales: team (id del equipo) y season (temporada).
# Si no se encontraron estadísticas, la función retorna None y muestra un mensaje. De lo contrario,
# la función crea un DataFrame de pandas a partir de la respuesta JSON y lo retorna.
# USO EN STATSPANDAS.PY

def get_team_stats(team=None, season=None):
    try:
        url = "https://api-nba-v1.p.rapidapi.com/teams/statistics"
        querystring = {}
        if team:
            querystring["team"] = str(team)
        if season:
            querystring["season"] = str(season)
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        json_data = response.json()
        if json_data.get("message") == "The resource you are looking for is not available.":
            raise ValueError("No se encontraron estadísticas para el equipo y temporada seleccionados.")
        df = pd.DataFrame(json_data["api"]["statistics"])
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener estadísticas del equipo: {str(e)}")
        return None
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None







# Recibe un parámetro opcional, lastname, que corresponde al apellido del jugador a buscar.
# Si no se encontraron jugadores, la función retorna None y muestra un mensaje.
# De lo contrario, la función crea una lista de diccionarios con los datos de los jugadores y la retorna.

def search_players(lastname):
    url = "https://api-nba-v1.p.rapidapi.com/players"
    querystring = {"search": lastname}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        players = response.json().get("api", {}).get("players", [])
        return players
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar jugadores: {str(e)}")
        return None




# Recibe un parámetro, season, que corresponde a la temporada de la que se quieren obtener los juegos.
# Si la solicitud es exitosa, procesa los juegos obtenidos utilizando la función process_games en el archivo Goocalendar.py.
def get_games_per_season(season):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {"season": season}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        games = response.json()["api"]["games"]
        Goocalendar.process_games(games)  # Pasar los juegos a la función en Goocalendar.py
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los juegos: {str(e)}")






##FUNCIONES COMPLETAMENTE TERMINADAS

###Imprime una lista de todos los equipos de los cuales tenemos información
def get_teams():
    url = "https://api-nba-v1.p.rapidapi.com/teams"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        teams = json_data.get('response', [])
        return teams
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los equipos: {str(e)}")
        return None



# Recibe un parámetro opcional, query, que corresponde al nombre del equipo a buscar.
# Si no se encontraron equipos, la función retorna None y muestra un mensaje. De lo contrario,
# la función crea una lista de diccionarios con los datos de los equipos y la retorna.
# Cada diccionario contiene los siguientes datos:id, name, abbreviation, city, conference y division.

def search_team(query):
    url = "https://api-nba-v1.p.rapidapi.com/teams"
    querystring = {"search": query}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        json_data = response.json()
        busqueda=json_data.get('response',[])
        return busqueda
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar equipos: {str(e)}")
        return None
       

# Recibe dos parámetros  season y/o conference, que corresponden a la temporada y conferencia de la que se quieren obtener los juegos.
# La función crea un DataFrame de pandas a partir de la respuesta JSON y lo retorna.
#USO EN STANDINGSPANDAS.PY
def get_standings(season, conference=None):
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"league": "standard", "season": season}
    if conference:
        querystring["conference"] = conference

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        json_data = response.json()
        ranking=json_data.get('response',[])
        df=pd.json_normalize(ranking)
        return df
    except Exception as err:
        print(f"An error occurred: {err}")
    

def get_player_by_name(player):
        # with open('/home/ruben/Documentos/UDC/Programacion Integrativa/ProyectoFinal/lista_jugadores.json') as f:
        #         data = json.load(f)
        # data=data.get('response')
        # df=pd.json_normalize(data,sep="-")
        # return data   
    url = "https://api-nba-v1.p.rapidapi.com/players"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    if player:
            querystring={"search":player}
    

    try:
        response = requests.get(url, headers=headers,params=querystring)
        response.raise_for_status()
        json_data = response.json()
        players = json_data.get('response', [])
        return players
    except:
        return []
    

def get_player_stadistics_by_id(id,season=2022):
    # with open('/home/ruben/Documentos/UDC/Programacion Integrativa/ProyectoFinal/player1_stats.json') as f:
    #     data = json.load(f)
    # data=data.get('response')
    # df=pd.json_normalize(data,sep="-")
    # return data   
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    if id:
            querystring = {"id":id,"season":season}


    try:
        response = requests.get(url, headers=headers,params=querystring)
        response.raise_for_status()
        json_data = response.json()
        players = json_data.get('response', [])
        return players
    except:
        raise "Introduce un id valido"    


def search_players_by_team_id(team,season=2022):
    url = "https://api-nba-v1.p.rapidapi.com/players"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    if id:
            querystring = {"team":team,"season":season}


    try:
        response = requests.get(url, headers=headers,params=querystring)
        response.raise_for_status()
        json_data = response.json()
        players = json_data.get('response', [])
        return players
    except:
        raise "Introduce un id valido"   



def get_games_by_team_and_season(team_id, season):
        url = "https://api-nba-v1.p.rapidapi.com/games/"

        querystring = {"season": str(season), "team": str(team_id)}

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }

        response = requests.get(url, headers=headers, params=querystring)
        games = response.json().get("response")

        return games

