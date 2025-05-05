from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag_engine import query_index

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    response_mode: Optional[str] = "compact"
    temperature: Optional[float] = 0.5



@router.post("/chat")
async def chat(request: ChatRequest):
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
        response = query_index(
            user_query=request.query,
            top_k=request.top_k,
            response_mode=request.response_mode,
            temperature=request.temperature
    ***REMOVED***

        return { "response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))