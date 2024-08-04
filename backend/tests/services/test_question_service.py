import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import UploadFile
from app.services.question_service import QuestionGeneratingService


@pytest.fixture
def question_service():
    return QuestionGeneratingService()


@pytest.mark.asyncio
async def test_generate_questions(question_service):
    # Mock file and LLM response
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.pdf"

    mock_llm_response = MagicMock()
    mock_llm_response.content = """
    {
      "questions": [
        {
          "question_text": "What is the capital of France?",
          "question_type": "single_answer_mcq",
          "choices": [
            {"text": "Paris", "is_correct": true},
            {"text": "London", "is_correct": false}
          ],
          "correct_answer": null
        }
      ]
    }
    """

    with patch(
        "app.services.question_service.read_pdf", new_callable=AsyncMock
    ) as mock_read_pdf, patch(
        "app.services.question_service.ChatGoogleGenerativeAI"
    ) as mock_llm:

        mock_read_pdf.return_value = "Mocked PDF content"
        mock_llm.return_value.invoke.return_value = mock_llm_response

        result = await question_service.generate_questions(
            file=mock_file,
            subject="History",
            content="Test content",
            difficulty="Medium",
            q_type_mcq_single=1,
            q_type_mcq_multiple=0,
            q_type_descriptive=0,
            q_type_fill_in_the_blanks=0,
        )

    assert isinstance(result, dict)
    assert "questions" in result
    assert len(result["questions"]) == 1
    assert result["questions"][0]["question_text"] == "What is the capital of France?"


@pytest.mark.asyncio
async def test_read_file_content_pdf(question_service):
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.pdf"

    with patch(
        "app.services.question_service.read_pdf", new_callable=AsyncMock
    ) as mock_read_pdf:
        mock_read_pdf.return_value = "Mocked PDF content"
        result = await question_service._read_file_content(mock_file)

    assert result == "Mocked PDF content"


@pytest.mark.asyncio
async def test_read_file_content_docx(question_service):
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.docx"

    with patch(
        "app.services.question_service.read_docx", new_callable=AsyncMock
    ) as mock_read_docx:
        mock_read_docx.return_value = "Mocked DOCX content"
        result = await question_service._read_file_content(mock_file)

    assert result == "Mocked DOCX content"


@pytest.mark.asyncio
async def test_read_file_content_unsupported(question_service):
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.txt"

    with pytest.raises(ValueError, match="Unsupported file type"):
        await question_service._read_file_content(mock_file)


def test_create_prompt(question_service):
    result = question_service._create_prompt(
        subject="Math",
        content="Algebra basics",
        difficulty="Easy",
        document_data="Additional content",
        q_type_mcq_single=2,
        q_type_mcq_multiple=1,
        q_type_descriptive=1,
        q_type_fill_in_the_blanks=1,
    )

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0][0] == "system"
    assert result[1][0] == "user"
    assert "Math" in result[1][1]
    assert "Easy" in result[1][1]
    assert "Algebra basics" in result[1][1]
    assert "Additional content" in result[1][1]


def test_get_system_instruction(question_service):
    result = question_service._get_system_instruction()
    assert isinstance(result, str)
    assert "You are an excellent teacher's assistant" in result
    assert "JSON format" in result


def test_get_user_query(question_service):
    result = question_service._get_user_query(
        subject="Science",
        content="Solar System",
        difficulty="Medium",
        document_data="Extra info about planets",
        q_type_mcq_single=3,
        q_type_mcq_multiple=2,
        q_type_descriptive=1,
        q_type_fill_in_the_blanks=1,
    )

    assert isinstance(result, str)
    assert "Subject: Science" in result
    assert "Difficulty: Medium" in result
    assert "Content: Solar System Extra info about planets" in result
    assert "3 single answer MCQ questions" in result
    assert "2 multiple answer MCQ questions" in result
    assert "1 descriptive answer questions" in result
    assert "1 fill in the blanks questions" in result
