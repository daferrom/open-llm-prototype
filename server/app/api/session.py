from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.models import ChatSession
from app.db.deps import get_db

router = APIRouter()

@router.post("/session")
def create_session(db: Session = Depends(get_db)):
    new_session = ChatSession()
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"session_id": new_session.id}
