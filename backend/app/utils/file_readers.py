import io
from typing import Union

import PyPDF2
from docx import Document
from fastapi import UploadFile


async def read_pdf(file: UploadFile) -> Union[str, None]:
    file_content = await file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    content = ""
    for page in pdf_reader.pages:
        content += page.extract_text()
    return content.strip()


async def read_docx(file: UploadFile) -> Union[str, None]:
    content = ""
    doc = Document(io.BytesIO(await file.read()))

    for paragraph in doc.paragraphs:
        content += paragraph.text
    return content.strip()
