import requests
from requests.auth import HTTPBasicAuth
import sys
from pathlib import Path
import os
import json
from dotenv import load_dotenv

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import PARENT_CODA_DOC_PAGE_ID # CoDa Documentation parent Page ID



# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running Pages Service confluence doc from local")
    load_dotenv()
    
    
# Configuration
CONFLUENCE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki/rest/api"
BASE_URL =       "https://nisum-team-aqnn9b9c.atlassian.net/wiki/api/v2/pages"
USERNAME = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

auth= HTTPBasicAuth(USERNAME, API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_page_content_by_id(page_id):
    response = requests.request(
        "GET",
        url= f"{BASE_URL}/{page_id}?body-format=storage",
        headers=headers,
        auth=auth,
    )

    response = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    print("get_page_content_by_id response: ", response)
    return response

def get_child_pages(parent_page_id):
    response = requests.request(
        "GET",
        f"{BASE_URL}/{parent_page_id}/children",
        headers=headers,
        auth=auth,
        timeout=10
    )
    response_data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
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

def get_all_pages(max_retries=3):

    url = f"{BASE_URL}"
    print(url)
    pages = []
    retries = 0

    while url and retries < max_retries:
        try:
            response = requests.request(
                "GET",
                url,
                headers={
                    "Accept": "application/json"
                },
                auth=auth,
                timeout=10
            )
                    # Validation Confluence API code response 
            if response.status_code == 200:
                data = response.json()
                pages.extend([{"id": page["id"], "title": page["title"]} for page in data.get("results", [])])

                # Pagination handling
                url = BASE_URL + data["_links"].get("next", "") if "_links" in data and "next" in data["_links"] else None

            elif response.status_code == 401:
                raise PermissionError("⚠️ Error 401: Wrong credentials or yo don't have not permissions to access Confluence API.")

            elif response.status_code == 403:
                raise PermissionError("⚠️ Error 403: You don't have permissions to access the Confluence API.")

            elif response.status_code == 404:
                raise FileNotFoundError("⚠️ Error 404: No pages found in Confluence.")

            else:
                raise Exception(f"⚠️ Error {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            print("⏳ Error: Timeout. Retrying...")
            retries += 1

        except requests.exceptions.ConnectionError:
            print("🔌 Error: Could not connect to Confluence. Check your connection.")
            return None

        except Exception as e:
            print(str(e))
            return None

    print("Pages", pages)
    return pages

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
        )
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
        )
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

def update_page_content_by_id(xhtml_content, page_id, title, version=1):
    
    payload = json.dumps({
        "id": page_id,
        "status": "current",
        "title": title,
        "body": {
            "representation": "storage",
            "value": xhtml_content
        },
        "version": {
            "number": version,
            "message": "Test message update"
        }
    })
    try:
        response = requests.request(
            "PUT",
            url=f"{BASE_URL}/{page_id}",
            data=payload,
            headers=headers,
            auth=auth
        )
        if response.status_code == 200:
            print(f"✅ Page updated successfully!")
            print("🔗 PAGE URL:", response.json().get("_links", {}).get("base") + response.json().get("_links", {}).get("webui"))
            return response
        elif response.status_code == 401:
            print("⚠️ Error 401: Authentication failed")
            return None
        elif response.status_code == 403:
            print("⚠️ Error 403: Insufficient permissions")
            return None
        elif response.status_code == 404:
            print("⚠️ Error 404: Page not found")
            return None
        else:
            print(f"⚠️ Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("⚠️ Request timed out")
        return None
    except requests.exceptions.ConnectionError:
        print("⚠️ Connection error")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error: {str(e)}")
        return None


if __name__ == "__main__":
    print("...Running Pages Service confluence doc")