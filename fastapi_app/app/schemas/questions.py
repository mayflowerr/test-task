from datetime import datetime
from pydantic import BaseModel, field_validator, ConfigDict, Field
from typing import List


class QuestionIn(BaseModel):
    text: str

    @field_validator("text")
    def check_text(cls, value):
        clear_text = value.strip()
        if not clear_text:
            raise ValueError("text is required")
        return clear_text
    

class QuestionOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerIn(BaseModel):
    user_id: str
    text: str

    @field_validator("text")
    def check_text(cls, value):
        clear_text = value.strip()
        if not clear_text:
            raise ValueError("text is required")
        return clear_text
    

class AnswerOut(BaseModel):
    id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswersOut(BaseModel):
    answers: List[AnswerOut] = Field(default_factory=list)