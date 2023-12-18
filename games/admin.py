from django.contrib import admin

from games.models import Game


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_1', 'team_2', 'team_1_score', 'team_2_score']


admin.site.register(Game, TeamAdmin)
