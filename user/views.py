from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm, UpdateForm


def register(request):
    form = RegistrationForm(request.POST or None)
    template_name = "user/register.html"
    context = {"form": form}

    if form.is_valid():
        form.save()
        return redirect('/user/login')
    else:
        form = RegistrationForm()

    return render(request, template_name, context)


@login_required
def update(request):
    user = get_object_or_404(User, username=request.user.username)
    form = UpdateForm(request.POST or None, instance=user, user=user)
    template_name = "user/update.html"
    context = {"form": form}

    if form.is_valid():
        form.save()
        redirect('/')
    else:
        form = UpdateForm(request.POST or None, instance=user)

    return render(request, template_name, context)


def update_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    template_name = "user/update_password.html"
    context = {"form": form}

    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('/')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, template_name, context)
