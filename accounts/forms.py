from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput({"placeholder": "Username"}))
    name = forms.CharField(widget=forms.TextInput({"placeholder": "Name"}))
    email = forms.CharField(widget=forms.EmailInput({"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput({"placeholder": "Password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "Confirm password"})
    )

    class Meta:
        model = User
        fields = ("username", "name", "email", "password1", "password2")


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar", "cover_picture", "username", "name", "email", "bio")


class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = ("old_password", "password1", "password2")
