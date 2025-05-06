import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat , session
from dotenv import load_dotenv
from pathlib import Path

from server.app.db import models
from app.db.db import engine


# Load .env from root
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    if not os.path.exists("server/app/db/db_initializated.flag"):
        models.Base.metadata.create_all(bind=engine)
        with open("server/app/db/db_initializated.flag", "w") as f:
            f.write("Database initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000/"], # To Allow all origin requests use ["*"] only on local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(session.router)