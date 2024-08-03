from typing import Union, Optional
from fastapi import APIRouter, Form, HTTPException, UploadFile
from services.question_generation import QuestionGeneratingService
from models.questions_response import ResponseModel

router = APIRouter()
question_generating_service = QuestionGeneratingService()


@router.post("/generate-questions", response_model=ResponseModel)
async def generate_questions(
    file: Union[UploadFile, None] = None,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    q_type_mcq_single: int = Form(...),
    q_type_mcq_multiple: int = Form(...),
    q_type_descriptive: int = Form(...),
    q_type_fill_in_the_blanks: int = Form(...),
):
    # Validate that at least one question type is greater than zero
    if (
        q_type_mcq_single <= 0
        and q_type_mcq_multiple <= 0
        and q_type_descriptive <= 0
        and q_type_fill_in_the_blanks <= 0
    ):
        raise HTTPException(
            status_code=400,
            detail="At least one question type must be greater than zero.",
        )

    # Determine file type and read content
    if file:
        if not file.filename.endswith((".pdf", ".docx")):
            # Handle unsupported file type error
            raise HTTPException(
                status_code=400,
                error="Unsupported file type. Please upload a PDF, DOC, or DOCX file.",
            )
    questions_response = await question_generating_service.generate_questions(
        file,
        subject,
        content,
        q_type_mcq_single,
        q_type_mcq_multiple,
        q_type_descriptive,
        q_type_fill_in_the_blanks,
    )
    # Return the response
    return {"status": "success", "questions": questions_response["questions"]}
