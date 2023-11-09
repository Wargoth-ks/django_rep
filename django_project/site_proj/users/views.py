from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile


def sign_up(request):
    if request.user.is_authenticated:
        return redirect(to="web_app:main")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account successfully created for {user}")
            return redirect(to="users:login")

        print("Form is not valid")
        return render(request, "users/sign_up.html", context={"form": form})

    return render(request, "users/sign_up.html", context={"form": RegisterForm()})


def login_user(request):
    if request.user.is_authenticated:
        return redirect(to="web_app:main")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users:login")

        login(request, user)
        return redirect(to="web_app:main")

    return render(request, "users/login.html", context={"form": LoginForm()})


@login_required
def logout_user(request):
    logout(request)
    return redirect(to="web_app:main")


@login_required
def profile(request, user):
    Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if profile_form.is_valid():
            profile_form.save()
            request.user.username = request.POST["username"]
            request.user.email = request.POST["email"]
            request.user.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect(to="users:profile", user=request.user)
        messages.error(request, "Error update profile!")

    profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "users/profile.html", {"profile_form": profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
    success_message = (
        "An email with instructions to reset your password has been sent to %(email)s."
    )
    subject_template_name = "users/password_reset_subject.txt"
