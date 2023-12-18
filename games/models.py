from django.db import models

from tiger_lab_league.models import BaseModel


class Game(BaseModel):
    team_1 = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='home_games'
    )
    team_1_score = models.IntegerField()
    team_2 = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='away_games'
    )
    team_2_score = models.IntegerField()

    def __str__(self):
        return f"{self.team_1.name} {self.team_1_score} - {self.team_2_score} {self.team_2.name}"
