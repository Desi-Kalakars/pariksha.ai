import os, json
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
                """You are an excellent teacher's assistant who reads a topic thoroughly, understands it,
            finds the key elements that are necessary to be understood, and creates a test for students.
            You will be given a subject, content, and types of questions. Your response should be in the following JSON format:

            {
              "questions": [
                {
                  "question_text": "What is the capital of France?", // The actual question being asked
                  "question_type": "single_answer_mcq", // Type of question: 'single_answer_mcq', 'multiple_answer_mcq', 'descriptive', or 'fill_in_the_blanks'
                  "choices": [ // Array of choices for MCQ questions, null for other types
                    {
                      "text": "Paris", // Text of the choice
                      "is_correct": true // Boolean indicating if this choice is correct
                    },
                    {
                      "text": "London",
                      "is_correct": false
                    }
                  ],
                  "correct_answer": null // Correct answer for non-MCQ questions, null for MCQs
                }
              ]
            }

            Ensure that your response strictly adheres to this JSON structure and don't add ```json in the beginning.""",
            ),
            (
                "user",
                f"""Subject: {subject}
            Content: {content} {document_data}
            Generate a test for students which contains:
            - {q_type_mcq_single} single answer MCQ questions
            - {q_type_mcq_multiple} multiple answer MCQ questions
            - {q_type_descriptive} descriptive answer questions
            - {q_type_fill_in_the_blanks} fill in the blanks questions
            Provide your response in the JSON format specified.""",
            ),
        ]
        ai_msg = (llm.invoke(messages)).content

        print(ai_msg)

        # Extract and return the text content of the response
        return json.loads(ai_msg)
