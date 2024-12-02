import requests
import pandas as pd
import json


#VER COMO METO LOS DATOS Y SOLUCIONAR EL PROBLEMA DE LOS ID
#




# Información de autenticación
RAPIDAPI_KEY = "9bfb2a642emsh24df258bdb0cbc1p1ce382jsn5c890cdbd9d3  "
RAPIDAPI_HOST = "api-nba-v1.p.rapidapi.com"

def convertir_minutos_a_num(minutos_str):
    data = {'min': [minutos_str]}
    df = pd.DataFrame(data)
    return df



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
        raise "Introduce un nombre valido"
    

def get_player_by_id(id,season=2022):
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



