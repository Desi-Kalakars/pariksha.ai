import os
from fastapi import UploadFile
from utils.file_readers import read_docx, read_pdf
from langchain_google_genai import ChatGoogleGenerativeAI


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

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

        # Create a message with the input text
        messages = [
            (
                "system",
                """You are an excellent teacher's assistant who reads a topic thoroughly understands it,
                  finds the key elements that are necessary to be understood and creates a test for students.
                  User is a teacher, he/she will give you subject, content and types of question and you have to reply in JSON format.""",
            ),
            (
                "user",
                f"""subject: {subject} content: {content} {document_data} generate a test for students which contains {q_type_mcq_single} single answer mcq questions
                {q_type_mcq_multiple} multiple answer mcq questions {q_type_descriptive} descriptive answer questions and 
                {q_type_fill_in_the_blanks} fill in the blanks questions""",
            ),
        ]
        ai_msg = llm.invoke(messages)

        # Extract and return the text content of the response
        return ai_msg.content
