from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class ContainerForm(forms.ModelForm):
    """Form for creating and updating Containers"""

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all())

    class Meta:
        model = Container
        fields = "__all__"


class LogForm(forms.ModelForm):
    """Form for creating and updating LOGS"""

    class Meta:
        model = Log
        fields = "__all__"


class FinishedLogForm(forms.ModelForm):
    """
    Form for creating or updating a FinishedLog instance.
    """
    class Meta:
        model = FinishedLog
        fields = "__all__"


class SaleOrderlineForm(forms.ModelForm):
    """
       Form for creating or updating a SaleOrderline instance.
    """
    class Meta:
        model = SaleOrderline
        fields = "__all__"


class SignupForm(UserCreationForm):
    """Form for user signup."""

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    """Form for user login."""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
