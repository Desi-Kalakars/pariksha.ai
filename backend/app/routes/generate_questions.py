from typing import Union, Optional
from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from services.question_generation import QuestionGeneratingService
from models.questions_response import ResponseModel
from models.error_response import ErrorResponse

router = APIRouter()
question_generating_service = QuestionGeneratingService()


@router.post(
    "/generate-questions",
    response_model=ResponseModel,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Generate questions based on input",
    description="This endpoint generates questions based on the provided content or uploaded file.",
)
async def generate_questions(
    file: Union[UploadFile, None] = File(
        None, description="An optional file to upload (PDF or DOCX)"
    ),
    subject: Optional[str] = Form(None, description="The subject of the content"),
    content: Optional[str] = Form(
        None, description="The text content to generate questions from"
    ),
    difficulty: Optional[str] = Form(
        None, description="The difficulty level of the questions"
    ),
    q_type_mcq_single: Optional[int] = Form(
        None, description="Number of single-answer MCQ questions"
    ),
    q_type_mcq_multiple: Optional[int] = Form(
        None, description="Number of multiple-answer MCQ questions"
    ),
    q_type_descriptive: Optional[int] = Form(
        None, description="Number of descriptive questions"
    ),
    q_type_fill_in_the_blanks: Optional[int] = Form(
        None, description="Number of fill-in-the-blanks questions"
    ),
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
                detail="Unsupported file type. Please upload a PDF, DOC, or DOCX file.",
            )
    try:
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
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=str(e))
