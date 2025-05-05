import os
import sys

from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY, CONFLUENCE_API_BASE_URL
from docs_loader.code_loader import load_code_file_as_docs
from doc_processors.code_splitter import split_docs_by_prog_lang
from code_embedders.code_t5_embedder import CodeT5Embedder
from vector_store_setters.vector_store_code_embds_setter import set_vector_store_code_embs
from docs_loader.confluence_docs_loader import set_confluence_loader ,load_confluence_docs_as_llama_idx_objs
from llama_index.readers.confluence import ConfluenceReader
from confluence_service.pages_service import get_pages_in_space
from confluence_service.spaces_service import get_spaces

def create_idx():
    # Load .env only on local execution
    env_utils.load_env_if_local()

    # Config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # OPEN API KEY shared by Sabrine

    # Open AI key validation
    assert OPENAI_API_KEY, "OPEN AI MISSING API KEY"

    Settings.embed_model = CodeT5Embedder()

    documents = load_code_file_as_docs(CODE_DIRECTORY, FILE_EXTS_TO_LOAD)

    nodes =split_docs_by_prog_lang(documents)

    print("🔍 Generating embeddings and creating index...")


    chroma_db_path = "./src/data/vector_store/code_chroma_code_t5_db/"
    db_collection_name = "code_docs"

    # Create vector store
    vector_store = set_vector_store_code_embs(path=chroma_db_path, collection=db_collection_name)

    # # TODO: THIS CAN BE REPLACED FOR IngestionPipeline
    # Set a disk persistent storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create the initial index
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    
    index.storage_context.persist(persist_dir="./src/data/vector_store/index_metadata/")
    
    return index

if __name__ == "__main__":
    print("..running create index module")
