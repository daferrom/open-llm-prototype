import sys
from pathlib import Path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import CodeSplitter
from tree_sitter_language_pack import get_parser
from tree_sitter import Parser

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY


def load_code_file_as_docs(code_dir, file_exts_list):
    print(f"📂 Loading files from code repository {code_dir}...")
    reader = SimpleDirectoryReader(code_dir, recursive=True, required_exts=file_exts_list)
    documents = reader.load_data()
    print(f"🔢 Loaded {len(documents)} documents")
    return documents


if __name__ == "__main__":
    print("...code loader running")
