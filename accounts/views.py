from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView


class SignupView(CreateView):
    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = "/"

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            email = form.cleaned_data["email"],
            password = form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return