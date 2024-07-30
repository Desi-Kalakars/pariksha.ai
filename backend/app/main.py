from fastapi import FastAPI
from routes.ping import router as ping_router
from routes.generate_questions import router as generate_questions
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(ping_router)
app.include_router(generate_questions,prefix='/api')

@app.get("/")
async def root():
    return {"message": "Welcome to Pariksha.ai!"}
