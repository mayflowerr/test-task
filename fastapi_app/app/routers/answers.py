from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.main import get_db
from app import models
from app.schemas.questions import (
    AnswerOut,
)

router = APIRouter(
    prefix="/answers",
    tags=["answers"],
)


@router.get("/{aid}", response_model=AnswerOut)
def get_answer(aid: int, db: Session = Depends(get_db)):
    answer = db.get(models.Answer, aid)
    if not answer:
        raise HTTPException(404, "Answer not found")
    return answer


@router.delete("/{aid}", status_code=204)
def delete_answer(aid: int, db: Session = Depends(get_db)):
    answer = db.get(models.Answer, aid)
    if not answer:
        raise HTTPException(404, "Answer not found")
    db.delete(answer); 
    db.commit()
    return