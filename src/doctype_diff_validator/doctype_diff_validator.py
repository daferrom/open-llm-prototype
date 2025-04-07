from pathlib import Path
import sys
import json
***REMOVED***


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils ***REMOVED***ad_file_by_env
from client_api_ai.prompt_templates import prompt_templates 


from client_api_ai import client_api_ai

# Load diff.txt content
diff_content = read_file_by_env.load_diff_content("diff.txt")

doctype_val_response = client_api_ai.get_api_ai_response(prompt_templates["DOCTYPE_PROMPT_VALIDATOR"].format(diff_content=diff_content))

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
