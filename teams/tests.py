from django.test import TestCase

from teams.models import Team


class TeamModelTestCase(TestCase):
    def test_team_str_representation(self):
        team_name = 'TeamA'
        team = Team.objects.create(name=team_name)
        self.assertEqual(str(team), team_name)

    def test_wrong_team_str_representation(self):
        team_name = 'TeamA'
        team = Team.objects.create(name=team_name)
        self.assertNotEqual(str(team), 'IncorrectName')
