from pathlib import Path
import sys
import json
***REMOVED***


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils , access_files_util


from client_api_ai import client_api_ai


#INPUT diff file

# Get workspace directory
workspace = env_utils.get_workspace()
print("Workspace:", workspace)

# Set diff file path
diff_file_path = workspace / "diff.txt"

# Open and read the .diff file as a text
diff_content = access_files_util.read_file(diff_file_path)



doctype_prompt_validator = f"""
    You are an expert technical writer specializing in software documentation.
    Your task is to analyze the changes in the following diff:

    {diff_content}

    Based on these changes, identify the most appropriate documentation type from the following categories:

    1. **Code**: Documentation within the code, including inline comments and docstrings.
    2. **API**: Guides on how to use functions, methods, and API endpoints. Often generated using tools like Swagger/OpenAPI, JSDoc, or Sphinx.
    3. **Technical**: Describes system architecture, data flows, design patterns, and dependencies.
    4. **User**: Provides step-by-step guides, tutorials, or user manuals on how to use the software.
    5. **Installation & Configuration**: Covers setup instructions, deployment steps, and environment configurations.
    6. **Testing**: Documents test cases, testing strategies (unit, integration, end-to-end), and quality assurance processes.
    7. **Development Process**: Explains methodologies, Git workflows, Definition of Done, PR policies, code conventions, style guides, and quality standards.

    Identify the most relevant documentation type based on the changes in the diff.

    ### Output Format:
    Return your response as a JSON object with the following structure:
    ```json
    {{
    "documentation_type": "<Selected documentation type>",
    "justification": "<Brief explanation based on the diff content>",
    "confidence": <Confidence score between 0 and 1>
    }}
    """

doctype_val_response = client_api_ai.get_api_ai_response(doctype_prompt_validator)

# 🔹 Delete delimiters```json ... ``` on the response
clean_json = re.sub(r"^```json|\n```$", "", doctype_val_response).strip()

# 🔹 Convert to Dictionary
data = json.loads(clean_json)

# Validates response format
print("TYPE !!!!!", type(doctype_val_response))
# Si la respuesta de OpenAI es un string con JSON dentro, conviértelo en un diccionario

# Write the response to a JSON file
with open("api_ai_response.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Print the response
print("... API AI response DOC type validation per diff ✅:", json.dumps(doctype_val_response, ensure_ascii=False, indent=4))
