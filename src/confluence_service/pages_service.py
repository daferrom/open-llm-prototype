***REMOVED***quests
from requests.auth import HTTPBasicAuth
import os
import json
from dotenv import load_dotenv


# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running Pages Service confluence doc from local")
    load_dotenv()
    
    
# Configuration
CONFLUENCE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki/rest/api"
BASE_URL =       "https://nisum-team-aqnn9b9c.atlassian.net/wiki/api/v2/pages"
USERNAME = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
PARENT_CODA_DOC_PAGE_ID = "5734416" # CoDa Documentation parent Page ID
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

auth= HTTPBasicAuth(USERNAME, API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_child_pages(parent_page_id):
    response = requests.request(
        "GET",
        f"{BASE_URL}/{parent_page_id}/children",
        headers=headers,
        auth=auth,
        timeout=10
    )
    response_data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    print(response_data)

    return response_data

def post_subpage(space_id="", title="", parent_id="", content_xhtml=""):
    # Set data Sub-Page payload
    payload = json.dumps({
        "spaceId": space_id,
        "status": "current",
        "title": title,
        "parentId": parent_id,
        "body": {
            "representation": "storage",
            "value": content_xhtml
    }})
    print("🚀 Posting Sub-Page to Confluence with your payload")

    ## POST request to create sub-page
    response = requests.post(BASE_URL, headers=headers, auth=auth, data=payload)

    if response.status_code in [200, 201]:
        print(f"✅ Sub-Page created successfully on space!")
        print("🔗 PAGE URL:", response.json().get("_links", {}).get("base") + response.json().get("_links", {}).get("webui"))
    else:
        print("❌ Error creating the Sub-Page:", response.status_code)
        print(response.text)


def createDocumentation(title,  content_xhtml, parentPageId=None):
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
    if parentPageId:
        data["ancestors"] = [{"id": parentPageId}]

    auth = (USERNAME, API_TOKEN)

    # # POST Request to create confluence page 
    response = requests.post(f"{CONFLUENCE_URL}/content", headers=headers, auth=auth, data=json.dumps(data))

    return response

def getContentBytitle(title,parentPageId):
    try:
        return requests.request(
            "GET",
            f"{CONFLUENCE_URL}/content/search?cql=title='{title}' AND ancestor=${parentPageId}&expand=body.storage,version",
            headers=headers,
            auth=auth,
            timeout=10
***REMOVED***
    except ZeroDivisionError:
        print("❌ Error upon getContentByTitle")

def getContentById(id):
    try:
        return requests.request(
            "GET",
            f"{BASE_URL}/content/{id}?expand=body.storage,version",
            headers=headers,
            auth=auth,
            timeout=10
***REMOVED***
    except ZeroDivisionError:
        print("❌ Error upon getContentById")

def updateContent(contenidoXML, pageId, version,title):
    try:
        data = {
            "type": "page",
            "title": title,
            "version": {
                        "number": version
                    },
            "body": {
                "storage": {
                    "value": contenidoXML,
                    "representation": "storage"
                }
            }
        }
        auth = (USERNAME, API_TOKEN)

        # # POST Request to create confluence page 
        return requests.put(f"{CONFLUENCE_URL}/content/{pageId}", headers=headers, auth=auth, data=json.dumps(data))

    except ZeroDivisionError:
        print("❌ Error upon UpdateContent")

# get_child_pages(PARENT_CODA_DOC_PAGE_ID)

if __name__ == "__main__":
    print("...Running Pages Service confluence doc")

