from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from src.index_getter.index_getter import get_or_create_index
from src.config.config import CHROMA_DB_PATH, CODE_DB_COLLECTION , SPACE_KEY_ENV_APP
from app.db.models import Message
from llama_index.core.chat_engine.types import ChatMessage

from sqlalchemy.orm import Session

index : VectorStoreIndex = get_or_create_index(CHROMA_DB_PATH, CODE_DB_COLLECTION, SPACE_KEY_ENV_APP)

def get_chat_history(session_id: int, db: Session) -> list[ChatMessage]:
    messages = db.query(Message).filter_by(session_id=session_id).order_by(Message.timestamp).all()
    return [ChatMessage(role=msg.role, content=msg.content) for msg in messages]


def save_message(session_id: int, role: str, content: str, db: Session):
    msg = Message(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

def query_index(user_query: str , top_k: int, response_mode: str, temperature: float) -> str:
    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=temperature),
            similarity_top_k=top_k,
            response_mode=response_mode,
    ***REMOVED***

    response = query_engine.query(user_query)

    return str(response)

def query_with_history(user_query: str, session_id: int, db: Session, top_k=8, response_mode="compact", temperature=0.5) -> str:
    chat_history = get_chat_history(session_id, db)

    chat_engine = index.as_chat_engine(
        llm=OpenAI(model="gpt-4", temperature=temperature),
        chat_mode="context",
        chat_history=chat_history,
        system_prompt="You are a helpful assistant for understanding code projects based on the embedded code and documentation the index",
        similarity_top_k=top_k,
        response_mode=response_mode
    )

    response = chat_engine.chat(user_query)


    # Persist conversation
    save_message(session_id, "user", user_query, db)
    save_message(session_id, "assistant", response.response, db)

    return str(response.response)
