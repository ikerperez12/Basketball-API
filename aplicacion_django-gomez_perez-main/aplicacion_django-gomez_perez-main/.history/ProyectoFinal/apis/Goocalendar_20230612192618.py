import requests
from NBA_API import *
import json
from Goocalendar import *
from google.oauth2 import service_account
from googleapiclient.discovery import build

class Goocalendar:
    def __init__(self, credentials_file_path):
        self.credentials_file_path = credentials_file_path

    def process_games(self, games):
        # Configuración de autenticación de Google Calendar API
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file_path, scopes=['https://www.googleapis.com/auth/calendar']
        )
        service = build('calendar', 'v3', credentials=creds)

        calendar = {
            'summary': 'Calendario de partidos de la NBA',
            'description': 'Calendario generado automáticamente con los partidos de la NBA',
            'timeZone': 'UTC'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()

        calendar_id = created_calendar['id']

        for game in games:
            # Obtener información de los equipos
            visitor_team = game['teams']['visitors']
            home_team = game['teams']['home']

            # Obtener información de los puntajes
            visitor_scores = game['scores']['visitors']
            home_scores = game['scores']['home']

            # Obtener información de la transmisión
            if 'broadcast' in game:
                broadcast_info = game['broadcast']['network']
            else:
                broadcast_info = 'Información de transmisión no disponible'

            # Crear eventos en Google Calendar para cada juego
            event = {
                'summary': f"{visitor_team['name']} vs {home_team['name']}",
                'description': f"Juego de la NBA: {visitor_team['name']} vs {home_team['name']}\n"
                               f"Fecha y hora: {game['date']['start']}\n"
                               f"Estadio: {game['arena']['name']}\n"
                               f"TV: {broadcast_info}",
                'start': {
                    'dateTime': game['date']['start'],
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': game['date']['start'],
                    'timeZone': 'UTC',
                },
                'colorId': self.get_color_id(visitor_team['id']),
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 60},  # Recordatorio de 1 hora antes del juego
                    ],
                },
            }

            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            calendar_link = f"https://calendar.google.com/calendar/r?cid={calendar_id}"
            print(f"Enlace para importar el calendario: {calendar_link}")
            print(f"Evento creado: {event['htmlLink']}")


    def get_color_id(self, team_id):
        # Asigna colores personalizados según el equipo visitante
        # Puedes personalizar esta lógica para asignar los colores que desees
        if team_id == 1:
            return '11'  # Color rojo
        elif team_id == 2:
            return '8'  # Color azul
        else:
            return '9'  # Color verde


games = get_games_by_team_and_season(team_id, season)
credentials_file_path = credentials_file_path = "ProyectoFinal\credenciales\credenciales.json"  # Ruta al archivo JSON de credenciales actualizado
goocalendar = Goocalendar(credentials_file_path)
goocalendar.process_games(games)
