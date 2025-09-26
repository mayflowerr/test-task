from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.main import get_db
from sqlalchemy import select
from app import models
from app.schemas.questions import (
    QuestionIn,
    QuestionOut,
    AnswerIn,
    AnswerOut,
    QuestionWithAnswersOut,
)

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)

@router.get("/", response_model=list[QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    rows = db.scalars(select(models.Question).order_by(models.Question.id.desc())).all()
    return rows


@router.post("/", response_model=QuestionOut, status_code=201)
def create_question(payload: QuestionIn, db: Session = Depends(get_db)):
    question = models.Question(text=payload.text)
    db.add(question); 
    db.commit();
    db.refresh(question)
    return question


@router.get("/{qid}", response_model=QuestionWithAnswersOut)
def get_question(qid: int, db: Session = Depends(get_db)):
    question = db.get(models.Question, qid)
    if not question:
        raise HTTPException(404, "Question not found")
    return question


@router.delete("/{qid}", status_code=204)
def delete_question(qid: int, db: Session = Depends(get_db)):
    question = db.get(models.Question, qid)
    if not question:
        raise HTTPException(404, "Question not found")
    db.delete(question); 
    db.commit()
    return


@router.post("/{qid}/answers/", response_model=AnswerOut, status_code=201)
def add_answer(qid: int, payload: AnswerIn, db: Session = Depends(get_db)):
    question = db.get(models.Question, qid)
    if not question:
        raise HTTPException(404, "Question not found")
    answer = models.Answer(question=question, user_id=payload.user_id, text=payload.text)
    db.add(answer); 
    db.commit(); 
    db.refresh(answer)
    return answer