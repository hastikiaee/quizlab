from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse,HttpResponseNotAllowed

from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissions

from .models import UserProfile
from .forms import VerifyForm,LoginForm,QuizForm,QuestionFormset,OptionFormset,OptionForm,QuestionForm,CustomUserCreationForm,FullProfileForm
from .mixins import RoleRequiredMixin
from quizes.models import ReportCard,QuizResult,Quiz,Question,Option

import random
# Create your views here.

class SignUpView(View):

    def get (self,request):

        form =CustomUserCreationForm()
        return render(request,"users/signup.html",context={'form':form})
    
    def post(self,request):
        
        form=CustomUserCreationForm()
        if form.is_valid():
            email=form.cleaned_data['username']
            password1=form.cleaned_data['password1']
            role=form.cleaned_data['role']
            code = str(random.randint(100000, 999999))
            request.session['temp_user'] = {
                'email': email,
                'password': password1,
                'code': code,
                'role':role,
                }
            
            send_mail(message=f"{code}",subject="yoyr code",
                      from_email="hasti1383kiaee@gmail.com",recipient_list=[email])
            
            return redirect('verify')
        
        return render (request,"users/signup.html",context={"form":form})
            
            
class VerifyVeiw(View):

    def get(self, request):
        form = VerifyForm()
        return render(request, "users/verify.html", context={"form": form})


    def post(self,request):
            
        form=VerifyForm(request.POST)
        if form.is_valid():

            code1=form.cleaned_data["code"]
            code2=request.session.get('temp_user', {}).get('code')
            

            if code1==code2:
                
                user=get_user_model()
                username=request.session.get('temp_user', {}).get('email')
                password=request.session.get('temp_user', {}).get('password')
                role=request.session.get('temp_user', {}).get('role')
                
                if not user.objects.filter(username__exact=username).exists():
                    
                    user=user.objects.create_user(username=username,password=password)
                    UserProfile.objects.create(user=user,role=role)
                    
                    user.session.pop('temp_user', None)


                    return redirect("login")
                else:
                     return render(request,"users/verify.html",context={"form":form,"message":"کاربر وجود دارد"})
            else:
                return render(request,"users/verify.html",context={"form":form,"message":"failed"})
        
        return render(request,"users/verify.html",context={"form":form})
    
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    
    def get (self,request):

        form =LoginForm()
        return render(request,"users/login.html",context={'form':form})
    
    def post(self,request):
        
        form=LoginForm(request.POST)
        if form.is_valid():
            
            email=form.cleaned_data['username']
            password=form.cleaned_data["password"]
            user=authenticate(request,username=email,password=password)
            if user:
                login(request,user)
                if user.user_profile.role == 0:
                    return redirect('student_dashboard')
                else:
                    return redirect('professor_dashboard')
            return render(request,"users/login.html",context={"form":form,"message":"رمز عبور یا نام کاربری اشتباه است"})
        
        return render (request,"users/login.html",context={"form":form})

    
class LogoutView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse('با موفقیت خارج شدید')

    def get(self, request, *args, **kwargs):
        
        return render(request,'users/logout.html')
    
#داشبورد دانش اموز
@method_decorator(csrf_exempt, name='dispatch')
class StudentDashBoardView(LoginRequiredMixin,RoleRequiredMixin,View):
    allowed_roles = [0]
    login_url='/login/'
    def get(self,request):
        return render (request, 'users/student_dashboard.html')
#داشبورد استاد 
class ProfessorDashbaordView(LoginRequiredMixin,RoleRequiredMixin,View):

    login_url="/login/"
    allowed_roles = [1]

    def get(self,request):
        user=self.request.user
        quizes=Quiz.objects.filter(creator=user)
        quizes.number=quizes.count()
        quizes.total_participation=0
        for quiz in quizes:
            quizes.total_participation+=QuizResult.objects.filter(quiz=quiz).count()
            quiz.participation=QuizResult.objects.filter(quiz=quiz).count()

    

        context={'quizes':quizes}
        return render(request,'users/professor_dashboard.html',context=context)
    
class QuisResultDetailView(LoginRequiredMixin,RoleRequiredMixin,View):

    login_url='/login/'
    allowed_roles = [0]

    def get(self,request,pk):

        quizresult=QuizResult.objects.get(user=request.user,pk=pk)

        quizresult.num_questions = quizresult.quiz.question.count()
        quizresult.total_participation=QuizResult.objects.filter(quiz=quizresult.quiz).count()
        quizresult.percent=int((quizresult.score/quizresult.num_questions)*100)

        questions= quizresult.quiz.question.all()
        for q in questions:
            q.options=q.option.all()
            for o in q.options:
                o.is_choosen=o.user_answer.filter(quiz_result=quizresult, is_choosen=True).exists()
                if o.is_choosen and o.is_answer:
                    q.is_correct=True
                else:
                    q.is_correct=False
        '''for o in q.options:
            o.is_choosen=o.user_answer.filter(quiz_result=quizresult, is_choosen=True).exists()'''
        
        context={'quizresult':quizresult,"questions":questions}
        return render(request,'users/quizresult_detail.html',context=context)
        

