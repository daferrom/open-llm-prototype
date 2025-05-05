from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat
from dotenv import load_dotenv
from pathlib import Path


# Load .env from root
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000/"], # To Allow all origin requests use ["*"] only on local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)