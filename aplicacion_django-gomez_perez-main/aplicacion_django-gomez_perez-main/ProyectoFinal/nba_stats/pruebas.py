
import base64
from io import BytesIO
import pandas as pd
import json
import os
import requests
from PIL import Image,ImageOps
import matplotlib.pyplot as plt
lista_dict_estadisticas=[]

def get_player_by_name(player):
        with open('/home/ruben/Documentos/UDC/Programacion Integrativa/ProyectoFinal/lista_jugadores.json') as f:
                data = json.load(f)
        data=data.get('response')
        df=pd.json_normalize(data,sep="-")
        return data

def get_player_by_id(id):
        with open('/home/ruben/Documentos/UDC/Programacion Integrativa/ProyectoFinal/player1_stats.json') as f:
                data = json.load(f)
        data=data.get('response')
        df=pd.json_normalize(data,sep="-")
        return data

def get_player_by_id2(id):
        with open('/home/ruben/Documentos/UDC/Programacion Integrativa/ProyectoFinal/player2_stats.json') as f:
                data = json.load(f)
        data=data.get('response')
        df=pd.json_normalize(data,sep="-")
        return data


BING_API_KEY = "79f1e8649a7a44aeb3b962e39d6ccf45"

# Función para buscar imágenes de jugadores en Bing
def search_player_images(player_name):
    url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {
        "Ocp-Apim-Subscription-Key": BING_API_KEY
    }
    params = {
        "q": player_name + " NBA player",
        "count": 1  # Obtener solo una imagen
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        json_data = response.json()
        if "value" in json_data and len(json_data["value"]) > 0:
            image_url = json_data["value"][0]["thumbnailUrl"]
            return image_url
        else:
            print("No se encontraron imágenes para el jugador.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar imágenes: {str(e)}")
        return None


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
                 'medias':medias
                 }

    añadir_elemento_lista_jugadores(diccionario)

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

def generar_grafica():
      global lista_dict_estadisticas
      if(len(lista_dict_estadisticas)==2):
        df1=pd.read_html(lista_dict_estadisticas[0]['estadisticas'])
        df2=pd.read_html(lista_dict_estadisticas[1]['estadisticas'])
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


def añadir_elemento_lista_jugadores(diccionario):
    global lista_dict_estadisticas
    if len(lista_dict_estadisticas)==2:
        del lista_dict_estadisticas[0]
        lista_dict_estadisticas.insert(1,diccionario)
    else:
         lista_dict_estadisticas.append(diccionario)    
            


_json=get_player_by_id("absc")
_json2=get_player_by_id2("absc")
obtener_estadisticas_jugador(_json)
obtener_estadisticas_jugador(_json2)
# obtener_estadisticas_jugador(_json2)
# obtener_estadisticas_jugador(_json)
# obtener_estadisticas_jugador(_json2)
# print(len(lista_dict_estadisticas))
print(lista_dict_estadisticas[0]['estadisticas_partido'][0:3])

# print(lista_dict_estadisticas[1]['nombre'])


