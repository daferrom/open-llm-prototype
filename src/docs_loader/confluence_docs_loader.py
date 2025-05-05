import os
import sys
from pathlib import Path

from llama_index.readers.confluence import ConfluenceReader
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils
from confluence_service.pages_service import get_all_pages, get_child_pages
from config.config import CONFLUENCE_API_BASE_URL,  PAGE_PARENTS_IDS, MODEL_FOR_EMBEDDINGS
from tracers.phoenix_tracer import set_tracer_phoenix_config

def set_confluence_loader(url):
    loader = ConfluenceReader(
        base_url = url,
        user_name = os.getenv("MY_EMAIL"),
        password = os.getenv("CONFLUENCE_API_TOKEN")
    )
    return loader

def load_docs(loader):
    pages_ids=list(PAGE_PARENTS_IDS.values())
    return loader.load_data(page_ids=pages_ids, include_children=True, include_attachments=False)

def convert_docs_to_llama_idx_objects(docs):
    return [Document(text=doc.text, metadata=doc.metadata) for doc in docs]

def load_confluence_docs_as_llama_idx_objs(url):
    loader = set_confluence_loader(url)
    loaded_docs = load_docs(loader)
    documents = convert_docs_to_llama_idx_objects(loaded_docs)
    return documents

def set_vector_store():
    # Set db config
    db = chromadb.PersistentClient(path="./doc_chroma_db")
    chroma_collection = db.get_or_create_collection("confluence_docs")
    return ChromaVectorStore(chroma_collection=chroma_collection)

# Update the db just with the updated or moddified docs
def update_vector_store():
    print("🔄 Fetching Documents from Confluence...")
    documents = load_confluence_docs_as_llama_idx_objs(url=CONFLUENCE_API_BASE_URL)

    if not documents:
        print("✅ No new documents found. Exiting...")
        return

    vector_store = set_vector_store()
    print("✅ Updating Vector Store with Docs...")

    """ TODO: Optimize docs updates and its embeddings only for the modified ones
        not the whole docs, this requires a spike to think version handling and determine
        confluence sevices to develop
    """


    # TODO: TEST WITH these models: "sentence-transformers/all-mpnet-base-v2" (Better for english). "BAAI/bge-base-en-v1.5" and  (More Precision).
    # Create the pipeline with transaformations
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=256, chunk_overlap=50),
            HuggingFaceEmbedding(model_name=MODEL_FOR_EMBEDDINGS),
        ],
        vector_store=vector_store,
    )

    pipeline.run(documents=documents)
    print("✅ Docs Update completed.")


if __name__ == "__main__":

    # Load .env only on local execution
    env_utils.load_env_if_local()

    set_tracer_phoenix_config()
    update_vector_store()
