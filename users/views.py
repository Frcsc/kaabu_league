from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render
from django.views import View

from users.forms import LoginForm, RegistrationForm
from users.models import UserProfile
from users.permissions import LoginRequired

User = get_user_model()


class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('games')
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('new_email')
        password = request.POST.get('new_password')

        if User.objects.filter(email=email).exists():
            messages.add_message(
                request,
                messages.ERROR,
                "email belongs to a diffrent user.",
            )
            return redirect('login')
        user = User.objects.create_user(email, password)
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('games')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('games')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('games')
            else:
                messages.add_message(request, messages.INFO, "wrong email or password.")
        return redirect('login')


class Logout(LoginRequired, View):
    def post(self, request):
        logout(request)
        return redirect("login")
