from fastapi import FastAPI
from routes.generate_questions import router as generate_questions
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Question Generation API",
    description="An API for generating questions based on provided content or files",
    version="1.0.0",
)

app.include_router(generate_questions, prefix="/api")


@app.get(
    "/",
    summary="Root endpoint",
    description="Returns a welcome message",
    response_model=dict,
)
async def root():
    return {"message": "Welcome to the Question Generation API"}
