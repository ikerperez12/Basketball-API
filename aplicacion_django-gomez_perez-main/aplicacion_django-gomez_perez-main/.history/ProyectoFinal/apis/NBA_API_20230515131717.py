import requests
import pandas as pd



#VER COMO METO LOS DATOS Y SOLUCIONAR EL PROBLEMA DE LOS ID
#




# Información de autenticación
RAPIDAPI_KEY = "8d34ad3e40mshf83c619f5fffa69p1a39bbjsnbcf4cb9e6772"
RAPIDAPI_HOST = "api-nba-v1.p.rapidapi.com"



#Recibe dos parámetros opcionales, id y season, que corresponden al id del jugador y la temporada
#Si no se encontraron estadísticas, la función retorna None y muestra un mensaje. De lo contrario,
# la función crea un DataFrame de pandas a partir de la respuesta JSON y lo retorna.
#USO EN STATSPANDAS.PY

def get_player_stats(id=None, season=None):
    try:
        url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
        querystring = {}
        if id:
            querystring["id"] = str(id)
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
            raise ValueError("No se encontraron estadísticas para el jugador y temporada seleccionados.")
        df = pd.DataFrame(json_data["api"]["statistics"])
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener estadísticas del jugador: {str(e)}")
        return None
    except ValueError as e:
        print(f"Error: {str(e)}")
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





# Recibe un parámetro opcional, query, que corresponde al nombre del equipo a buscar.
# Si no se encontraron equipos, la función retorna None y muestra un mensaje. De lo contrario,
# la función crea una lista de diccionarios con los datos de los equipos y la retorna.
# Cada diccionario contiene los siguientes datos:id, name, abbreviation, city, conference y division.

def search_teams(query):
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
        busquedaequipos = []
        for teamsearch in busqueda:
            team_dict = {
                "id": teamsearch.get("id"),
                "name": teamsearch.get("nickname"),
                "nickname": teamsearch.get("code"),
                "city": teamsearch.get("city"),
                "logo": teamsearch.get("logo")
            }
            busquedaequipos.append(team_dict)
        return busquedaequipos



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
        ranking_final = []
        for team in ranking:
            team_dict = {
                "id": team.get("id"),
                "name": team.get("name"),
                "nickname": team.get("nickname"),
                "city": team.get("city")
            }
            teams_final.append(team_dict)
        return teams_final
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los equipos: {str(e)}")
        return None


# OBTENER EQUIPOS 2345

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
        teams_final = []
        for team in teams:
            team_dict = {
                "id": team.get("team").get("id"),
                "name": team.get("team").get("name"),
                "rank": team.get("conference").get("rank"),
                "league":team.get("league"),
            }
            teams_final.append(team_dict)
        return teams_final
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los equipos: {str(e)}")
        return None
