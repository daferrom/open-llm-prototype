import sys
from pathlib import Path
import json
import os
from bs4 import BeautifulSoup


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import PARENT_CODA_DOC_PAGE_ID , PAGE_PARENTS_IDS , DOC_TYPES , SPACE_ID # CoDa DOCUMENTATION / parent Page ID
from confluence_service.pages_service import get_child_pages ,get_page_content_by_id , update_page_content_by_id,  post_subpage
from utils.access_files_util ***REMOVED***ad_file_as_json
from llama_idx_prototype.llama_idx_prototype import set_index , set_llm_config, get_llama_idx_query
from utils import env_utils , access_files_util
from utils.response_processors import clean_xml_delimiters
from doctype_diff_validator.controller_doc_updates import get_diff_file_content
from client_api_ai.client_api_ai import get_api_ai_response
from client_api_ai.prompt_templates import prompt_templates 


def search_existing_docs(index, changes, llm):
    """ Search the most relevant doc for the changes """
     # Convert the index to a retriever for direct similarity-based retrieval.
    retriever = index.as_retriever(
        llm=llm,
        response_mode="compact"
    )

    response = retriever.retrieve(changes)
    print("------------ retrieved response ------------", response, "-----------------------------")
    return response


def decide_action(index, changes, llm):
    """Determine if update or create a new documentation page"""
    response = search_existing_docs(index=index, changes=changes, llm=llm)

    if not response:  # If the are no results it avoids updating and create a new confluence page
        print("⚠️ No documents retrieved. Cannot update, will create a new page.")
        return "create", None

    # TAKES THE TOP RESULT
    top_result = response[0]  # `NodeWithScore` object
    similarity_score = top_result.score  # `.score` almacena la similitud

    if similarity_score > 0.8: # Hardcoded on 0.59 for testing update flow purposes 
        metadata = top_result.node.metadata  # Access node metadata
        page_id = metadata.get("page_id")
        print("🔄 Updating page:", page_id)
        return "update", page_id
    else:
        print("⚠️ Similarity too low (≤ 0.8). No updates will be made.")
        return "create", None  # A new page is created


def generate_documentation(changes, action , doc_type_id , page_id):
    """Generates Documentation with GPT-4"""

    doc_type_key_prompt = DOC_TYPES[doc_type_id]
    doc_version = 1
    print(f"📝 📝 📝 📝 📝 📝 📝 📝 GENERATING {doc_type_key_prompt} DOCUMENTATION to {action} a confluence page 📝 📝 📝 📝 📝 📝 📝 📝")
    if action == "update":
        response = get_page_content_by_id(page_id)
        data = json.loads(response)
        xhtml_existing_page = data['body']['storage']['value']  # Return a string that rep the xhtml
        page_title = data['title']

        # TODO: Create Version service and versioning docs system
        doc_version = data['version']['number'] + 1

        update_doc_prompt = f"""
        You are an expert technical writer specializing in {doc_type_key_prompt} documentation.
        Given this existing xhtml documentation:
        {xhtml_existing_page}
        Given the following code changes:
        {changes}
        Update the existing xhtml documentation to including properly the new changes.
        **Output (XHTML format):**
        ```xml
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title><!-- xhtml existing title --></title>
        </head>
        <body>
            <!-- The updated documentation -->
        </body>
        </html>
        ```
        """

        return get_api_ai_response(update_doc_prompt) , doc_version , page_title
    else:
        return get_api_ai_response(prompt_templates[doc_type_key_prompt].format(diff_content=changes)), doc_version , "New Page default title"

def publish_doc_to_confluence(action, documentation, page_id, page_title, doc_type_id, doc_version=1):
    if action == "update":
        update_page_content_by_id(xhtml_content=documentation, page_id=page_id, title=page_title, version=doc_version)
    else: # when action is "create" or not action defined
        try:
            soup = BeautifulSoup(documentation, "xml")  # Try with xml parser first
            title_tag = soup.find("title")
            title = title_tag.text if title_tag else page_title
        except:
            try:
                # Fallback to lxml parser
                soup = BeautifulSoup(documentation, "lxml")
                title_tag = soup.find("title") 
                title = title_tag.text if title_tag else page_title
            except:
                # If all parsing fails, use default title
                title = page_title

        print(f".....PUBLISHING XHTML DOC TO CONFLUENCE WITH TITLE: {title}......")
        post_subpage(space_id=SPACE_ID, title=title, parent_id=PAGE_PARENTS_IDS[doc_type_id], content_xhtml=documentation)

if  __name__ == "__main__":
    print("...create_idx_by_doctype")

    # Load .env only on local execution
    env_utils.load_env_if_local()

    HF_API_TOKEN = os.getenv("MY_HF_TOKEN")
    MODEL_NAME= "Qwen/Qwen2.5-Coder-32B-Instruct"
    MODEL_FOR_EMBEDD = "BAAI/bge-small-en-v1.5"
    XHTML_DOC_PATH = "summary.xhtml"

    # Get workspace directory
    workspace = env_utils.get_workspace()

    # Set api_ai_response.json file path
    doctype_response_path = workspace / "api_ai_response.json"
    validation_doctype_json = read_file_as_json(doctype_response_path)

    print("validation_doctype_json", validation_doctype_json)

    doc_type_id = validation_doctype_json["id"]

    # Get diff content of last commit
    diff_content = get_diff_file_content()

    # Load index with all Confluence Docs
    index = set_index(model_name_for_embedd=MODEL_FOR_EMBEDD)

    llm_hf = set_llm_config(model_name=MODEL_NAME, temp=0.7, max_tokens=500, hf_api_token=HF_API_TOKEN)

    # Decide if its required to Update an existing document or create a new Page
    action, page_id = decide_action(index=index, changes=diff_content, llm=llm_hf)

    # Generate xhtml doc
    xhtml_documentation , xhtml_doc_version , page_title = generate_documentation(changes=diff_content, action=action , doc_type_id=doc_type_id , page_id=page_id)

    xhtml_documentation = clean_xml_delimiters(xhtml_documentation)

    # Save on disk xhtml doc
    with open("summary.xhtml", "w") as f:
        f.write(xhtml_documentation) ## Write the generated doc in xhtml



    print(f"XHTML Documentation by DOC TYPE {DOC_TYPES[doc_type_id]} : ", xhtml_documentation)

    publish_doc_to_confluence(action, xhtml_documentation, page_id, page_title, doc_type_id , xhtml_doc_version)
    # # Publicar en Confluence
    # status = publish_to_confluence(documentation, action, page_id)

    # print("✅ Documentación publicada con estado:", status)








