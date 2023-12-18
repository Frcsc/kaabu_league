from django.db import models

from tiger_lab_league.models import BaseModel


class TeamManager(models.Manager):
    def get_team(self, name):
        team, _ = self.get_or_create(name=name)
        return team


class Team(BaseModel):
    name = models.CharField(max_length=124, unique=True)

    def __str__(self):
        return self.name

    objects = TeamManager()
