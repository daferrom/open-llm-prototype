import sys
from pathlib import Path
# Add 'src' to sys.path for allowing imports

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import FILE_EXTS_TO_LOAD, CODE_DIRECTORY 
from docs_loader.code_loader import load_code_file_as_docs
from doc_processors.code_splitter import split_docs_by_prog_lang

def load_nodes(code_dir, files_exts_to_load):
    documents = load_code_file_as_docs(code_dir, files_exts_to_load)
    nodes = split_docs_by_prog_lang(documents)
    return nodes