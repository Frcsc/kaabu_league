from django.urls import path

from rankings.views import HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="homepage"),
]
