from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, App


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ["apk_file"]
