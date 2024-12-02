from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuración de autenticación de Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '/path/to/service/account/key.json'  # reemplazar con la ruta del archivo de clave de servicio de Google
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def process_games(games):
    # Crear eventos en Google Calendar para cada juego
    service = build('calendar', 'v3', credentials=creds)
    calendar_id = 'primary'  # reemplazar con el ID del calendario deseado

    for game in games:
        # Aquí puedes tratar los datos de cada juego y crear eventos en Google Calendar según tus necesidades
        # Por ejemplo, puedes obtener la fecha y hora del juego, los equipos involucrados, etc.

        # Ejemplo básico de creación de un evento en Google Calendar
        event = {
            'summary': f"{game['vTeam']['fullName']} vs {game['hTeam']['fullName']}",
            'description': f"Juego de la NBA: {game['vTeam']['fullName']} vs {game['hTeam']['fullName']}\n"
                           f"Fecha y hora: {game['startTimeUTC']}\n"
                           f"Estadio: {game['arena']['name']}\n"
                           f"TV: {game['watch']['broadcast']['national']}",
            'start': {
                'dateTime': game['startTimeUTC'],
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': game['endTimeUTC'],
                'timeZone': 'UTC',
            },
            'colorId': getColorId(game['vTeam']['teamId']),  # Asigna un color personalizado según el equipo visitante
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},  # Recordatorio de 1 hora antes del juego
                ],
            },
        }

        try:
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Evento creado: {event['htmlLink']}")
        except Exception as e:
            print(f"Error al crear el evento: {str(e)}")



#IMPLEMENTACIONES EXTRA:

# 1:Se agregó la descripción detallada del juego al campo 'description' del evento en Google Calendar.
# 2:Se agregó un color personalizado al evento en Google Calendar según el equipo visitante.
# 3:Se agregó un recordatorio de 1 hora antes del juego.