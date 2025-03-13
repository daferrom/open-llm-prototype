import requests
import subprocess
import json
from dotenv import load_dotenv
import os


# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running create confluence doc from local")
    load_dotenv()

# Config

EMAIL = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

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
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("❌ Error al convertir AsciiDoc:", e)
        return None



# Headers and auth
headers = {
    "Content-Type": "application/json"
}
auth = (EMAIL, API_TOKEN)

# Publish content to confluence
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

XHTML_DOC_TO_PUBLISH = convert_adoc_to_xhtml(ADOC_FILE)
print(XHTML_DOC_TO_PUBLISH)

publish_to_confluence("NEW TEST PAGE CONFLUENCE PUBLISH 1", XHTML_DOC_TO_PUBLISH)

