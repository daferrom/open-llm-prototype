import sys
import os
from pathlib import Path

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from index_loader.index_loader import load_code_index
from llama_index.core import VectorStoreIndex, StorageContext
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY , CHROMA_DB_PATH ,CODE_DB_COLLECTION
from docs_loader.nodes_loader import load_nodes
from vector_store_setters.vector_store_code_embds_setter import set_vector_store_code_embs
from index_creator.create_index import create_idx

def get_or_create_index(chroma_db_path, db_collection_name):

    index_dir = "./src/data/vector_store/index_metadata/"

    if os.path.exists(index_dir) and os.listdir(index_dir):
        print("...Loading index from storage...")
        return load_code_index(chroma_db_path, db_collection_name)

    else:
        print("Creating new index...")
        return create_idx()

if __name__ == "__main__":
    print("..running index getter")