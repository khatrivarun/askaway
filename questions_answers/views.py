from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import uuid

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer


def list_questions(request):
    list_of_questions = Question.objects.all()
    context = {'questions': list_of_questions}
    template_name = ''
    return render(request, template_name, context)


def list_single_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    answers = Answer.objects.filter(question=question)
    context = {'question': question, 'answers': answers}
    template_name = 'questions_answers/question.html'
    return render(request, template_name, context)


@login_required
def create_question(request):
    question_form = QuestionForm(request.POST or None)

    if question_form.is_valid():
        question = question_form.save(commit=False)
        slug = slugify(question.question) + str(uuid.uuid4())
        question.slug = slug
        question.user = request.user
        question.save()
        return redirect('/')
    else:
        question_form = QuestionForm()

    template_name = 'questions_answers/create_question.html'
    context = {'form': question_form}
    return render(request, template_name, context)


@login_required
def update_single_question(request, slug):
    user = request.user
    question = get_object_or_404(Question, slug=slug, user=user)
    question_form = QuestionForm(request.POST or None, instance=question)
    context = {'form': question_form}
    template_name = 'questions_answers/update_question.html'

    if question_form.is_valid():
        question_form.save()
        return redirect('/')

    return render(request, template_name, context)


@login_required
def delete_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    template_name = ''
    context = {'question': question}
    if request.method == "POST":
        question.delete()
        return redirect('/')
    return render(request, template_name, context)


@login_required
def create_answer(request, slug):
    question = get_object_or_404(Question, slug=slug)
    answer_form = AnswerForm(request.POST or None)

    if answer_form.is_valid():
        answer = answer_form.save(commit=False)
        answer.question = question
        answer.user = request.user
        answer.save()
        answer_form = AnswerForm()
        return redirect('/')

    template_name = ''
    context = {'form': answer_form}
    return render(request, template_name, context)


@login_required
def delete_answer(request, slug, id):
    question = get_object_or_404(Question, slug=slug)
    answer = get_object_or_404(Answer, question=question, id=id)
    template_name = ''
    context = {'answer': answer}
    if request.method == "POST":
        answer.delete()
        return redirect('/')
    return render(request, template_name, context)
