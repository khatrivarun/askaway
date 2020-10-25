from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm


def register(request):
    form = RegistrationForm(request.POST or None)
    template_name = "user/register.html"
    context = {"form": form}

    if form.is_valid():
        form.save()
        redirect('/')
    else:
        form = RegistrationForm()

    return render(request, template_name, context)


def signin(request):
    form = LoginForm(request.POST or None)
    template_name = "user/login.html"
    context = {"form": form}

    if form.is_valid():
        user = form.login(request)
        if user:
            login(request, user=user)
            redirect('/')
    else:
        form = LoginForm()

    return render(request, template_name, context)
