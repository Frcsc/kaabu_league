import csv

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DeleteView, FormView, TemplateView, UpdateView

from games.forms import GameForm, UploadFileForm
from games.models import Game
from teams.models import Team
from users.permissions import LoginRequired


class FileUploadView(LoginRequired, TemplateView):
    template_name = 'upload_csv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UploadFileForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            self.handle_uploaded_file(csv_file)
            return redirect('games')
        return self.render_to_response({'form': form})

    def handle_uploaded_file(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:

            team_1_name = row['team_1 name']
            score_1 = int(row['team_1 score'])
            team_2_name = row['team_2 name']
            score_2 = int(row['team_2 score'])

            team_1 = Team.objects.get_team(name=team_1_name)
            team_2 = Team.objects.get_team(name=team_2_name)

            Game.objects.create(
                team_1=team_1,
                team_1_score=score_1,
                team_2=team_2,
                team_2_score=score_2,
            )


class GameListView(LoginRequired, TemplateView):
    template_name = 'game_list.html'

    def get_games(self, **kwargs):
        return Game.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = self.get_games()
        return context


class AddGameView(LoginRequired, FormView):
    template_name = 'add_game.html'
    form_class = GameForm
    success_url = '/games/'

    def form_valid(self, form):
        team_1 = form.cleaned_data.get('team_1')
        team_2 = form.cleaned_data.get('team_2')

        if team_1 == team_2:
            messages.add_message(
                self.request,
                messages.ERROR,
                "A team cannot play itself.",
            )
            return self.form_invalid(form)
        form.save()
        return super().form_valid(form)


class EditGameView(LoginRequired, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'edit_game.html'
    success_url = '/games/'

    def form_valid(self, form):
        team_1 = form.cleaned_data.get('team_1')
        team_2 = form.cleaned_data.get('team_2')

        if team_1 == team_2:
            messages.add_message(
                self.request,
                messages.ERROR,
                "A team cannot play itself.",
            )
            return self.form_invalid(form)
        return super().form_valid(form)


class DeleteGameView(LoginRequired, DeleteView):
    model = Game
    success_url = '/games/'
    template_name = 'delete_game.html'
