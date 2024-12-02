import NBA_API
import pandas as pd
from typing import List


#Esta función elimina filas y columnas no necesarias, y reemplaza valores nulos por cero.
def clean_data(df):
    df.drop(["min"], axis=1, inplace=True) # Eliminar columna "min"
    df.dropna(subset=["games_played"], inplace=True) # Eliminar filas sin datos en "games_played"
    df.fillna(0, inplace=True) # Reemplazar valores nulos con cero
    return df


# Esta función ordena los datos del DataFrame en orden descendente según una columna dada.
def sort_data(df, column):
    df.sort_values(column, ascending=False, inplace=True)
    return df


# Recibe un DataFrame de pandas y una lista de nombres de columnas a convertir a tipo numérico.
# La función convierte las columnas seleccionadas a tipo numérico y retorna el DataFrame modificado.

def convert_to_numeric(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
    return df

# Recibe un DataFrame de pandas y el nombre de una columna que contiene valores porcentuales.
# La función convierte los valores porcentuales de la columna seleccionada a tipo numérico y los divide por 100,
# luego reemplaza la columna original con la columna modificada y retorna el DataFrame.

def convert_pct_to_float(df: pd.DataFrame, column: str) -> pd.DataFrame:
    df[column] = pd.to_numeric(df[column].str.strip('%'))/100
    return df

# Recibe un DataFrame de pandas y el nombre de una columna que contiene valores de tiempo.
# La función convierte los valores de tiempo de la columna seleccionada a segundos y los retorna como una Serie de pandas.

def convert_time_to_seconds(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_timedelta(df[column]).dt.total_seconds()

# Recibe un DataFrame de pandas y el nombre de una columna que contiene valores de fechas.
# La función convierte los valores de fecha de la columna seleccionada a tipo fecha y los retorna como una Serie de pandas.

def convert_date_to_datetime(df: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_datetime(df[column])



#CALCULOS 


# Recibe un DataFrame de pandas y una lista de nombres de columnas a las que se les calculará la media.
# La función calcula la media de las columnas seleccionadas y retorna una Serie de pandas.

def calculate_mean(df: pd.DataFrame, columns: List[str]) -> pd.Series:
    return df[columns].mean()

# Recibe un DataFrame de pandas y una lista de nombres de columnas a las que se les calculará la mediana.
# La función calcula la mediana de las columnas seleccionadas y retorna una Serie de pandas.

def calculate_median(df: pd.DataFrame, columns: List[str]) -> pd.Series:
    return df[columns].median()

# Recibe un DataFrame de pandas y una lista de nombres de columnas a las que se les calculará la desviación estándar.
# La función calcula la desviación estándar de las columnas seleccionadas y retorna una Serie de pandas.

def calculate_std(df: pd.DataFrame, columns: List[str]) -> pd.Series:
    return df[columns].std()




#CALCULOS INTERESANTES uso pandas


#Esta función calcula las estadísticas totales de una temporada dada.
def calc_season_stats(df):
    season_stats = df.sum(numeric_only=True)
    return season_stats


#Esta función calcula las estadísticas promedio por juego de una temporada dada.
def calc_per_game_stats(df):
    per_game_stats = df.mean(numeric_only=True)
    return per_game_stats


#Esta función calcula el índice de eficiencia de un jugador en una temporada dada.
def calc_player_efficiency_rating(df):
    points = df["points"]
    rebounds = df["totReb"]
    assists = df["assists"]
    steals = df["steals"]
    blocks = df["blocks"]
    turnovers = df["turnovers"]
    fouls = df["pFouls"]
    minutes_played = df["min"]
    efficiency_rating = (points + rebounds + assists + steals + blocks - turnovers - fouls) / minutes_played
    return efficiency_rating

#Esta función calcula el índice de eficiencia de un equipo en una temporada dada.
def calc_team_efficiency_rating(df):
    points = df["points"].sum()
    rebounds = df["totReb"].sum()
    assists = df["assists"].sum()
    steals = df["steals"].sum()
    blocks = df["blocks"].sum()
    turnovers = df["turnovers"].sum()
    fouls = df["pFouls"].sum()
    minutes_played = df["min"].sum()
    efficiency_rating = (points + rebounds + assists + steals + blocks - turnovers - fouls) / minutes_played
    return efficiency_rating
