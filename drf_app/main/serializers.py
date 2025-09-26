from rest_framework import serializers
from main.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'user_id', 
            'text', 
            'created_at'
        ]
        read_only_fields = [
            'id', 
            'question', 
            'created_at'
        ]

    def validate_text(self, value):
        clear_text = value.strip()
        if not clear_text:
            raise serializers.ValidationError('text must not be empty')
        return clear_text
    

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'text', 
            'created_at'
        ]
        read_only_fields = [
            'id', 
            'created_at'
        ]

    def validate_text(self, value):
        clear_text = value.strip()
        if not clear_text:
            raise serializers.ValidationError('text must not be empty')
        return clear_text
    

class QuestionWithAnswersSerializer(QuestionSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta(QuestionSerializer.Meta):
        fields = [
            'id',
            'text', 
            'created_at',
            'answers'
        ]