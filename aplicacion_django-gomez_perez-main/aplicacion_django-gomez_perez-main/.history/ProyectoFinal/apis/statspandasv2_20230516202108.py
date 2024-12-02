import pandas as pd
from NBA_API import *
import NBA_API

# Obtener los datos del jugador desde la API
player_stats = NBA_API.get_player_stats(id="236", season="2020")





def format_player_stats(player_stats):
    df_list = []
    for player in player_stats:
        # Aplanar los datos anidados
        player_info = player.pop('player')
        team_info = player.pop('team')
        game_info = player.pop('game')

        player.update({
            'player_id': player_info['id'],
            'player_firstname': player_info['firstname'],
            'player_lastname': player_info['lastname'],
            'team_id': team_info['id'],
            'team_name': team_info['name'],
            'team_nickname': team_info['nickname'],
            'team_code': team_info['code'],
            'team_logo': team_info['logo'],
            'game_id': game_info['id'],
        })

        df = pd.DataFrame(player, index=[0])
        df_list.append(df)
    return df_list



# Formatea los datos y crea los DataFrames
df_list = format_player_stats(player_stats['response'])




def print_player_stats(df_list, num_games):
    for df in df_list[:num_games]:
        print(df.to_string(index=False))
        print("\n")

# Llamada a la función para imprimir las estadísticas de los primeros 4 partidos
print_player_stats(df_list, 2)




# Ahora puedes usar pandas para operar en la lista de DataFrames.
# Por ejemplo, calcular la media de puntos:
points_list = [df['points'].mean() for df in df_list]
print(points_list)