class CreateQuizView(LoginRequiredMixin,RoleRequiredMixin,View):
    
    login_url='/login/'
    allowed_roles = [1]
    def get(self, request):


        quiz_form = QuizForm()
        question_formset = QuestionFormset(queryset=Question.objects.none())

        # bind OptionFormset to each Question form
        for q_form in question_formset.forms:
            q_form.option_formset = OptionFormset(prefix=f"options-{q_form.prefix}")

        return render(request, 'users/create_quiz.html', {
            'quiz_form': quiz_form,
            'question_formset': question_formset,
        })

    def post(self, request):

        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormset(request.POST, queryset=Question.objects.none())

        if quiz_form.is_valid() and question_formset.is_valid():

            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user
            quiz.save()

            # ذخیره سؤالات
            questions = question_formset.save(commit=False)

            for q_form, question in zip(question_formset.forms, questions):

                question.quiz = quiz
                question.save()

                # OptionFormset مربوط به این سؤال
                option_formset = OptionFormset(
                    request.POST,
                    prefix=f"options-{q_form.prefix}",
                    instance=question
                )

                if option_formset.is_valid():
                    option_formset.save()

            return redirect('professor_dashboard')

        # اگر خطا بود، دوباره formset های گزینه‌ها را bind کن
        for q_form in question_formset.forms:
            q_form.option_formset = OptionFormset(
                request.POST,
                prefix=f"options-{q_form.prefix}"
            )

        return render(request, 'users/create_quiz.html', {
            'quiz_form': quiz_form,
            'question_formset': question_formset,
        })

class DeleteQuizView(LoginRequiredMixin,RoleRequiredMixin,View):
    login_url='/login/'
    allowed_roles = [1]

    def post(self,request,pk):
       
        quiz = Quiz.objects.get(pk=pk)
        quiz.delete()
        return redirect('professor_dashboard')
    
class EditQuizView(LoginRequiredMixin,RoleRequiredMixin,View):
    login_url='/login/'
    allowed_roles = [1]

    def get(self,request,pk):
        
        quiz=Quiz.objects.get(pk=pk)
        quiz_form = QuizForm(instance=quiz) 
        questions=quiz.question.all()
        for question in questions:
            correct_option = question.option.filter(is_answer=True).first()
            question.correct_option = correct_option.text if correct_option else None
        

        return render(request, 'users/edit_quiz.html', {'quiz_form': quiz_form , 'questions':questions,"quiz":quiz})
    def post(self,request,pk):
        quiz=Quiz.objects.get(pk=pk)
        questions=Question.objects.filter(quiz=quiz)

        quiz_form = QuizForm(request.POST,instance=quiz) 
        
        if quiz_form.is_valid() :
            quiz=quiz_form.save()

            return redirect('professor_dashboard')
        return render(request, 'users/edit_quiz.html', {'quiz_form': quiz_form , 'questions':questions,"quiz":quiz})
    
class EditQuestionView(RoleRequiredMixin,LoginRequiredMixin,View):

    login_url='/login/'
    allowed_roles = [1]
    
    def get(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk)
        quiz = question.quiz  # برای بازگشت بعد از ذخیره یا نمایش نام آزمون
        question_form = QuestionForm(instance=question)
        option_formset = OptionFormset(instance=question)

        return render(request, 'users/edit_question.html', {
            'quiz': quiz,
            'question': question,
            'question_form': question_form,
            'option_formset': option_formset,
        })

class RankingView(LoginRequiredMixin,View):

    login_url='/login/'

    def get(self,request):

        reports = ReportCard.objects.all().order_by('rank')
        return render(request,'users/ranking.html',{'reports':reports})

class UserProfileView(LoginRequiredMixin,View):
    
    login_url='/login/'

    def get(self,request):
        user_profile=request.user.user_profile
        form=FullProfileForm(instance=user_profile,user=request.user)
        return render(request,'users/profile.html',{'form':form})
    
    def post(self,request):
        user_profile=request.user.user_profile
        form = FullProfileForm(request.POST,instance=user_profile,user=request.user)
        if form.is_valid():
            form.save()
            if form.cleaned_data['password']:
                logout(request)
                return redirect('login') 

        return render(request,'users/profile.html',{'form':form}) 
        
    
