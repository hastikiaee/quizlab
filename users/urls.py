from django.urls import path
from .views import (SignUpView,VerifyVeiw,LoginView,LogoutView,StudentDashBoardView,
                    QuisResultDetailView,ProfessorDashbaordView,CreateQuizView,DeleteQuizView,EditQuizView,EditQuestionView,
                    RankingView,UserProfileView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyVeiw.as_view(), name='verify'),
    path('login/',LoginView.as_view(),name="login"),
    path("logout/",LogoutView.as_view(),name='logout'),
    path("ranking/",RankingView.as_view(),name='ranking'),
    path("profile/",UserProfileView.as_view(),name='profile'),
    path('student/dashboard/',StudentDashBoardView.as_view(),name='student_dashboard'),
    path('professor/dashboard/',ProfessorDashbaordView.as_view(),name='professor_dashboard'),
    path('student/dashboard/result_detail/<int:pk>',QuisResultDetailView.as_view(),name='quizresult_detail'),
    path('professor/dashboard/create_quiz/',CreateQuizView.as_view(),name="create_quiz"),
    path('professor/dashboard/delete_quiz/<int:pk>/',DeleteQuizView.as_view(),name="delete_quiz"),
    path('professor/dashboard/edit_quiz/<int:pk>/',EditQuizView.as_view(),name="edit_quiz"),
    path('professor/dashboard/edit_question/<int:question_pk>/',EditQuestionView.as_view(),name="edit_question")
]