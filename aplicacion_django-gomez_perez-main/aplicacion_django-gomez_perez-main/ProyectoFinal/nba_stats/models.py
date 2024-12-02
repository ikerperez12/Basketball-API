from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=255)
    team = models.CharField(max_length=100)
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.IntegerField(default=0)
    blocks = models.IntegerField(default=0)
    turnovers = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    conference = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    minutes_played = models.IntegerField(default=0)
    efficiency_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name
    

class Standing(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    season = models.CharField(max_length=4)
    conference = models.CharField(max_length=4)
    wins = models.IntegerField()
    losses = models.IntegerField()
    win_percentage = models.DecimalField(max_digits=4, decimal_places=3)
    games_behind = models.DecimalField(max_digits=4, decimal_places=1)
    conference_rank = models.IntegerField()

    class Meta:
        ordering = ['conference_rank']