from django.db.models import Case, F, IntegerField, Sum, Value, When
from django.views.generic import TemplateView

from teams.models import Team


class HomePage(TemplateView):
    template_name = 'home.html'

    def get_team_rankings(self):
        teams = Team.objects.annotate(
            total_points=Sum(
                Case(
                    When(
                        home_games__team_1_score__gt=F('home_games__team_2_score'),
                        then=Value(3),
                    ),
                    When(
                        home_games__team_1_score=F('home_games__team_2_score'),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                + Case(
                    When(
                        away_games__team_2_score__gt=F('away_games__team_1_score'),
                        then=Value(3),
                    ),
                    When(
                        away_games__team_2_score=F('away_games__team_1_score'),
                        then=Value(1),
                    ),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
        ).order_by('-total_points', 'name')

        return teams

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = self.get_team_rankings()
        return context
