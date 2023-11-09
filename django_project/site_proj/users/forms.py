from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-group",
                "style": "background-color: transparent; color: white;  border-radius: 5px;",
                "placeholder": "Enter your username",
            }
        ),
    )

    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-group",
                "style": "background-color: transparent; color: white;  border-radius: 5px;",
                "placeholder": "Enter your email",
            }
        ),
    )

    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-group",
                "type": "password",
                "style": "background-color: transparent; color: white;  border-radius: 5px;",
                "placeholder": "Enter your password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-group",
                "type": "password",
                "style": "background-color: transparent; color: white;  border-radius: 5px;",
                "placeholder": "Confirm your password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        """
        Returns the name if entered name is unique otherwise gives duplicate name error.
        """
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """
        Returns the email if entered email is unique otherwise gives duplicate_email error.
        """
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Duplicate email error")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-group",
                "style": "background-color: transparent; color: white;  border-radius: 5px;",
                "placeholder": "Enter your username",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "input-group",
                "type": "password",
                "style": "background-color: transparent; color: white;  border-radius: 5px;",
                "placeholder": "Enter your password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ["username", "email", "avatar"]

    def clean_username(self):
        """
        Returns the name if entered name is unique otherwise gives duplicate name error.
        """
        username = self.cleaned_data["username"]
        if (
            User.objects.filter(username=username).exists()
            and username != self.instance.user.username
        ):
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        """
        Returns the email if entered email is unique otherwise gives duplicate_email error.
        """
        email = self.cleaned_data["email"]
        if (
            User.objects.filter(email=email).exists()
            and email != self.instance.user.email
        ):
            raise forms.ValidationError("Duplicate email error")
        return email
