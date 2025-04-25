import sys
from pathlib import Path
from llama_index.llms.openai import OpenAI

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils, response_processors
from config.config import CHROMA_DB_PATH ,CODE_DB_COLLECTION
from index_getter.index_getter import get_or_create_index

def create_xhtml_doc(input_query, doc_name):
    env_utils.load_env_if_local()

    index = get_or_create_index(CHROMA_DB_PATH, CODE_DB_COLLECTION)

    file_path = f"temp/{doc_name.lower()}.xhtml"

    print(f"🤖 ... Creating xhtml doc {file_path} based on your embedded code !")

    # set a query engine
    query_engine = index.as_query_engine(
            llm=OpenAI(model="gpt-4", temperature=0.5),
            response_mode="compact",
    ***REMOVED***
    # make query
    response = query_engine.query(input_query)

    cleaned_response = response_processors.clean_xml_delimiters(response.response)

    ## Write the generated doc in xhtml
    with open(file_path, "w") as f:
        f.write(cleaned_response) 

    print(f"🤖 Doc {file_path} created ")


if __name__ == "__main__":
    print("...running create xhtml doc from zero with codde idx")

