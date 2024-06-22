from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person


class SignUpForm(UserCreationForm):
    password = forms.PasswordInput(max_length=255, required=True)

    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = Person
        fields = [
            "email",
            "password",
        ]
