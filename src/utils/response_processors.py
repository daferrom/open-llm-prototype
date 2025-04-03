***REMOVED***
import json

def clean_response_to_json(llama_idx_response):
     # 🔹 Delete delimiters```json ... ``` on the response
    clean_json = re.sub(r"^```json|\n```$", "", llama_idx_response.response).strip()
    # 🔹 Convert to Dictionary
    return json.loads(clean_json)

def clean_response_to_xml(llama_idx_response):
     # 🔹 Delete delimiters```json ... ``` on the response
    clean_json = re.sub(r"^```xml|\n```$", "", llama_idx_response.response).strip()
    # 🔹 Convert to Dictionary
    return json.loads(clean_json)

def clean_response_to_xml(llama_idx_response):
     # 🔹 Delete delimiters```json ... ``` on the response
    clean_json = re.sub(r"^```xml|\n```$", "", llama_idx_response.response).strip()
    # 🔹 Convert to Dictionary
    return json.loads(clean_json)

def clean_xml_delimiters(response):
    response_content = response.strip()
    if response_content.startswith("```xml"):
        response_content = response_content[7:]  # Remove ```xml
    if response_content.endswith("```"):
        response_content = response_content[:-3]  # Remove ```
    return response_content


if __name__ == "__main__":
    print("...Response processors called....")