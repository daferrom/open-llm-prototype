import llama_index.core
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.readers.confluence import ConfluenceReader
import sys
from pathlib import Path
***REMOVED***
import json

import llama_index
import os
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import VectorStoreIndex
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI


import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from client_api_ai.prompt_templates import prompt_templates
from utils ***REMOVED***ad_file_by_env
from config.config import PAGE_PARENTS_IDS , SPACE_ID


from utils import env_utils

def set_tracer_phoenix_config():
    # PHOENIX Config for Tr
    PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
    
    llama_index.core.set_global_handler(
        "arize_phoenix",
        endpoint="https://llamatrace.com/v1/traces"
    )


def set_confluence_loader():
    loader = ConfluenceReader(
        base_url = BASE_URL,
        user_name = USER,
        password = CONFLUENCE_READER_TOKEN
    )
    return loader

def load_docs(loader, space_key):
    return loader.load_data(space_key=space_key, include_attachments=False)

def convert_docs_to_llama_idx_objects(docs):
    return [Document(text=doc.text, metadata=doc.metadata) for doc in docs]

def set_vector_store():
    # Set db config
    db = chromadb.PersistentClient(path="./doc_chroma_db")
    chroma_collection = db.get_or_create_collection("confluence_docs")
    return ChromaVectorStore(chroma_collection=chroma_collection)

# set an index based on the vector store of embeddings
def set_index(model_name_for_embedd):
    vector_store = set_vector_store()
    embed_model = HuggingFaceEmbedding(model_name=model_name_for_embedd)
    return VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model) # return index

def set_llm_config(model_name, temp, max_tokens, hf_api_token):
        return HuggingFaceInferenceAPI(
            model_name=model_name,
            temperature=temp,
            max_tokens=max_tokens,
            token=hf_api_token,
***REMOVED***

def get_llama_idx_query(index, prompt_query, llm):
        print(f"🦙🦙🦙🦙🦙🦙🦙🦙🦙 Requesting response using llama idx query engine with model: {llm.model_name} 🦙🦙🦙🦙🦙🦙🦙🦙🦙")
        query_engine = index.as_query_engine(
            llm=llm,
            response_mode="tree_summarize",
***REMOVED***
        return query_engine.query(prompt_query)

if __name__ == "__main__":

    # Load diff.txt content
    diff_content_loaded = read_file_by_env.load_diff_content("diff.txt")

    # Load .env only on local execution
    env_utils.load_env_if_local()

    HF_API_TOKEN = os.getenv("MY_HF_TOKEN")
    CONFLUENCE_READER_TOKEN= os.getenv("CONFLUENCE_TOKEN_3")
    USER = os.getenv("MY_EMAIL")
    SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
    OPENAI_API_KEY = os.getenv("GH_GPT4_API_KEY")
    BASE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki"
    MODEL_NAME= "Qwen/Qwen2.5-Coder-32B-Instruct"

    print("MY DIFF CONTENT", diff_content_loaded)

    set_tracer_phoenix_config()

    # Load Confluence Documents
    loader = set_confluence_loader()
    loaded_docs = load_docs(loader, SPACE_KEY)
    documents = convert_docs_to_llama_idx_objects(loaded_docs)


    # TODO: CREATE OAUTH 2.0 token service autorization
    # TODO: Implement fetching Data by batches or pagination to execute pipeline on paralell async


    # TODO: Set a backend database
    vector_store = set_vector_store()

    # Create the pipeline with transaformations
    # TODO: TEST WITH these models: "sentence-transformers/all-mpnet-base-v2" (Better for english). "BAAI/bge-base-en-v1.5" and  (More Precision).

    # TODO: double ckeck if the pipeline is totally replaced by lines of # Create index from our vector store and embeddings:
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=256, chunk_overlap=50),
            HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),
        ],
        vector_store=vector_store,
    )

    pipeline.run(documents=documents)

    # Create index from our vector store and embeddings:
    index = set_index(model_name_for_embedd="BAAI/bge-small-en-v1.5")


    # TODO: This Would be enhacement Querying a VectorStoreIndex with prompts and LLMs
    # TODO: Test with as_retriever
    # USE this as_retriever
    # Returns a list of nodes(Documents) NodesWithScore


    llm_hf = set_llm_config(model_name=MODEL_NAME, temp=0.7, max_tokens=500, hf_api_token=HF_API_TOKEN)

    # FaithfulnessEvaluator
    evaluator = FaithfulnessEvaluator(llm=llm_hf)

    doct_type_val_prompt = prompt_templates["DOCTYPE_PROMPT_VALIDATOR"].format(diff_content=diff_content_loaded)
    doctype_val_response = get_llama_idx_query(index, doct_type_val_prompt, llm_hf)

    # TODO: Visualize evaluations
    eval_result = evaluator.evaluate_response(response=doctype_val_response)
    eval_result.passing

    # Process string response to json and save it as api_ai_response.json

    # 🔹 Delete delimiters```json ... ``` on the response
    clean_json = re.sub(r"^```json|\n```$", "", doctype_val_response.response).strip()

    # 🔹 Convert to Dictionary
    data = json.loads(clean_json)

    # Write the response to a JSON file
    with open("api_ai_response.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # Print the response
    print("... API AI response DOC type validation per diff ✅:", json.dumps(data, ensure_ascii=False, indent=4))


