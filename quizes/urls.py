from django.urls import path

from .views import QuizView,QuizSubmit

urlpatterns =[
    path('quizes/', QuizView.as_view(), name='quizes'),
    path('quizes/<int:pk>', QuizSubmit.as_view(), name='quize-submit'),
]