from django.urls import path

from games.views import (
    AddGameView,
    DeleteGameView,
    EditGameView,
    FileUploadView,
    GameListView,
)

urlpatterns = [
    path("upload", FileUploadView.as_view(), name="upload"),
    path("", GameListView.as_view(), name="games"),
    path('add/', AddGameView.as_view(), name='add_game'),
    path('delete/<int:pk>/', DeleteGameView.as_view(), name='delete_game'),
    path('edit/<int:pk>/', EditGameView.as_view(), name='edit_game'),
]
