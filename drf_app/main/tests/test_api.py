import pytest
from rest_framework.test import APIClient
from main.models import Question
from django.urls import reverse


@pytest.fixture()
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_question_and_list(client):
    # create
    response = client.post(reverse("question-list-create"), 
                           {"text": "First question"}, 
                           format="json")
    assert response.status_code == 201
    qid = response.json()["id"]

    # list
    response = client.get(reverse("question-list-create"))
    assert response.status_code == 200
    data = response.json()
    assert any(q["id"] == qid and q["text"] == "First question" for q in data)


@pytest.mark.django_db
def test_question_detail_with_answers_and_cascade(client):
    # create question
    question = Question.objects.create(text="Q1")

    # add two answers
    answer1 = client.post(reverse("answer-create", args=[question.id]),
                          {"user_id": "u1", "text": "A1"}, 
                          format="json")
    answer2 = client.post(reverse("answer-create", args=[question.id]),
                          {"user_id": "u1", "text": "A2"}, 
                          format="json")
    assert answer1.status_code == 201 and answer2.status_code == 201
    a1_id = answer1.json()["id"]

    # detail question includes answers
    response = client.get(reverse("question-retrieve-delete", args=[question.id]))
    assert response.status_code == 200
    detail = response.json()
    assert detail["id"] == question.id
    assert len(detail["answers"]) == 2

    # delete question -> answers must be gone
    response = client.delete(reverse("question-retrieve-delete", args=[question.id]))
    assert response.status_code == 204
    # answer fetch -> 404
    response = client.get(reverse("answer-retrieve-delete", args=[a1_id]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_cannot_create_answer_for_missing_question(client):
    response = client.post(reverse("answer-create", args=[99999]),
                       {"user_id": "u1", "text": "oops"}, 
                       format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_validation_non_empty_text(client):
    # question text must not be empty
    response = client.post(reverse("question-list-create"), {"text": "   "}, format="json")
    assert response.status_code == 400

    # answer text must not be empty
    question = Question.objects.create(text="Q")
    response = client.post(reverse("answer-create", args=[question.id]), {"user_id": "u1", "text": "   "}, format="json")
    assert response.status_code == 400