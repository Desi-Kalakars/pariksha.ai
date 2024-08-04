from typing import List, Union

from pydantic import BaseModel


class Choice(BaseModel):
    text: str
    is_correct: bool


class Question(BaseModel):
    question_text: str
    question_type: str
    choices: Union[List[Choice], None]
    correct_answer: Union[str, None]


class ResponseModel(BaseModel):
    status: str
    questions: List[Question]
