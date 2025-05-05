import os
import sys
from pathlib import Path
# Add 'src' to sys.path for allowing imports

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY 
from docs_loader.code_loader import load_code_file_as_docs
from doc_processors.code_splitter import split_docs_by_prog_lang
from confluence_service.spaces_service import get_spaces
from confluence_service.pages_service import get_pages_in_space
from llama_index.readers.confluence import ConfluenceReader
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY, CONFLUENCE_API_BASE_URL, CHROMA_DB_PATH, CODE_DB_COLLECTION, INDEX_DIR
from llama_index.core.node_parser import SentenceSplitter

def load_code_nodes(code_dir, files_exts_to_load):
    documents = load_code_file_as_docs(code_dir, files_exts_to_load)

    # Add metadata , code type
    for doc in documents:
        doc.metadata['type'] = 'code'
        doc.metadata['source'] = 'repository'

    nodes = split_docs_by_prog_lang(documents)
    return nodes

def load_nodes_from_confluence_space(space_key):
    spaces = get_spaces()

    results = spaces["results"]
    result = [space for space in results if space["key"] == space_key]

    space_id = result[0]["id"]

    pages = get_pages_in_space(space_id)

    pages_ids = [page["id"] for page in pages]

    print("pages_ids", pages_ids)

    loader = ConfluenceReader(
            base_url = CONFLUENCE_API_BASE_URL,
            user_name = os.getenv("MY_EMAIL"),
            password = os.getenv("CONFLUENCE_API_TOKEN")
***REMOVED***

    confluence_documents = loader.load_data(page_ids=pages_ids, include_children=True, include_attachments=False)

    # Add metadata , documentation type
    for doc in confluence_documents:
        doc.metadata['type'] = 'documentation'
        doc.metadata['source'] = 'confluence'

    # Split for confluence docs
    doc_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)

    # Apply splits on docs

    return doc_splitter.get_nodes_from_documents(confluence_documents)
