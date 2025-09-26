from django.urls import path
from main.views import (
    QuestionListCreateView, 
    QuestionRetrieveDeleteView, 
    AnswerCreateView, 
    AnswerRetrieveDeleteView
)

urlpatterns = [
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path("questions/<int:pk>/", QuestionRetrieveDeleteView.as_view(), name="question-retrieve-delete"),
    path("questions/<int:pk>/answers/", AnswerCreateView.as_view(), name="answer-create"),
    path("answers/<int:pk>/", AnswerRetrieveDeleteView.as_view(), name="answer-retrieve-delete"),
]