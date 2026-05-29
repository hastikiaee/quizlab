from django import template
register = template.Library()
##
from quizes.models import Quiz,Question,Option



@register.simple_tag()
def quizes():
     
    quizes=Quiz.objects.all()
    for quiz in quizes:
        quiz.numquestions=quiz.question.count()
    return quizes

@register.simple_tag()
def quiz(pk):
    quiz=Quiz.objects.get(pk=pk)

    return quiz

@register.simple_tag()
def questions(pk):
    questions=Question.objects.filter(quiz__pk=pk)
    return questions

@register.simple_tag()
def options(pk):
    options=Option.objects.filter(question__quiz__pk=pk)
    return options