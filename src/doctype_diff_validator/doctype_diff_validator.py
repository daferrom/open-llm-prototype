from pathlib import Path
import sys
import json
import re


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import read_file_by_env


from client_api_ai import client_api_ai

# Load diff.txt content
diff_content = read_file_by_env.load_diff_content("diff.txt")

# TODO: PLace prompt in prompt_templates.py

doctype_prompt_validator = f"""
    As a specialized documentation analyzer, evaluate the following code diff 
    to determine its primary documentation category:

    {diff_content}

    Documentation Categories:
    1. CODE         - In-code documentation (comments, docstrings)
    2. API          - Function/method/endpoint usage guides
    3. TECHNICAL    - System architecture and design documentation
    4. USER         - End-user guides and tutorials
    5. SETUP        - Installation and configuration instructions
    6. TESTING      - Test documentation and QA processes
    7. PROCESS      - Development workflows and standards

    Requirements:
    - Choose ONE primary category that best matches the diff
    - Consider the context and scope of changes
    - Base your decision on concrete evidence from the diff

    Respond in JSON format:
    {{
        "documentation_type": "<category_name>",
        "id": "<1-7>",
        "justification": "<specific_evidence_from_diff>",
        "confidence": <0.0-1.0>
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
