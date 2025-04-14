import os
import sys
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import CodeSplitter
from llama_index.llms.openai import OpenAI
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

from llama_index.core import ServiceContext
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

from tree_sitter import Parser
from tree_sitter_language_pack import get_parser

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils

def load_code_file_as_docs(code_dir, file_exts_list):
    print(f"📂 Loading files from code repository {code_dir}...")
    reader = SimpleDirectoryReader(code_dir, recursive=True, required_exts=[".json", ".ts", "mjs", ".js", ".vue" ,".prisma", ".css", "md"])
    documents = reader.load_data()
    print(f"🔢 Loaded {len(documents)} documents")
    return documents



def get_parser_for_language(language: str) -> Parser:
    """Returns a configured parser for a programming language tree-sitter-language-pack."""
    try:
        parser = get_parser(language)
        # parser = Parser()
        # parser.set_language(ts_language)
        return parser
    except Exception as e:
        print(f"❌ The parser couldn't be obtained for {language}: {e}")
        return None


def set_vector_store_code_embs():
    # Set db config
    db = chromadb.PersistentClient(path="./code_chroma_db")
    chroma_collection = db.get_or_create_collection("code_docs")
    return ChromaVectorStore(chroma_collection=chroma_collection)



def split_docs_by_prog_lang(documents):
    all_nodes =[]
    omitted_docs_per_file_type = 0
    omitted_parsers = 0
    for doc in documents:

        # language = doc.metadata.get("file_type", None)
        file_extension = Path(doc.metadata['file_path']).suffix.lower()

        # Cleaning dot of string
        language = file_extension.lstrip('.')
        # print("Extension without dot", ext)

        if not language:
            print(f"⚠️ Document {language} without 'file_type', omitted ⏭️")
            continue

        print(f"🧩 Splitting DOC : {doc.metadata.get('file_path')} as {language}...")

        # For allowing parser for typescript files with tsx parser 
        # TODO: This is a temp fix it should be handled better the equivalent parser names
        if language == "ts":
            language = "tsx"

        parser_by_doc_ext = get_parser_for_language(language)

        if not parser_by_doc_ext:
            print(f"⚠️  Parser not available for {language}, Parser ommited. ⏭️")
            omitted_parsers = omitted_parsers + 1
            continue

        print("✂️ Splitting code in fragments...")
        splitter = CodeSplitter(parser=parser_by_doc_ext, language=language, chunk_lines=100)
        split_nodes = splitter.get_nodes_from_documents([doc])
        all_nodes.extend(split_nodes)

    print("ommited docs per type", omitted_docs_per_file_type)
    print("ommitted_parsers", omitted_parsers)
    return all_nodes

if __name__ == "__main__":
    # Load .env only on local execution
    env_utils.load_env_if_local()

    persist_dir = "./chroma_index"
    code_dir = "./src/code_repos"

    # Config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Sabrine shared OPEN API KEY
    assert OPENAI_API_KEY, "OPEN AI MISSING API KEY"

    # Load code files
    print("📂 Loading files from code repository...")

    file_exts_to_load = [".json", ".ts", "mjs", ".js", ".vue" ,".prisma", ".css", ".md"]

    documents = load_code_file_as_docs(code_dir, file_exts_to_load)

    nodes =split_docs_by_prog_lang(documents)

    # Create vector index
    vector_store = set_vector_store_code_embs()
    # TODO: THIS CAN BE REPLACED FOR IngestionPipeline
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("🔍 Generating embeddings and creating index...")
    embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    index = VectorStoreIndex(nodes, embed_model=embed_model)

    # make query
    print("🤖 Ready for answering question about your code !")
    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=0.5),
            response_mode="compact",
    ***REMOVED***

    # example
    response = query_engine.query("Based on the code structure, function and class names, what appears to be the purpose of this project?")
    print("\nResponse:")
    print(response)