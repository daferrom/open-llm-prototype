import sys
import os
from pathlib import Path
from llama_index.llms.openai import OpenAI



# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llama_idx_prototype.llama_idx_prototype import  set_index, set_llm_config, get_llama_idx_query_refined
from config.config import CHROMA_DB_PATH ,CODE_DB_COLLECTION
from utils import env_utils
from index_getter.index_getter import get_or_create_index

if __name__ == "__main__":

    # Load .env only on local execution
    env_utils.load_env_if_local()


    index = get_or_create_index(CHROMA_DB_PATH, CODE_DB_COLLECTION)

    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=0.5),
            response_mode="compact",
    ***REMOVED***


    print("🤖\n Terminal env_monitor_app Chatbot ready to chat (type 'exit' to end) 🤖\n")

    # Bucle de conversación
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 ¡See you later 🐊 !")
            break

        response = query_engine.query(user_input)
        print(f"🤖 CoDA Bot: {response}\n")

