from django import template
from django.shortcuts import get_object_or_404
register = template.Library()
##
from quizes.models import QuizResult,ReportCard

@register.simple_tag(takes_context=True)
def rank(context):
    request = context['request']
    
    try:
        report = ReportCard.objects.get(user=request.user)
        return report.rank
    except ReportCard.DoesNotExist:
        return 0

@register.simple_tag(takes_context=True)
def avg(context):
    request = context['request']
    
    all_quizes = QuizResult.objects.filter(user=request.user).count()
    
    try:
        report_card = get_object_or_404(ReportCard, user=request.user)
        score = report_card.score
    except:
        score = 0

    if all_quizes != 0:
        avg_value = score / all_quizes
    else:
        avg_value = 0

    return avg_value, all_quizes

@register.simple_tag(takes_context=True)
def quiz_results(context):
    request=context['request']        
    quizresults=QuizResult.objects.filter(user=request.user)
    for q in quizresults:
        q.num_questions = q.quiz.question.count()
        q.total_participation=QuizResult.objects.filter(quiz=q.quiz).count()
        q.percent=int((q.score/q.num_questions)*100)
    return quizresults

