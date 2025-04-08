import sys
from pathlib import Path
import json
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex



# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from client_api_ai.prompt_templates import prompt_templates
from client_api_ai import client_api_ai
from llama_idx_prototype.llama_idx_prototype import get_llama_idx_query, set_llm_config, set_tracer_phoenix_config
from docs_loader.confluence_docs_loader import set_vector_store

from utils import env_utils , access_files_util, response_processors

#INPUT diff file

# Get workspace directory
workspace = env_utils.get_workspace()
print("Workspace:", workspace)

# Set diff file path
diff_file_path = workspace / "diff.txt"

# Open and read the .diff file as a text
diff_content_read = access_files_util.read_file(diff_file_path)

print("Diff_content",diff_content_read )

with open("api_ai_response.json", "r", encoding="utf-8") as file:
    doctype_validation = json.load(file)

#TODO: Remove when confluence publish directs the right main DocType to publish
doc_type = doctype_validation["documentation_type"]

print("DOC TYPE", doc_type)

print("Diff_content",diff_content_read )

print("Available keys in prompt_templates:", prompt_templates.keys())


if __name__ == "__main__":
    # Load .env only on local execution
    env_utils.load_env_if_local()

    HF_API_TOKEN = os.getenv("HF_API_TOKEN")
    MODEL_NAME= "Qwen/Qwen2.5-Coder-32B-Instruct"

    # For Checking APi behavior remote and response
    set_tracer_phoenix_config()

    # Set prompt for generate Documentation per with the respective Doctype template
    prompt_to_send = prompt_templates[doc_type].format(diff_content=diff_content_read)

    llm_hf = set_llm_config(model_name=MODEL_NAME, temp=0.7, max_tokens=500, hf_api_token=HF_API_TOKEN)

    vector_store = set_vector_store()
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    xhtml_doc_response = get_llama_idx_query(index, prompt_to_send, llm_hf)
    print("XHTML RESPONSE", xhtml_doc_response)

    with open("summary.xhtml", "w") as f:
        f.write(xhtml_doc_response.response) ## Write the generated doc in xhtml

    print(f"XHTML Documentation by DOC TYPE {doc_type} : ", xhtml_doc_response)
