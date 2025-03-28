import sys
from pathlib import Path
import json

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from client_api_ai.prompt_templates import prompt_templates
from client_api_ai import client_api_ai

from utils import env_utils , access_files_util

#INPUT diff file

# Get workspace directory
workspace = env_utils.get_workspace()
print("Workspace:", workspace)

# Set diff file path
diff_file_path = workspace / "diff.txt"

# Open and read the .diff file as a text
diff_content_read = access_files_util.read_file(diff_file_path)

print("Diff_content",diff_content_read )

with open("api_ai_response.json", "r", encoding="utf-8") as file:
    doctype_validation = json.load(file)

#TODO: Remove when confluence publish directs the right main DocType to publish
# doc_type = doctype_validation["documentation_type"] # Hardcode doctype "Technical for DEMO generation"
doc_type = "Code" #


print("DOC TYPE", doc_type)

print("Diff_content",diff_content_read )

print("Available keys in prompt_templates:", prompt_templates.keys())



if __name__ == "__main__":
    xhtml_doc_response = client_api_ai.get_api_ai_response(prompt_templates[doc_type].format(diff_content=diff_content_read))

    with open("summary.xhtml", "w") as f:
        f.write(xhtml_doc_response) ## Write the generated doc in xhtml

    print(f"XHTML Documentation by DOC TYPE {doc_type} : ", xhtml_doc_response)
