import os
import sys
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import CodeSplitter
from llama_index.llms.openai import OpenAI
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter, TokenTextSplitter

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils

def set_vector_store_code_embs():
    # Set db config
    db = chromadb.PersistentClient(path="./code_chroma_db")
    chroma_collection = db.get_or_create_collection("code_docs")
    return ChromaVectorStore(chroma_collection=chroma_collection)


if __name__ == "__main__":
    # Load .env only on local execution
    env_utils.load_env_if_local()
    
    persist_dir = "./chroma_index"
    code_dir = "./src/code_repos"

    
    # Config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Sabrine shar OPEN API KEY
    assert OPENAI_API_KEY, "OPEN AI MISSING API KEY"

    # Load code files
    print("📂 Loading files from code repository...")
    reader = SimpleDirectoryReader(code_dir, recursive=True, required_exts=[".json", ".ts", "mjs", ".js", ".vue" ,".prisma", "css"])
    documents = reader.load_data()

    print(f"🔢 Loaded {len(documents)} documents")
    print(documents[15].text)  # l

    print("✂️ Splitting code in fragments...")
    splitter = TokenTextSplitter(chunk_size=256, chunk_overlap=50)


    # # TODO: Improve the using CodeSplitter parametrized for each programming language in the code
    # # splitter = CodeSplitter(chunk_lines=40)
    nodes = splitter.get_nodes_from_documents(documents)
    print(f"🧩 Generated {len(nodes)} nodes")

    # Create vector index
    vector_store = set_vector_store_code_embs()
    # TODO: THIS CAN BE REPLACED FOR IngestionPipeline
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    
    print("🔍 Generating embeddings and creating index...")
    embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        )

    # Save index for future runs
    index.storage_context.persist()

    # make query
    print("🤖 Ready for answering question about your code !")
    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=0.5),
            response_mode="tree_summarize",
            )

    # example
    response = query_engine.query("¿What's the project about?")
    print("\nResponse:")
    print(response)