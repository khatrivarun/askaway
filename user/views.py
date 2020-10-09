from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def register(request):
    form = UserCreationForm(request.POST or None)
    template_name = "user/register.html"
    context = {"form": form}

    if form.is_valid():
        form.save()
        redirect('/')
    else:
        form = UserCreationForm()

    return render(request, template_name, context)
