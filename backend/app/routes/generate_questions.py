from fastapi import File, Form, UploadFile, APIRouter, HTTPException
from typing import  Optional

router = APIRouter()

@router.post("/generate-questions")
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
    if not any([q_type_mcq_single, q_type_mcq_multiple, q_type_descriptive, q_type_fill_in_the_blanks]):
        raise HTTPException(status_code=400, detail="At least one question type must be greater than zero.")

    if file:
        # Handle file upload
        # e.g., process the file, extract data, etc.
        pass
    else:
        # Handle case when no file is uploaded
        # e.g., process the content directly, etc.
        pass

    # Further processing based on subject, content, and question types
    # ...

    return {
        "message": "Questions generated successfully",
        "file": file.filename if file else None,
        "subject": subject,
        "content": content,
        "q_type_mcq_single": q_type_mcq_single,
        "q_type_mcq_multiple": q_type_mcq_multiple,
        "q_type_descriptive": q_type_descriptive,
        "q_type_fill_in_the_blanks": q_type_fill_in_the_blanks
    }