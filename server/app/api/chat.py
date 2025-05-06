from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from server.app.db.db import SessionLocal
from app.services.rag_engine import query_index ,query_with_history
from app.db.models import ChatSession

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: int
    top_k: Optional[int] = 5
    response_mode: Optional[str] = "compact"
    temperature: Optional[float] = 0.5

def get_db():
    """
    Dependency to get the database session.
    This function can be used in route handlers to access the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/chat")
async def chat(request: ChatRequest , db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter_by(id=request.session_id).first()
    
    if not session: 
        raise HTTPException(status_code=404, detail="Session not found")
    """
    Handles the chat endpoint for processing user queries.

    Endpoint:
        POST /chat

    Request Body:
        request (ChatRequest): The request object containing the user's query and optional parameters.
        - query (str): The user's query.
        - top_k (int, optional): The number of top results to return. Default is 5.
        - response_mode (str, optional): The mode of response. Default is "compact", ALLowed "tree_summarize" and "refine" too.
                check https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes/ fro more details.
        - temperature (float, optional): The temperature for the response. Default is 0.5.

    Returns:
        dict: A dictionary containing the response from the query index.

    Raises:
        HTTPException: If an error occurs during processing, a 500 status code is returned with the error details.
    """

    try:
        response = query_with_history(
            user_query=request.query,
            session_id=request.session_id,
            db=db,
            top_k=request.top_k,
            response_mode=request.response_mode,
            temperature=request.temperature
    ***REMOVED***

        return { "response": response }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))