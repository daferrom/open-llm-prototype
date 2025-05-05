import sys
import os
from pathlib import Path

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from index_loader.index_loader import load_code_index
from llama_index.core import VectorStoreIndex, StorageContext
from config.config import INDEX_DIR , CODE_DIRECTORY, FILE_EXTS_TO_LOAD
from vector_store_setters.vector_store_code_embds_setter import set_vector_store_code_embs
from index_creator.create_index import create_idx
from index_creator.create_idx_from_docs_and_code import create_idx_from_docs_and_code

def get_or_create_index(chroma_db_path, db_collection_name, space_key=None):

    if os.path.exists(INDEX_DIR) and os.listdir(INDEX_DIR):
        print("...Loading index from storage...")
        return load_code_index(chroma_db_path, db_collection_name)

    else:
        if space_key is not None:
            print("Creating new index based on docs and code...")
            return create_idx_from_docs_and_code(space_key=space_key, code_directory=CODE_DIRECTORY, file_exts_to_load=FILE_EXTS_TO_LOAD)
        else:
            print("Creating new index from code base...")
            return create_idx()

if __name__ == "__main__":
    print("..running index getter")