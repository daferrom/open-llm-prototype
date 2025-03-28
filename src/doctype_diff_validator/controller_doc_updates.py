import json
***REMOVED***
import sys
from pathlib import Path

# Import utilities
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import env_utils, access_files_util
from client_api_ai import client_api_ai
from prompts import doctype_validator, updateDocument
from client_api_ai import prompt_templates
from confluence_service import pages_service


def get_diff_file_content() -> str:
    """Retrieves the content of the diff.txt file within the workspace."""
    workspace_path = env_utils.get_workspace()
    diff_file_path = workspace_path / "diff.txt"
    return access_files_util.read_file(diff_file_path)


def clean_json_response(response: str) -> dict:
    cleaned_json = re.sub(r"^```html|\n```$", "", response).strip()
    return cleaned_json


def save_json_to_file(data: dict, filename: str = "api_ai_response.json") -> None:
    """Saves a dictionary to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    """Executes document type validation based on the diff file."""
    diff_content = get_diff_file_content()

    # Generate validation prompt
    # prompt_validator = doctype_validator.doctypeValidator(diff_content)
    
    # Process API response
    InfoParentPage = pages_service.getContentBytitle(title="4. User Docs",parentPageId="5734416").json()["results"]
    if len(InfoParentPage) > 0:
        version = InfoParentPage[0]["version"]["number"]+1
        previusDocumentation = InfoParentPage[0]["body"]["storage"]["value"]
        pageIdToUpdate = InfoParentPage[0]["id"]
        promToSend = updateDocument.updateDocumentation(diff_content=diff_content, previusDocumentation=previusDocumentation)
        newDocumentation = client_api_ai.get_api_ai_response(promToSend)
        newDocumentationFormated = re.sub(r"^```xml\n|\n```$", "", newDocumentation).strip()
        pages_service.updateContent(version=version, contenidoXML=newDocumentationFormated,title="4. User Docs", pageId=pageIdToUpdate)
    else:
        promToSend = prompt_templates.prompt_templates["User"].format(diff_content=diff_content)
        api_response = client_api_ai.get_api_ai_response(promToSend)
        pages_service.createDocumentation(title="4. User Docs",content_xhtml=api_response,parentPageId="5734416")
    # validated_data = clean_json_response(api_response)

    # # Save response to a JSON file
    # save_json_to_file(validated_data)

    # # Display the result in the console
    # print("✅ API AI Response (Document Type Validation):")
    # print(json.dumps(validated_data, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    main()
