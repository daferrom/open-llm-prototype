import requests
from requests.auth import HTTPBasicAuth
import os
import json
from dotenv import load_dotenv


# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running create confluence doc from local")
    load_dotenv()

# Configuration
BASE_URL = "https://nisum-team-aqnn9b9c.atlassian.net//wiki/api/v2/spaces"
USERNAME = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_ID = os.getenv("CONFLUENCE_SPACE_KEY")

auth= HTTPBasicAuth(USERNAME, API_TOKEN)

headers = {
    "Accept": "application/json",
}



def get_all_pages_in_space(id, max_retries=3):
    url = f"{BASE_URL}/{id}/pages"
    print(url)
    pages = []
    
    retries = 0
    while url and retries < max_retries:
        try:
            response = requests.request(
                "GET",
                url,
                headers=headers,
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

def get_spaces():
    url = f"{BASE_URL}"
    
    # TODO: Add error handling
    response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth,
            timeout=10
        )

    data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    print(data)
    return data

def get_child_pages():
    url = f"{BASE_URL}"
    



# Get all confluence spaces of a user
get_spaces()
get_all_pages_in_space(295237)
