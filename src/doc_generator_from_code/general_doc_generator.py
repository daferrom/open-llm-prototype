import os
import sys
import json

import torch
from transformers import AutoTokenizer
from pathlib import Path
from llama_index.core.embeddings import  BaseEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import CodeSplitter
from llama_index.llms.openai import OpenAI
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import ServiceContext
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.core import Settings

from pydantic import PrivateAttr
from typing import Any

from tree_sitter import Parser
from tree_sitter_language_pack import get_parser

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils, response_processors
from client_api_ai.prompt_templates import prompt_templates
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY
from docs_loader.code_loader import load_code_file_as_docs
from doc_processors.code_splitter import split_docs_by_prog_lang


from transformers import AutoTokenizer, T5EncoderModel
from typing import Any
from pydantic import PrivateAttr
import torch

class CodeT5Embedder(BaseEmbedding):
    _tokenizer: Any = PrivateAttr()
    _model: Any = PrivateAttr()

    def __init__(self, model_name="Salesforce/codet5-base"):
        super().__init__()
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = T5EncoderModel.from_pretrained(model_name)
        self._model.eval()

    def _get_text_embedding(self, text: str) -> list[float]:
        with torch.no_grad():
            inputs = self._tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = self._model(**inputs)
            last_hidden = outputs.last_hidden_state
            pooled = last_hidden.mean(dim=1).squeeze().numpy()
        return pooled.tolist()

    def _get_query_embedding(self, query: str) -> list[float]:
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)

def set_vector_store_code_embs():
    # Set db config
    db = chromadb.PersistentClient(path="./code_chroma_code_t5_db")
    chroma_collection = db.get_or_create_collection("code_docs")
    return ChromaVectorStore(chroma_collection=chroma_collection)


if __name__ == "__main__":
    # Load .env only on local execution
    env_utils.load_env_if_local()

    # code_dir = "./src/code_repos"

    # Config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Sabrine shared OPEN API KEY
    assert OPENAI_API_KEY, "OPEN AI MISSING API KEY"

    # Load code files
    print("📂 Loading files from code repository...")


    documents = load_code_file_as_docs(CODE_DIRECTORY, FILE_EXTS_TO_LOAD)

    nodes =split_docs_by_prog_lang(documents)

    print("🔍 Generating embeddings and creating index...")
    # embed_model = HuggingFaceEmbedding(model_name="microsoft/codebert-base")

    Settings.embed_model = CodeT5Embedder()

    # Create vector index
    vector_store = set_vector_store_code_embs()

    # TODO: THIS CAN BE REPLACED FOR IngestionPipeline
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(nodes, storage_context=storage_context)

    # make query
    print("🤖 Ready for answering question about your code !")
    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=0.5),
            response_mode="compact",
    ***REMOVED***

    # example
    # input_query = "Based on the code structure, function and class names, what appears to be the purpose of this project?"

    # TODO: Consider to separate templates cor each section of th initial DOcumentation of a project.
    input_query = prompt_templates["BASE_DOCUMENTATION_V2"]
    response = query_engine.query(input_query)
    print(dir(response))
    print("=================================")
    print("raw response", response)
    print("TYPE response", type(response))

    cleaned_response = response_processors.clean_xml_delimiters(response.response)

    # Write the response to a JSON file
    with open("base_documentation.xhtml", "w") as f:
        f.write(cleaned_response) ## Write the generated doc in xhtml


    print(f"Question : {input_query}")
    print("\nResponse:")
    print("...GPT-4 response cleaned ✅:", cleaned_response)

