from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Sum, Avg
from django.conf import settings
from django_jalali.db import models as jmodels

import datetime



class Quiz (models.Model):
    
    creator=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,related_name='quiz')
    date = models.DateField(_("date"),default=timezone.now, auto_now_add=False,null=False,blank=False)
    title=models.CharField(_('title'),blank=False,null=False)
    time=models.DurationField(_('time'),blank=False,null=False)
    description=models.TextField(_('description'),blank=True)

    def __str__(self):
        return self.title

class Question (models.Model):

    quiz=models.ForeignKey(Quiz,verbose_name=_('quiz'), on_delete=models.CASCADE,related_name='question')
    title=models.TextField(_("title"),blank=False,null=False)

    def __str__(self):
        return self.title

class Option (models.Model):

    question=models.ForeignKey(Question,verbose_name=_("question"), on_delete=models.CASCADE,related_name='option')
    text=models.TextField(_("text"),blank=False,null=False)
    is_answer=models.BooleanField(_('is answer'),default=False)


    def clean(self):
        
        if self.question.option.count()>4:
            raise ValidationError('نمی‌توان بیش از 4 گزینه برای هر سوال ثبت کرد.')

    def save (self,*args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
    
  
class QuizResult(models.Model):
    
    user=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(""), on_delete=models.CASCADE,related_name='quizresult')
    quiz=models.ForeignKey( Quiz,verbose_name=_("quiz"), on_delete=models.CASCADE,related_name='quizresult')
    time=models.DurationField(_('time'),default=datetime.timedelta(0))
    score=models.IntegerField(_('score'),blank=False,null=False,default=0)
    date_time=jmodels.jDateField(auto_now_add=True)
    

    def calculate_score(self):
        score=0
        user_answers=self.user_answer.filter(is_choosen=True)
        for user_answer in user_answers:
            if user_answer.option.is_answer:
                score+=1
        self.score=score
        self.save(update_fields=['score'])
        return self.score
        
    def rank(self):
    
        all_results = self.quiz.quizresult.all().order_by('-score', 'time').values_list('user_id', flat=True)
        for idx, result_id in enumerate(all_results, start=1):
            if result_id == self.user_id:
                return idx
        
            
           
class UserAnswer(models.Model):

    quiz_result=models.ForeignKey(QuizResult,verbose_name=_('quiz rsult'),on_delete=models.CASCADE,related_name='user_answer')
    option=models.ForeignKey(Option,verbose_name=("option"),on_delete=models.CASCADE,related_name='user_answer')

    is_choosen=models.BooleanField(_('user answer'),default=False)


        
class ReportCard(models.Model):

    user=models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE,related_name='reportcard')
    score=models.IntegerField(_('score'),default=0)
    time=models.DurationField(_("time"),default=datetime.timedelta(0))
    rank=models.IntegerField(_("rank"),default=0)

    def update_score(self):
        agg=self.user.quizresult.all().aggregate(total=Sum('score'))
        self.score=agg['total'] or 0
        self.save()

    def update_time(self):
        agg=self.user.quizresult.all().aggregate(total=Sum('time'))
        self.time=agg['total'] or datetime.timedelta(0)
        self.save()

    @staticmethod
    def update_all_ranks():
        all_reportcards = ReportCard.objects.all().order_by('-score', 'time')
        for idx, report in enumerate(all_reportcards, start=1):
            if report.rank != idx:
                report.rank = idx
                report.save()

