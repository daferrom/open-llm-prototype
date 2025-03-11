***REMOVED***quests
import json
from dotenv import load_dotenv
import os


# Load env variables from .env
load_dotenv()


# Config

#TODO: ADOC conversion to XHTML for publishing on Confluence

EMAIL = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

CONFLUENCE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki/rest/api/content"

# Page data
data = {
    "type": "page",
    "title": "Test Page from API",
    "space": {"key": SPACE_KEY},
    "body": {
        "storage": {
            "value": "<p>Este es el contenido nuevo en formato HTML.</p>",
            "representation": "storage"
        }
    }
}

# Headers and auth
headers = {
    "Content-Type": "application/json"
}
auth = (EMAIL, API_TOKEN)

# POST Request to create page 
response = requests.post(CONFLUENCE_URL, headers=headers, auth=auth, data=json.dumps(data))

# PRINT Response
if response.status_code == 200 or response.status_code == 201:
    print("✅ Page created successfully!")
    print("🔗 URL de la página:", response.json().get("_links", {}).get("base") + response.json().get("_links", {}).get("webui"))
else:
    print("❌ Error creating the page:", response.status_code)
    print(response.text)
