from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, logout
from .forms import RegistrationForm, UpdateForm, DeleteAccountForm
from questions_answers.models import Question, Answer, Vote
from django.db.models import Count


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


@login_required
def view_me(request):
    """
    Display User and their questions and answers
    """

    # Getting the user.
    user = request.user

    # Getting their questions.
    questions = Question.objects.filter(user=user)

    # Getting number of answers per questions.
    total_answers = Answer.objects.filter(question__in=questions).values('question_id').annotate(
        total_answers=Count('question_id'))

    # Converting it into a dictionary of question_id to answers for ease.
    total_answers = {answer_['question_id']: answer_['total_answers'] for answer_ in total_answers}

    # Getting their answers.
    answers = Answer.objects.filter(user=user)

    # Getting votes per each answer.
    total_votes = Vote.objects.filter(answer__in=answers).values('answer').annotate(total_votes=Count('answer'))

    # Converting it into a dictionary of answer_id to votes for ease.
    total_votes = {vote_['answer']: vote_['total_votes'] for vote_ in total_votes}

    # Setting up the context and the template name to render on.
    context = {'questions': questions, 'answers': answers, 'display_user': user, 'total_answers': total_answers,
               'total_votes': total_votes}
    template_name = 'user/user.html'

    # Rendering the question and its answers.
    return render(request, template_name, context)


def view_user(request, username):
    """
    Display User and their questions and answers
    """

    # Getting the user.
    user = get_object_or_404(User, username=username)

    # Getting their questions.
    questions = Question.objects.filter(user=user)

    # Getting number of answers per questions.
    total_answers = Answer.objects.filter(question__in=questions).values('question_id').annotate(
        total_answers=Count('question_id'))

    # Converting it into a dictionary of question_id to answers for ease.
    total_answers = {answer_['question_id']: answer_['total_answers'] for answer_ in total_answers}

    # Getting their answers.
    answers = Answer.objects.filter(user=user)

    # Getting votes per each answer.
    total_votes = Vote.objects.filter(answer__in=answers).values('answer').annotate(total_votes=Count('answer'))

    # Converting it into a dictionary of answer_id to votes for ease.
    total_votes = {vote_['answer']: vote_['total_votes'] for vote_ in total_votes}

    # Setting up the context and the template name to render on.
    context = {'questions': questions, 'answers': answers, 'display_user': user, 'total_answers': total_answers,
               'total_votes': total_votes}
    template_name = 'user/user.html'

    # Rendering the question and its answers.
    return render(request, template_name, context)


@login_required
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


@login_required
def delete_account(request):
    """
    User Delete Function
    """

    # Getting the user.
    user = get_object_or_404(User, username=request.user.username)

    # Preparing the form.
    form = DeleteAccountForm(request.POST or None)

    # Checking if the form is valid
    if form.is_valid():

        # Deleting user object
        user.delete()

        # Logging out from the seesion.
        logout(request)

        # Redirecting to register page
        return redirect('/user/register')
    else:
        # Cleaning out invalid values
        form = DeleteAccountForm()

    # Setting up the template to render on and context
    template_name = "user/delete_account.html"
    context = {"form": form}

    # Rendering the form.
    return render(request, template_name, context)
