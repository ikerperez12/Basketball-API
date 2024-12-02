import unittest
from apis import 
from unittest.mock import patch, Mock
import pandas as pd
import sys

# Aquí suponemos que tus funciones están en un módulo llamado "nba"
# Reemplaza "nba" con el nombre de tu módulo
sys.modules['nba'] = __import__(__name__)
from nba import get_standings, get_player_by_name, get_player_by_id, search_players_by_team_id

class TestNBAFunctions(unittest.TestCase):
    pass


@patch('nba.requests.get')
def test_get_standings(self, mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {'response': []}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    result = get_standings("2022", "east")

    mock_get.assert_called_with(
        "https://api-nba-v1.p.rapidapi.com/standings",
        headers={
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        },
        params={"league": "standard", "season": "2022", "conference": "east"}
    )
    self.assertIsInstance(result, pd.DataFrame)


@patch('nba.requests.get')
def test_get_player_by_name(self, mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {'response': []}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    result = get_player_by_name("LeBron")

    mock_get.assert_called_with(
        "https://api-nba-v1.p.rapidapi.com/players",
        headers={
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        },
        params={"search":"LeBron"}
    )
    self.assertIsInstance(result, list)



@patch('nba.requests.get')
def test_get_player_by_id(self, mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {'response': []}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    result = get_player_by_id(1)

    mock_get.assert_called_with(
        "https://api-nba-v1.p.rapidapi.com/players/statistics",
        headers={
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        },
        params={"id":1, "season":2022}
    )
    self.assertIsInstance(result, list)


@patch('nba.requests.get')
def test_search_players_by_team_id(self, mock_get):
    mock_resp = Mock()
    mock_resp.json.return_value = {'response': []}
    mock_resp.raise_for_status = Mock()
