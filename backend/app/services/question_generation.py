import os
from fastapi import UploadFile
from utils.file_readers import read_docx, read_pdf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage


class QuestionGeneratingService:

    def __init__(self):
        self.llm_key = os.environ.get("GEMINI_API_KEY")

    async def generate_questions(
        self,
        file: UploadFile,
        subject: str,
        content: str,
        q_type_mcq_single: int,
        q_type_mcq_multiple: int,
        q_type_descriptive: int,
        q_type_fill_in_the_blanks: int,
    ):
        document_data = None
        # Determine file type and read content
        if file:
            if file.filename.endswith(".pdf"):
                document_data = await read_pdf(file)
            elif file.filename.endswith(".docx"):
                document_data = await read_docx(file)

        model = ChatGoogleGenerativeAI(model="gemini-pro")

        # Create a message with the input text
        message = HumanMessage(content=document_data)

        # Generate a response
        response = model.invoke([message])

        # Extract and return the text content of the response
        return response.content
