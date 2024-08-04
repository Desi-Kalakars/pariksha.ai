import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app
from app.services.question_service import QuestionGeneratingService

client = TestClient(app)


@pytest.fixture
def mock_question_service():
    with patch.object(
        QuestionGeneratingService, "generate_questions", new_callable=AsyncMock
    ) as mock_service:
        yield mock_service


def test_generate_questions_with_content_all_types(mock_question_service):
    mock_question_service.return_value = {
        "questions": [
            {
                "question_text": "What is the capital of France?",
                "question_type": "single_answer_mcq",
                "choices": [
                    {"text": "Paris", "is_correct": True},
                    {"text": "London", "is_correct": False},
                    {"text": "Berlin", "is_correct": False},
                    {"text": "Madrid", "is_correct": False},
                ],
                "correct_answer": None,
            },
            {
                "question_text": "Which of the following are programming languages?",
                "question_type": "multiple_answer_mcq",
                "choices": [
                    {"text": "Python", "is_correct": True},
                    {"text": "Java", "is_correct": True},
                    {"text": "HTML", "is_correct": False},
                    {"text": "CSS", "is_correct": False},
                ],
                "correct_answer": None,
            },
            {
                "question_text": "Explain the concept of polymorphism in OOP.",
                "question_type": "descriptive",
                "choices": None,
                "correct_answer": "Polymorphism allows objects to be treated as instances of their parent class rather than their actual class.",
            },
            {
                "question_text": "Fill in the blank: The capital of Japan is _____?",
                "question_type": "fill_in_the_blanks",
                "choices": None,
                "correct_answer": "Tokyo",
            },
        ]
    }

    response = client.post(
        "/api/generate-questions",
        data={
            "content": "This is a test content for generating questions.",
            "subject": "General Knowledge",
            "difficulty": "medium",
            "q_type_mcq_single": 1,
            "q_type_mcq_multiple": 1,
            "q_type_descriptive": 1,
            "q_type_fill_in_the_blanks": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    questions = response.json()["questions"]
    assert len(questions) == 4
    assert questions[0]["question_type"] == "single_answer_mcq"
    assert questions[1]["question_type"] == "multiple_answer_mcq"
    assert questions[2]["question_type"] == "descriptive"
    assert questions[3]["question_type"] == "fill_in_the_blanks"


def test_generate_questions_with_file_all_types(mock_question_service):
    mock_question_service.return_value = {
        "questions": [
            {
                "question_text": "What is the capital of Germany?",
                "question_type": "single_answer_mcq",
                "choices": [
                    {"text": "Berlin", "is_correct": True},
                    {"text": "Paris", "is_correct": False},
                    {"text": "Rome", "is_correct": False},
                    {"text": "Madrid", "is_correct": False},
                ],
                "correct_answer": None,
            },
            {
                "question_text": "Which of the following are fruits?",
                "question_type": "multiple_answer_mcq",
                "choices": [
                    {"text": "Apple", "is_correct": True},
                    {"text": "Carrot", "is_correct": False},
                    {"text": "Banana", "is_correct": True},
                    {"text": "Broccoli", "is_correct": False},
                ],
                "correct_answer": None,
            },
            {
                "question_text": "Describe the process of photosynthesis.",
                "question_type": "descriptive",
                "choices": None,
                "correct_answer": "Photosynthesis is the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water.",
            },
            {
                "question_text": "Fill in the blank: The largest planet in our solar system is _____?",
                "question_type": "fill_in_the_blanks",
                "choices": None,
                "correct_answer": "Jupiter",
            },
        ]
    }

    file_content = b"Dummy content for file"
    response = client.post(
        "/api/generate-questions",
        files={"file": ("test.docx", file_content)},
        data={
            "subject": "General Knowledge",
            "difficulty": "medium",
            "q_type_mcq_single": 1,
            "q_type_mcq_multiple": 1,
            "q_type_descriptive": 1,
            "q_type_fill_in_the_blanks": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    questions = response.json()["questions"]
    assert len(questions) == 4
    assert questions[0]["question_type"] == "single_answer_mcq"
    assert questions[1]["question_type"] == "multiple_answer_mcq"
    assert questions[2]["question_type"] == "descriptive"
    assert questions[3]["question_type"] == "fill_in_the_blanks"


def test_generate_questions_with_content_no_file(mock_question_service):
    mock_question_service.return_value = {
        "questions": [
            {
                "question_text": "What is the capital of Italy?",
                "question_type": "single_answer_mcq",
                "choices": [
                    {"text": "Rome", "is_correct": True},
                    {"text": "Paris", "is_correct": False},
                    {"text": "Berlin", "is_correct": False},
                    {"text": "Madrid", "is_correct": False},
                ],
                "correct_answer": None,
            },
        ]
    }

    response = client.post(
        "/api/generate-questions",
        data={
            "content": "This is a test content for generating a single question.",
            "subject": "Geography",
            "difficulty": "easy",
            "q_type_mcq_single": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    questions = response.json()["questions"]
    assert len(questions) == 1
    assert questions[0]["question_type"] == "single_answer_mcq"


def test_generate_questions_with_file_no_content(mock_question_service):
    mock_question_service.return_value = {
        "questions": [
            {
                "question_text": "What is the capital of Spain?",
                "question_type": "single_answer_mcq",
                "choices": [
                    {"text": "Madrid", "is_correct": True},
                    {"text": "Paris", "is_correct": False},
                    {"text": "Berlin", "is_correct": False},
                    {"text": "Rome", "is_correct": False},
                ],
                "correct_answer": None,
            },
        ]
    }

    file_content = b"Dummy content for file"
    response = client.post(
        "/api/generate-questions",
        files={"file": ("test.docx", file_content)},
        data={
            "subject": "Geography",
            "difficulty": "easy",
            "q_type_mcq_single": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    questions = response.json()["questions"]
    assert len(questions) == 1
    assert questions[0]["question_type"] == "single_answer_mcq"


def test_generate_questions_with_all_fields(mock_question_service):
    mock_question_service.return_value = {
        "questions": [
            {
                "question_text": "Describe the process of mitosis.",
                "question_type": "descriptive",
                "choices": None,
                "correct_answer": "Mitosis is the process of cell division in eukaryotic cells.",
            },
        ]
    }

    file_content = b"Dummy content for file"
    response = client.post(
        "/api/generate-questions",
        files={"file": ("test.docx", file_content)},
        data={
            "content": "This is additional content.",
            "subject": "Biology",
            "difficulty": "hard",
            "q_type_descriptive": 1,
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    questions = response.json()["questions"]
    assert len(questions) == 1
    assert questions[0]["question_type"] == "descriptive"


def test_missing_content_or_file(mock_question_service):
    response = client.post("/api/generate-questions")

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Either a file must be uploaded or content must be provided."
    )


def test_unsupported_file_type(mock_question_service):
    file_content = b"Dummy content for file"
    response = client.post(
        "/api/generate-questions",
        files={"file": ("test.txt", file_content)},
        data={
            "subject": "History",
            "difficulty": "hard",
            "q_type_mcq_single": 1,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Unsupported file type. Please upload a PDF, DOC, or DOCX file."
    )


def test_no_question_types_provided(mock_question_service):
    response = client.post(
        "/api/generate-questions",
        data={
            "content": "This is a test content for generating questions.",
            "subject": "Geography",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "At least one question type must be provided and greater than zero."
    )


@patch.object(QuestionGeneratingService, "generate_questions", new_callable=AsyncMock)
def test_generate_questions_internal_server_error(mock_service):
    # Simulate an internal server error
    mock_service.side_effect = Exception("Internal server error")

    response = client.post(
        "/api/generate-questions",
        data={
            "content": "This is a test content for generating questions.",
            "subject": "General Knowledge",
            "difficulty": "medium",
            "q_type_mcq_single": 1,
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
