import unittest

import unittest
from unittest.mock import patch, Mock
import pandas as pd
import sys

# Aquí suponemos que tus funciones están en un módulo llamado "nba"
# Reemplaza "nba" con el nombre de tu módulo
sys.modules['nba'] = __import__(__name__)
from nba import get_standings, get_player_by_name, get_player_by_id, search_players_by_team_id

class TestNBAFunctions(unittest.TestCase):
    pass
