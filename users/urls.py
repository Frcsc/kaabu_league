from django.urls import path

from users.views import LoginView, Logout, RegistrationView

urlpatterns = [
    path('register', RegistrationView.as_view(), name='registration'),
    path("login", LoginView.as_view(), name="login"),
    path("logout", Logout.as_view(), name="logout"),
]
