from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from . import models


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        fields = ('birth_date', 'contact_number', 'description', 'gender')


class UpdateUserBaseForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password')
