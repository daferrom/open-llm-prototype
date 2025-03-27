import llama_index.core
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.readers.confluence import ConfluenceReader
import sys
from pathlib import Path

import llama_index
import os
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import VectorStoreIndex
from llama_index.core.evaluation import FaithfulnessEvaluator

import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from client_api_ai.prompt_templates import prompt_templates
from utils import read_file_by_env


from utils import env_utils

# Load diff.txt content
diff_content_loaded = read_file_by_env.load_diff_content("diff.txt")

# Load .env only on local execution
env_utils.load_env_if_local()

HF_API_TOKEN = os.getenv("MY_HF_TOKEN")
CONFLUENCE_READER_TOKEN= os.getenv("CONFLUENCE_READER_TOKEN")
USER = os.getenv("MY_EMAIL")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")


BASE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki"

# PHOENIX Config for Tr
PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={PHOENIX_API_KEY}"

llama_index.core.set_global_handler(
    "arize_phoenix",
    endpoint="https://llamatrace.com/v1/traces"
)


# Load Confluence Documents
# TODO: CREATE OAUTH 2.0 token service autorization
# TODO: Implement fetching Data by batches or pagination to execute pipeline on paralell async
# loader = ConfluenceReader(
#     base_url = BASE_URL,
#     user_name = USER,
#     password = CONFLUENCE_READER_TOKEN
# )

# # Load documents (Confluence pages) from a specified space
# docs = loader.load_data(space_key=SPACE_KEY, include_attachments=False)

# # Convertirlos en objetos `Document` de LlamaIndex
# documents = [Document(text=doc.text) for doc in docs]


# for doc in documents:
#     print("=============== Start Doc================", doc.text[:500])  # Muestra los primeros 500 caracteres


# TODO: Set an backend database
# Set db config
db = chromadb.PersistentClient(path="./doc_chroma_db")
chroma_collection = db.get_or_create_collection("confluence_docs")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Create the pipeline with transaformations
# TODO: TEST WITH:
# "sentence-transformers/all-mpnet-base-v2" (Better for english).
# "BAAI/bge-base-en-v1.5" and  (More Precision).

# pipeline = IngestionPipeline(
#     transformations=[
#         SentenceSplitter(chunk_size=256, chunk_overlap=50),
#         HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5"),
#     ],
#     vector_store=vector_store,
# )

# pipeline.run(documents=documents)

# create index from our vector store and embeddings:
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)



## as_query_engine:

## TODO: This Would be enhacement Querying a VectorStoreIndex with prompts and LLMs
## TODO: Test with as_retriever
## USE this as_retriever
#  Returns a list of nodes(Documents) NodesWithScore

llm = HuggingFaceInferenceAPI(
        model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
        temperature=0.7,
        max_tokens=500,
        token=HF_API_TOKEN,
    )

# FaithfulnessEvaluator
evaluator = FaithfulnessEvaluator(llm=llm)

print("MY DIFF CONTENT", diff_content_loaded)

query_engine = index.as_query_engine(
    llm=llm,
    response_mode="tree_summarize",
)
response = query_engine.query(prompt_templates["DOCTYPE_PROMPT_VALIDATOR"].format(diff_content=diff_content_loaded))

print(" 😎😎😎😎😎 response 😎😎😎😎😎", response) # Response must be The setup Instructions of Coda

# TODO: Visualize evaluations
eval_result = evaluator.evaluate_response(response=response)
eval_result.passing




