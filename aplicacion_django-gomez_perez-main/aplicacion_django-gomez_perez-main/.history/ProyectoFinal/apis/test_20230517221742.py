import unittest

from unittest.mock import patch, Mock
import pandas as pd
import sys

# Aquí suponemos que tus funciones están en un módulo llamado "nba"
# Reemplaza "nba" con el nombre de tu módulo
sys.modules['nba'] = __import__(__name__)
from NBA_API import get_standings, get_player_by_name, get_player_by_id, search_players_by_team_id

class TestNBAFunctions(unittest.TestCase):

    @patch('nba.requests.get')
    def test_get_standings(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {'response': []}
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        result = get_standings("2022", "east")

        if mock_get.called:
            print("get_standings: La función requests.get fue llamada correctamente.")
        else:
            print("get_standings: La función requests.get NO fue llamada correctamente.")

        if isinstance(result, pd.DataFrame):
            print("get_standings: La función retorna un DataFrame como se esperaba.")
        else:
            print("get_standings: La función NO retorna un DataFrame como se esperaba.")

    @patch('nba.requests.get')
    def test_get_player_by_name(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {'response': []}
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        result = get_player_by_name("LeBron")

        if mock_get.called:
            print("get_player_by_name: La función requests.get fue llamada correctamente.")
        else:
            print("get_player_by_name: La función requests.get NO fue llamada correctamente.")

        if isinstance(result, list):
            print("get_player_by_name: La función retorna una lista como se esperaba.")
        else:
            print("get_player_by_name: La función NO retorna una lista como se esperaba.")

    @patch('nba.requests.get')
    def test_get_player_by_id(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {'response': []}
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        result = get_player_by_id(1)

        if mock_get.called:
            print("get_player_by_id: La función requests.get fue llamada correctamente.")
        else:
            print("get_player_by_id: La función requests.get NO fue llamada correctamente.")

        if isinstance(result, list):
            print("get_player_by_id: La función retorna una lista como se esperaba.")
        else:
            print("get_player_by_id: La función NO retorna una lista como se esperaba.")

    @patch('nba.requests.get')
    def test_search_players_by_team_id(self, mock_get):
        mock_resp = Mock()
        mock_resp.json.return_value = {'response': []}
        mock_resp.raise_for_status = Mock()
        mock_get.return_value = mock_resp

        result = search_players_by_team_id(1)

        if mock_get.called:
            print("search_players_by_team_id: La función requests.get fue llamada correctamente.")
        else:
            print("search_players_by_team_id: La función requests.get NO fue llamada correctamente.")

        if isinstance(result, list):
            print("search_players_by_team_id: La función retorna una lista como se esperaba.")
        else:
            print("search_players_by_team_id: La función NO retorna una lista como se esperaba.")
