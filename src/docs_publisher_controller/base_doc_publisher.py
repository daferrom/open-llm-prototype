import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import env_utils
from confluence_service.spaces_service import create_new_space, get_spaces , delete_space
from confluence_service.pages_service import create_documentation_page, post_subpage
from confluence_service.long_running_tasks_service import get_long_running_task
from client_api_ai.prompt_templates import doc_from_code_template_prompts
from config.config import DOC_TYPES

def publish_children_doctype_pages(space_id, parent_page_id, page_title, file_name):
    # Get workspace directory
    workspace = env_utils.get_workspace()

    # Set diff file path
    base_doc_file_path = workspace / f"temp/{file_name}"


    # Open and read the base_documentation.xhtml file as a text
    with open(base_doc_file_path, "r", encoding="utf-8") as file:
        doc_content = file.read()

    post_subpage(space_id=space_id, title=page_title, parent_id=parent_page_id, content_xhtml=doc_content)

def main():
     # Get workspace directory
    workspace = env_utils.get_workspace()

    # Set diff file path
    base_doc_file_path = workspace / "temp/general_documentation.xhtml"

    # Open and read the base_documentation.xhtml file as a text
    with open(base_doc_file_path, "r", encoding="utf-8") as file:
        base_doc_content = file.read()

    soup = BeautifulSoup(base_doc_content, "xml")  # Try with xml parser first

    title = soup.find("h1").contents[0]

    description = soup.find("p").contents[0]


    # Creates a new space on confluence

    data = create_new_space(title, description)
    # Creates a page inside new space with the base documentation

    space_key= data.get('key')
    space_id= data.get('id')

    print("space_key created", space_key)
    print("space_id created", space_id)

    response = create_documentation_page(f"{title} documentation space", content_xhtml=base_doc_content, parent_page_id=None, space_key=space_key)

    response.json()
    print("response json",response.json())

    data_cr = response.json()
    parent_id=data_cr.get('id')

    # Publish all Doc types on children pages of general documentation

    for i, (prompt_key , prompt_value) in enumerate(doc_from_code_template_prompts.items(), start=1):
        file_name = f"{prompt_key.lower()}.xhtml"
        doc_name = f"{i}. {DOC_TYPES.get(str(i))} Docs"
        print("file_name", file_name)
        print("file_name", doc_name)
        publish_children_doctype_pages(space_id=space_id ,parent_page_id=parent_id, page_title=doc_name, file_name=file_name)


if __name__ == "__main__":
    main