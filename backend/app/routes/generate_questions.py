from fastapi import File, Form, UploadFile, APIRouter, HTTPException
from typing import  Optional
from models.questions_response import ResponseModel

router = APIRouter()

@router.post("/generate-questions",response_model=ResponseModel)
async def generate_questions(
    file: Optional[UploadFile] = File(None),
    subject: str = Form(...),
    content: str = Form(...),
    q_type_mcq_single: int = Form(...),
    q_type_mcq_multiple: int = Form(...),
    q_type_descriptive: int = Form(...),
    q_type_fill_in_the_blanks: int = Form(...),
):
    # Validate that at least one question type is greater than zero
    if (
        q_type_mcq_single <= 0 and
        q_type_mcq_multiple <= 0 and
        q_type_descriptive <= 0 and
        q_type_fill_in_the_blanks <= 0
    ):
        raise HTTPException(status_code=400, detail="At least one question type must be greater than zero.")

    # Validate file type if a file is provided
    if file:
        valid_extensions = {"pdf", "doc", "docx"}
        filename = file.filename
        file_extension = filename.split(".")[-1].lower()

        if file_extension not in valid_extensions:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF, DOC, or DOCX file.")

        # Handle file upload
        # e.g., process the file, extract data, etc.
    else:
        # Handle case when no file is uploaded
        # e.g., process the content directly, etc.
        pass


    # Placeholder logic to generate questions
    questions = {
        "mcq_single": ["question1", "question2"] if q_type_mcq_single > 0 else [],
        "mcq_multiple": ["question1", "question2"] if q_type_mcq_multiple > 0 else [],
        "fill_in_the_blanks": ["question1", "question2"] if q_type_fill_in_the_blanks > 0 else [],
        "descriptive": ["question1", "question2"] if q_type_descriptive > 0 else []
    }

    # Return the response
    return {
        "status": "success",
        "questions": questions
    }
