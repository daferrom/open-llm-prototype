import os
import sys
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from vector_store_setters.vector_store_code_embds_setter import set_vector_store_code_embs
from code_embedders.code_t5_embedder import CodeT5Embedder
from llama_index.core import Settings
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY, CHROMA_DB_PATH, CODE_DB_COLLECTION, INDEX_DIR, SPACE_KEY_ENV_APP

from docs_loader.nodes_loader import load_nodes_from_confluence_space
from docs_loader.nodes_loader import load_code_nodes


# Function to create an index from code and confluence docs

def create_idx_from_docs_and_code(space_key=None, code_directory=None, file_exts_to_load=None):

    # Set the embedding model
    Settings.embed_model = CodeT5Embedder()

    # Split for code docs and load nodes
    split_code_nodes = load_code_nodes(code_dir=code_directory, files_exts_to_load=file_exts_to_load)
    
    # Split for confluence docs
    split_docs_nodes = load_nodes_from_confluence_space(space_key)
    
    # Combine both sets of nodes
    all_nodes = split_code_nodes + split_docs_nodes

    vector_store = set_vector_store_code_embs(path=CHROMA_DB_PATH, collection=CODE_DB_COLLECTION)

    # Set a disk persistent storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create the initial index
    index = VectorStoreIndex(all_nodes, storage_context=storage_context)

    index.storage_context.persist(persist_dir=INDEX_DIR)

    return index

if __name__ == "__main__":
    print("..running create index from docs and code")
    create_idx_from_docs_and_code(space_key=SPACE_KEY_ENV_APP, code_directory=CODE_DIRECTORY, file_exts_to_load=FILE_EXTS_TO_LOAD)
