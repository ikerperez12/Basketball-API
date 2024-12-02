import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import NBA_API


# Crear gráfico de barras apiladas por victorias y derrotas
def create_stacked_bar_chart(df_standings):
    """
    Crea un gráfico de barras apiladas que muestra las victorias y derrotas por equipo.

    Args:
        df_standings (DataFrame): DataFrame de clasificación.

    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x="teamName", y="win", data=df_standings, color="green", label="Victorias")
    sns.barplot(x="teamName", y="loss", data=df_standings, color="red", label="Derrotas")
    plt.xticks(rotation=90)
    plt.title("Victorias y Derrotas por equipo")
    plt.xlabel("Equipo")
    plt.ylabel("Cantidad")
    plt.legend()
    plt.show()


# Crear gráfico de pastel por conferencia
def create_pie_chart_by_conference(df_standings):
    """
    Crea un gráfico de pastel que muestra la distribución de equipos por conferencia.

    Args:
        df_standings (DataFrame): DataFrame de clasificación.

    """
    conference_counts = df_standings["conference"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(conference_counts, labels=conference_counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Distribución por conferencia")
    plt.axis("equal")
    plt.show()


# Filtrar clasificación por conferencia
def filter_standings_by_conference(df_standings, conference):
    """
    Filtra la clasificación por conferencia.

    Args:
        df_standings (DataFrame): DataFrame de clasificación.
        conference (str): Conferencia a filtrar.

    Returns:
        DataFrame: DataFrame filtrado por conferencia.

    """
    filtered_standings = df_standings[df_standings["conference"] == conference]
    return filtered_standings


# Crear gráfico de línea para seguir el rendimiento de un equipo a lo largo de la temporada
def create_team_performance_chart(df_standings, team_name):
    """
    Crea un gráfico de línea que muestra el rendimiento de un equipo a lo largo de la temporada.

    Args:
        df_standings (DataFrame): DataFrame de clasificación.
        team_name (str): Nombre del equipo.

    """
    team_data = df_standings[df_standings["teamName"] == team_name]
    plt.figure(figsize=(10, 6))
    plt.plot(team_data["winPercentage"], marker="o")
    plt.xticks(range(len(team_data)), team_data["teamName"], rotation=90)
    plt.title(f"Rendimiento del equipo {team_name}")
    plt.xlabel("Partido")
    plt.ylabel("Porcentaje de victorias")
    plt.show()


def show_standins():
    pass
def main():
    # Obtener los datos de clasificación utilizando la función get_standings
    df_standings = NBA_API.get_standings(season="2021")

    # Crear visualizaciones
    create_stacked_bar_chart(df_standings)
    create_pie_chart_by_conference(df_standings)

    # Filtrar por conferencia (ejemplo: "East")
    filtered_standings = filter_standings_by_conference(df_standings, "East")
    print(filtered_standings)

    # Rendimiento del equipo (ejemplo: "Los Angeles Lakers")
    create_team_performance_chart(df_standings, "Los Angeles Lakers")

if __name__ == "__main__":
    main()