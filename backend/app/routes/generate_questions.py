from typing import Union, Optional
from fastapi import APIRouter, Form, HTTPException, UploadFile
from services.question_generation import QuestionGeneratingService
from models.questions_response import ResponseModel

router = APIRouter()
question_generating_service = QuestionGeneratingService()


@router.post("/generate-questions", response_model=ResponseModel)
async def generate_questions(
    file: Union[UploadFile, None] = None,
    subject: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    difficulty: Optional[str] = Form(None),
    q_type_mcq_single: Optional[int] = Form(None),
    q_type_mcq_multiple: Optional[int] = Form(None),
    q_type_descriptive: Optional[int] = Form(None),
    q_type_fill_in_the_blanks: Optional[int] = Form(None),
):
    # Validate that either file or content is provided
    if file is None and not content:
        raise HTTPException(
            status_code=400,
            detail="Either a file must be uploaded or content must be provided.",
        )

    # Validate that at least one question type is provided and greater than zero
    if not any(
        q_type is not None and q_type > 0
        for q_type in [
            q_type_mcq_single,
            q_type_mcq_multiple,
            q_type_descriptive,
            q_type_fill_in_the_blanks,
        ]
    ):
        raise HTTPException(
            status_code=400,
            detail="At least one question type must be provided and greater than zero.",
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
        difficulty,
        q_type_mcq_single,
        q_type_mcq_multiple,
        q_type_descriptive,
        q_type_fill_in_the_blanks,
    )
    # Return the response
    return {"status": "success", "questions": questions_response["questions"]}
