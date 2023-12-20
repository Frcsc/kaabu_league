import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from games.models import Game
from teams.models import Team

User = get_user_model()


class GameModelTestCase(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='Team1')
        self.team2 = Team.objects.create(name='Team2')

    def test_game_str_representation(self):
        game = Game.objects.create(
            team_1=self.team1, team_1_score=2, team_2=self.team2, team_2_score=1
        )
        expected_str = f"{self.team1.name} 2 - 1 {self.team2.name}"
        self.assertEqual(str(game), expected_str)

    def test_game_title_property(self):
        game = Game.objects.create(
            team_1=self.team1, team_1_score=3, team_2=self.team2, team_2_score=3
        )
        expected_title = f"{self.team1.name} 3 - 3 {self.team2.name}"
        self.assertEqual(game.game_title, expected_title)

    def test_team_manager_get_team(self):
        team = Team.objects.get_team(name='Team1')
        self.assertEqual(self.team1.name, team.name)

    def test_team_manager_get_existing_team(self):
        existing_team = Team.objects.create(name='ExistingTeam')
        team = Team.objects.get_team(name=existing_team.name)
        self.assertEqual(team, existing_team)

    def test_team_manager_get_non_existent_user(self):
        existing_team = Team.objects.create(name='ExistingTeam')
        incorrect_team_name = 'IncorrectTeam'
        team = Team.objects.get_team(name=incorrect_team_name)
        self.assertNotEqual(team, existing_team)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@gmail.com', password='testpassword'
        )
        self.team1 = Team.objects.create(name='Team1')
        self.team2 = Team.objects.create(name='Team2')
        self.game = Game.objects.create(
            team_1=self.team1, team_1_score=2, team_2=self.team2, team_2_score=1
        )

    def test_login_required_views(self):
        views = ['upload', 'games', 'add_game', 'edit_game', 'delete_game']
        for view_name in views:
            if view_name == 'edit_game' or view_name == 'delete_game':
                response = self.client.get(reverse(view_name, kwargs={'pk': 1}))
            else:
                response = self.client.get(reverse(view_name))
            self.assertRedirects(response, reverse('login'), status_code=302)

    def test_authenticated_user_can_access_views(self):
        views = ['upload', 'games', 'add_game', 'edit_game', 'delete_game']
        self.client.login(email='testuser@gmail.com', password='testpassword')
        for view_name in views:
            if view_name == 'edit_game' or view_name == 'delete_game':
                response = self.client.get(
                    reverse(view_name, kwargs={'pk': self.game.pk})
                )
            else:
                response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 200)

    def test_file_upload_view(self):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'csv', 'test.csv')
        self.client.login(email='testuser@gmail.com', password='testpassword')
        with open(file_path, 'rb') as file:
            response = self.client.post(reverse('upload'), {'file': file})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Game.objects.count(), 6)

    def test_add_game_view(self):
        self.client.login(email='testuser@gmail.com', password='testpassword')
        response = self.client.post(
            reverse('add_game'),
            {
                'team_1': self.team1.id,
                'team_1_score': 1,
                'team_2': self.team2.id,
                'team_2_score': 2,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Game.objects.count(), 2)

    def test_edit_game_view(self):
        self.client.login(email='testuser@gmail.com', password='testpassword')
        form_data = {
            'team_1': self.team1.id,
            'team_1_score': 32,
            'team_2': self.team2.id,
            'team_2_score': 20,
        }

        response = self.client.post(
            reverse('edit_game', args=[self.game.id]), form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Game.objects.get(id=self.game.id).team_1_score,
            form_data.get('team_1_score'),
        )

    def test_delete_game_view(self):
        self.client.login(email='testuser@gmail.com', password='testpassword')
        response = self.client.post(reverse('delete_game', args=[self.game.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Game.objects.count(), 0)
