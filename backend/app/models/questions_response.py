from pydantic import BaseModel
from typing import List

class Questions(BaseModel):
    mcq_single: List[str]
    mcq_multiple: List[str]
    fill_in_the_blanks: List[str]
    descriptive: List[str]

class ResponseModel(BaseModel):
    status: str
    questions: Questions
