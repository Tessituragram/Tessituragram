from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import PendingSignup


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        pending = PendingSignup(
            username=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password_hash=make_password(self.cleaned_data["password1"]),
        )
        if commit:
            pending.save()
        return pending


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class EmailChangeForm(forms.Form):
    new_email = forms.EmailField(label="New email")

    def clean_new_email(self):
        email = self.cleaned_data["new_email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email