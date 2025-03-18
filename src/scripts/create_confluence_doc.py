***REMOVED***quests
import subprocess
import json
from dotenv import load_dotenv
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from confluence_service.pages_service import post_subpage  # Importar la función


# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running create confluence doc from local")
    load_dotenv()

# Config

EMAIL = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
# This would be the reference SPACE of the project en confluence
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY") ##
SPACE_ID = "295237"
PARENT_CODA_DOC_PAGE_ID = "5734416" # CoDa Documentation parent Page ID
CONFLUENCE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki/rest/api/content"
ADOC_FILE = "summary.adoc"

# Convert AsciiDoc to XHTML
def convert_adoc_to_xhtml(adoc_file):
    try:
        result = subprocess.run(
            ["asciidoctor", "-o", "-", "-s", "--backend=html5", adoc_file],
            capture_output=True,
            text=True,
            check=True
***REMOVED***
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("❌ Error al convertir AsciiDoc:", e)
        return None


auth = (EMAIL, API_TOKEN)

def publish_to_confluence(title,  content_xhtml):

    # Set data Page payload
    data = {
        "type": "page",
        "title": title,
        "space": {"key": SPACE_KEY},
        "body": {
            "storage": {
                "value": content_xhtml,
                "representation": "storage"
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    auth = (EMAIL, API_TOKEN)

    # # POST Request to create confluence page 
    response = requests.post(CONFLUENCE_URL, headers=headers, auth=auth, data=json.dumps(data))

    if response.status_code in [200, 201]:
        print("✅ Page created successfully!")
        print("🔗 PAGE URL:", response.json().get("_links", {}).get("base") + response.json().get("_links", {}).get("webui"))
    else:
        print("❌ Error creating the page:", response.status_code)
        print(response.text)


# Publish a child page in a confluence page in content
def publish_confluence_subpage(page_title, xhtml_content):
    post_subpage(space_id=SPACE_ID, title=page_title, parent_id=PARENT_CODA_DOC_PAGE_ID, content_xhtml=xhtml_content)


# Extract title from AsciiDoc file
def extract_adoc_title(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line.startswith("="):  # Detecta el título en AsciiDoc
                return line.lstrip("= ").strip()  # Elimina '=' y espacios adicionales
    return None  # Si no encuentra título

# Ejemplo de uso
doc_title = extract_adoc_title(ADOC_FILE)
print(doc_title)


XHTML_DOC_TO_PUBLISH = convert_adoc_to_xhtml(ADOC_FILE)
print(".....XHTML_DOC_TO_PUBLISH......", XHTML_DOC_TO_PUBLISH)

# publish_to_confluence("Change diff_content handling", XHTML_DOC_TO_PUBLISH)

with open("summary.xhtml", "r", encoding="utf-8") as file:
    xhtml_content = file.read()

publish_confluence_subpage("Update to GitHub Workflow for Documentation Publishing TEST 1.0.0", xhtml_content)

