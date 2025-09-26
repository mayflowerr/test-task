# fastapi_app/tests/test_api.py
def test_create_question_and_list(client):
    resp = client.post("/questions/", json={"text": "First question"})
    assert resp.status_code == 201
    qid = resp.json()["id"]

    resp = client.get("/questions/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(q["id"] == qid and q["text"] == "First question" for q in data)


def test_question_detail_with_answers_and_cascade(client):
    # create question
    resp = client.post("/questions/", json={"text": "Q1"})
    qid = resp.json()["id"]

    # add two answers
    a1 = client.post(f"/questions/{qid}/answers/", json={"user_id": "u1", "text": "A1"})
    a2 = client.post(f"/questions/{qid}/answers/", json={"user_id": "u1", "text": "A2"})
    assert a1.status_code == 201 and a2.status_code == 201
    a1_id = a1.json()["id"]

    # question detail includes answers
    resp = client.get(f"/questions/{qid}")
    assert resp.status_code == 200
    detail = resp.json()
    assert detail["id"] == qid
    assert len(detail["answers"]) == 2

    # delete question -> delete answers
    resp = client.delete(f"/questions/{qid}")
    assert resp.status_code == 204

    # get deleted answer -> 404
    resp = client.get(f"/answers/{a1_id}")
    assert resp.status_code == 404


def test_cannot_create_answer_for_missing_question(client):
    resp = client.post("/questions/99999/answers/", json={"user_id": "u1", "text": "oops"})
    assert resp.status_code == 404


def test_validation_non_empty_text(client):
    resp = client.post("/questions/", json={"text": "   "})
    assert resp.status_code == 422

    # create valid question
    q = client.post("/questions/", json={"text": "Q"}).json()
    resp = client.post(f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": "   "})
    assert resp.status_code == 422 
