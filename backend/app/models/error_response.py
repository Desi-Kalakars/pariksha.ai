from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str
