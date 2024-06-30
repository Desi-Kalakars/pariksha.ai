from fastapi import FastAPI
from routes.ping import router as ping_router

app = FastAPI()

app.include_router(ping_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Pariksha.ai!"}
