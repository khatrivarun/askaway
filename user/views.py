from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm, UpdateForm


def register(request):
    """
    User Registration function
    """

    # Preparing the form
    form = RegistrationForm(request.POST or None)

    # Checking if the form is valid
    if form.is_valid():

        # Save the user object.
        form.save()

        # Redirect to login page.
        return redirect('/user/login')
    else:

        # Clean form in case of invalid inputs
        form = RegistrationForm()

    # Setting up the template to render on and context
    template_name = "user/register.html"
    context = {"form": form}

    # Rendering the form.
    return render(request, template_name, context)


@login_required
def update(request):
    """
    User update function.
    """

    # Fetch the user and prepare form with values filled in.
    user = get_object_or_404(User, username=request.user.username)
    form = UpdateForm(request.POST or None, instance=user, user=user)

    # Checking if the form is valid
    if form.is_valid():

        # Update user details
        form.save()

        # Redirect to home page.
        return redirect('/')
    else:

        # Recreate the form with filled in values.
        form = UpdateForm(request.POST or None, instance=user)

    # Setting up the template to render on and context
    template_name = "user/update.html"
    context = {"form": form}

    # Rendering the form.
    return render(request, template_name, context)


def update_password(request):
    """
    User Password Update Function.
    """

    # Preparing the form
    form = PasswordChangeForm(request.user, request.POST)

    # Checking if the form is valid
    if form.is_valid():

        # Update the password
        user = form.save()

        # Update the session
        update_session_auth_hash(request, user)

        # Redirect to homepage
        return redirect('/')
    else:

        # Cleaning out invalid values
        form = PasswordChangeForm(request.user)

    # Setting up the template to render on and context
    template_name = "user/update_password.html"
    context = {"form": form}

    # Rendering the form.
    return render(request, template_name, context)
