from django.forms import ModelForm, Textarea
from .models import Question, Answer


# Question Form
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'description']


# Answer Form/
class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']
        widgets = {
            'answer': Textarea(attrs={'rows': 5, 'cols': 125})
        }
