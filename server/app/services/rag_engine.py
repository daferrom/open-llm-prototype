from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from src.index_getter.index_getter import get_or_create_index
from src.config.config import CHROMA_DB_PATH, CODE_DB_COLLECTION , SPACE_KEY_ENV_APP

index : VectorStoreIndex = get_or_create_index(CHROMA_DB_PATH, CODE_DB_COLLECTION, SPACE_KEY_ENV_APP)

def query_index(user_query: str , top_k: int, response_mode: str, temperature: str) -> str:
    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=temperature),
            similarity_top_k=top_k,
            response_mode=response_mode,
    ***REMOVED***

    response = query_engine.query(user_query)

    return str(response)