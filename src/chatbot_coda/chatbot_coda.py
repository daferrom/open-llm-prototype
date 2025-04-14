import sys
import os
from pathlib import Path



# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llama_idx_prototype.llama_idx_prototype import  set_index, set_llm_config, get_llama_idx_query_refined
from config.config import MODEL_FOR_EMBEDDINGS, MODEL_NAME
from utils import env_utils

if __name__ == "__main__":

    # Load .env only on local execution
    env_utils.load_env_if_local()

    HF_API_TOKEN = os.getenv("HF_API_TOKEN")

    index = set_index(model_name_for_embedd=MODEL_FOR_EMBEDDINGS)

    llm_hf = set_llm_config(model_name=MODEL_NAME, temp=0.7, max_tokens=500, hf_api_token=HF_API_TOKEN)

    print("🤖\n Terminal CoDa Chatbot ready to chat (type 'exit' to end) 🤖\n")

    # Bucle de conversación
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 ¡See you later 🐊 !")
            break

        response = get_llama_idx_query_refined(index, user_input, llm_hf)
        print(f"🤖 CoDA Bot: {response}\n")

