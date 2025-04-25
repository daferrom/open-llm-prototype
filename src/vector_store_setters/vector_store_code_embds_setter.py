import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

def set_vector_store_code_embs(path, collection):
    # Set db config
    db = chromadb.PersistentClient(path=path)
    chroma_collection = db.get_or_create_collection(collection)
    return ChromaVectorStore(chroma_collection=chroma_collection)
