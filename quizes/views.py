import datetime

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse

from .models import QuizResult,ReportCard,Quiz,Option,UserAnswer
# Create your views here.

class QuizView(View):
    def get(self,request):
        return render(request, 'quizes/quizes.html')

@method_decorator(csrf_exempt, name='dispatch')
class QuizSubmit(View):
    def get(self, request, pk):

        quiz = get_object_or_404(Quiz, id=pk)
        start_time_key = f'quiz_{quiz.id}_start'
        
        if not request.session.get(start_time_key):
            request.session[start_time_key] = datetime.datetime.now().timestamp()

        total_seconds = quiz.time.total_seconds()   

        elapsed_seconds = datetime.datetime.now().timestamp() - request.session[start_time_key]

        remaining_seconds = total_seconds - elapsed_seconds

        if remaining_seconds <= 0:
            messages.error(request, "زمان آزمون به پایان رسیده است.")
            return redirect('student_dashboard')
        
        return render(request, 'quizes/quiz-submit.html', {'quiz': quiz, 'remaining_time': remaining_seconds})

    def post(self, request, pk):

        quiz = get_object_or_404(Quiz, id=pk)
        questions = quiz.question.all()
        user = request.user
        start_time_key = f'quiz_{quiz.id}_start'

        start_time = request.session.get(start_time_key)
        if not start_time:
            messages.error(request, "زمان آزمون به پایان رسیده است.")
            return redirect('student_dashboard')

        elapsed = datetime.datetime.now().timestamp() - start_time
        if elapsed > quiz.time.total_seconds():
            messages.warning(request, "زمان آزمون تمام شده است. پاسخ‌های ثبت شده ذخیره می‌شوند.")

        if QuizResult.objects.filter(user=user, quiz=quiz).exists():
            messages.error(request, "شما قبلاً در این آزمون شرکت کرده‌اید.")
            return redirect('student_dashboard')

  
        report_card, created = ReportCard.objects.get_or_create(user=user)

   
        quiz_result = QuizResult.objects.create(
            user=user,
            score=0,
            quiz=quiz
        )
        
        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                UserAnswer.objects.create(
                    quiz_result=quiz_result,
                    option=selected_option,
                    is_choosen=True
                )

        # به‌روزرسانی نمره
        quiz_result.calculate_score()
        quiz_result.rank()

        report_card.update_score()
        ReportCard.update_all_ranks()
        report_card.update_time()

        return redirect('student_dashboard')

    
