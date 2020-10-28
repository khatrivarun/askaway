from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Count
import uuid

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer, Vote


def list_questions(request):
    """
    Function used to fetch all questions from the database.
    """

    # Get all questions from the database
    list_of_questions = Question.objects.all()

    # Setting the context and
    # the template to render on
    context = {'questions': list_of_questions}
    template_name = 'questions_answers/questions_all.html'

    # Rendering all the questions.
    return render(request, template_name, context)


def list_single_question(request, slug):
    """
    Function which handles getting a single question,
    all answers to that question, user liked answers
    and all likes an answer got
    """

    # Getting the question and its answers.
    question = get_object_or_404(Question, slug=slug)
    answers = Answer.objects.filter(question=question)
    user = request.user

    # Loading Answer Form.
    answer_form = AnswerForm(request.POST or None)

    # Getting total votes for each answer from the database.
    total_votes = Vote.objects.filter(answer__in=answers).values('answer').annotate(total_votes=Count('answer'))

    # Converting it into a dictionary of answer_id to votes for ease.
    total_votes = {vote_['answer']: vote_['total_votes'] for vote_ in total_votes}

    if not user.is_anonymous:
        # Getting all the answers the user liked from the given list of answers
        votes = Vote.objects.filter(user=user, answer__in=answers)

        # Converting it into a list of answer_ids for ease.
        user_votes = [vote_.answer for vote_ in votes]
    else:
        user_votes = list()

    # Setting up the context and the template name to render on.
    context = {'question': question, 'answers': answers, 'voted': user_votes, 'total_votes': total_votes,
               'form': answer_form}
    template_name = 'questions_answers/question.html'

    # Rendering the question and its answers.
    return render(request, template_name, context)


@login_required
def create_question(request):
    """
    Function which creates a question in the database
    based on the user input
    """

    # Preparing Django Form to render
    question_form = QuestionForm(request.POST or None)

    # Checking if the form is validated/
    if question_form.is_valid():

        # Get all the values from the form
        question = question_form.save(commit=False)

        # Generate a unique slug for the question.
        slug = slugify(question.question) + str(uuid.uuid4())

        # Assigning slug and the user it belongs to.
        question.slug = slug
        question.user = request.user

        # Saving the question in database.
        question.save()

        # Redirecting to all questions.
        return redirect('/questions/all')
    else:

        # Clean the form on invalid inputs
        question_form = QuestionForm(request.POST or None)

    # Setting up context and template to render on.
    template_name = 'questions_answers/create_question.html'
    context = {'form': question_form}

    # Rendering the form.
    return render(request, template_name, context)


@login_required
def update_single_question(request, slug):
    """
    Function which is responsible to update a given question.
    """

    # Get the user and the question
    user = request.user
    question = get_object_or_404(Question, slug=slug, user=user)

    # Prepare the question form with filled in values.
    question_form = QuestionForm(request.POST or None, instance=question)

    # Checking if the form is validated.
    if question_form.is_valid():

        # Update the values of the question
        question_form.save()

        # Redirect to the question page.
        return redirect(f'/questions/question/{question.slug}')
    else:

        # Clean out the form on invalid values.
        question_form = QuestionForm(request.POST or None, instance=question)

    # Setting up context and template to render on.
    context = {'form': question_form}
    template_name = 'questions_answers/update_question.html'

    # Rendering the form.
    return render(request, template_name, context)


@login_required
def delete_question(request, slug):
    """
    Function which is responsible to delete a given question.
    """

    # Get the user from the session.
    user = request.user

    # Get the user question from the database.
    question = get_object_or_404(Question, slug=slug, user=user)

    # If the user confirmed the delete.
    if request.method == "POST":
        # Delete the question,
        question.delete()

        # Redirect to all questions.
        return redirect('/questions/all')

    # Setting up the template to render on and the context.
    template_name = ''
    context = {'question': question}

    # Rendering.
    return render(request, template_name, context)


@login_required
def create_answer(request, slug):
    """
    Function which creates an answer for
    a specific question in the database
    based on the user input.
    """

    # Get the user and the question.
    user = request.user

    # Prepare the answer form.
    question = get_object_or_404(Question, slug=slug)
    answer_form = AnswerForm(request.POST or None)

    # Checking if the form is valid.
    if answer_form.is_valid() and request.method == "POST":
        # Gettting the form values.
        answer = answer_form.save(commit=False)

        # Setting the question
        # and the user references.
        answer.question = question
        answer.user = user

        # Saving the answer
        answer.save()

        # Redirecting to that specific question
        return redirect(f'/questions/question/{question.slug}')


@login_required
def delete_answer(request, slug, answer_id):
    """
    Function which is responsible to delete a given question.
    """

    # Get the user, question and the answer.
    user = request.user
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, question=question, id=answer_id, user=user)

    # If the user confirmed the delete.
    if request.method == "POST":
        # Delete the answer
        answer.delete()

        # Redirect to the question page.
        return redirect(f'/questions/question/{slug}')

    # Setting up the template to render on and the context.
    template_name = ''
    context = {'answer': answer}

    # Rendering.
    return render(request, template_name, context)


@login_required
def vote(request, answer_id, slug):
    """
    Function responsible for voting up
    or deleting the vote from an answer
    """

    # Get the user, question and the answer.
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user

    # Fetching the vote if the user liked the answer.
    vote_ = Vote.objects.filter(answer=answer, user=user)

    # If it exists, delete it.
    if vote_:
        vote_.delete()

    # If it does not exist, create one.
    else:
        new_vote = Vote()
        new_vote.user = user
        new_vote.answer = answer
        new_vote.save()

    # Render back the question page.
    return redirect(f'/questions/question/{question.slug}')
