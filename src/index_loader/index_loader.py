# utils/load_index.py
import sys
from pathlib import Path
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore

from llama_index.core import Settings

# Add 'src' to sys.path for allowing code_embedders import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from code_embedders.code_t5_embedder import CodeT5Embedder 
from vector_store_setters.vector_store_code_embds_setter import set_vector_store_code_embs



def load_code_index(path, collection_name):

    Settings.embed_model = CodeT5Embedder()

    vector_store = set_vector_store_code_embs(path=path, collection=collection_name)

    storage_context = StorageContext.from_defaults(
        persist_dir="./src/data/vector_store/index_metadata/",
        vector_store=vector_store
    )

    return load_index_from_storage(storage_context)
