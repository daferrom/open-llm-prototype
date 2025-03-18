***REMOVED***quests
import json
from dotenv import load_dotenv
import os
import sys
from bs4 import BeautifulSoup


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
XHTML_DOC_PATH = "summary.xhtml"

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
    print("......page_title to publish", page_title)
    post_subpage(space_id=SPACE_ID, title=page_title, parent_id=PARENT_CODA_DOC_PAGE_ID, content_xhtml=xhtml_content)



# publish_to_confluence("Change diff_content handling", XHTML_DOC_TO_PUBLISH)

with open(XHTML_DOC_PATH, "r", encoding="utf-8") as file:
    xhtml_content = file.read()



# Extract the title from the XHTML content

# Remove markdown code block markers if present
xhtml_content = xhtml_content.strip()
if xhtml_content.startswith("```xml"):
    xhtml_content = xhtml_content[7:]  # Remove ```xml
if xhtml_content.endswith("```"):
    xhtml_content = xhtml_content[:-3]  # Remove ```

soup = BeautifulSoup(xhtml_content, "lxml-xml")  # Use "lxml-xml" for valid XHTML

# Look for the <head> and then the <title>
head = soup.find("head")
title = head.find("title").string if head and head.find("title") else "No title found"


print(f".....PUBLISHING XHTML DOC {title}......")
publish_confluence_subpage(title, xhtml_content)

