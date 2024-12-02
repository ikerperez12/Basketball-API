from django.test import TestCase
from .models import Team,Player,Standing
from NBA_API import get_player_stats

# Create your tests here.

class PlayerStatsTestCase(TestCase):
    def test_get_player_stats(self):
        player_id = "123456"
        season = "2020-2021"
        stats = get_player_stats(player_id, season)
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, dict)


class TeamTestCase(TestCase):

    def setUp(self):
        Team.objects.create(
            name="Los Angeles Lakers", abbreviation="LAL", city="Los Angeles",
            conference="West", division="Pacific"
        )

    def test_team_attributes(self):
        lakers = Team.objects.get(name="Los Angeles Lakers")
        self.assertEqual(lakers.name, "Los Angeles Lakers")
        self.assertEqual(lakers.abbreviation, "LAL")
        self.assertEqual(lakers.city, "Los Angeles")
        self.assertEqual(lakers.conference, "West")
        self.assertEqual(lakers.division, "Pacific")

class StandingsTestCase(TestCase):
    def setUp(self):
        Team.objects.create(name="Los Angeles Lakers", conference="West", wins=52, losses=20, win_pct=0.722, games_back=0)
        Team.objects.create(name="Miami Heat", conference="East", wins=44, losses=29, win_pct=0.603, games_back=0)
        Team.objects.create(name="Houston Rockets", conference="West", wins=44, losses=28, win_pct=0.611, games_back=0)
        Team.objects.create(name="Toronto Raptors", conference="East", wins=46, losses=26, win_pct=0.639, games_back=0)
        
    def test_standings_sort(self):
        west_standings = Standing(conference="West")
        west_teams = Team.objects.filter(conference="West")
        west_standings.sort_by_conference_position(west_teams)
        west_standings_positions = [team.position for team in west_standings.teams]
        self.assertEqual(west_standings_positions, [1, 2])
        
        east_standings = Standing(conference="East")
        east_teams = Team.objects.filter(conference="East")
        east_standings.sort_by_conference_position(east_teams)
        east_standings_positions = [team.position for team in east_standings.teams]
        self.assertEqual(east_standings_positions, [1, 2])