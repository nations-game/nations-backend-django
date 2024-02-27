from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Form
from ..models import User, Nation

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class NationCreateForm(forms.ModelForm):
    class Meta:
        model = Nation
        fields = [
            "name", "system"
        ]
