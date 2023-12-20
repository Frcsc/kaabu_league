from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as _


class LoginRequired(LoginRequiredMixin):

    login_url = _('login')
    redirect_field_name = None

    def handle_no_permission(self):
        messages.error(self.request, "please sign in.")
        return super().handle_no_permission()
