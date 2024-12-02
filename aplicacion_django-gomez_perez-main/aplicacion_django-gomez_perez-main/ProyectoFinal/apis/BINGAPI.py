
import requests

# Claves de la API de Bing
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






