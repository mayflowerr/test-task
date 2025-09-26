from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from main.models import Question, Answer
from main.serializers import (
    QuestionSerializer, 
    AnswerSerializer, 
    QuestionWithAnswersSerializer
)


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.order_by("-id")
    serializer_class = QuestionSerializer


class QuestionRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.order_by("-id")
    serializer_class = QuestionWithAnswersSerializer\
    

class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        q = get_object_or_404(Question, pk=kwargs["pk"])
        data = request.data.copy()
        ser = self.get_serializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save(question=q)
        return Response(ser.data, status=status.HTTP_201_CREATED)
    

class AnswerRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.order_by("-id")
    serializer_class = AnswerSerializer