import requests
from requests.auth import HTTPBasicAuth
import os
import json
from dotenv import load_dotenv


# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running Pages Service confluence doc from local")
    load_dotenv()
    
    
# Configuration

BASE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki/api/v2/pages"
USERNAME = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
PARENT_CODA_DOC_PAGE_ID = "5734416" # CoDa Documentation parent Page ID

auth= HTTPBasicAuth(USERNAME, API_TOKEN)

headers = {
    "Accept": "application/json",
}

def get_child_pages(parent_page_id):
    url= f"{BASE_URL}"

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
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
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

    ## POST request to create sub-page
    response = requests.post(BASE_URL, headers=headers, auth=auth, data=payload)

    if response.status_code in [200, 201]:
        print(f"✅ Sub-Page created successfully on space!")
        print("🔗 PAGE URL:", response.json().get("_links", {}).get("base") + response.json().get("_links", {}).get("webui"))
    else:
        print("❌ Error creating the Sub-Page:", response.status_code)
        print(response.text)



# get_child_pages(PARENT_CODA_DOC_PAGE_ID)

if __name__ == "__main__":
    print("...Running Pages Service confluence doc")

