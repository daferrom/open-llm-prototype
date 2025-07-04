***REMOVED***quests
from requests.auth import HTTPBasicAuth
import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
***REMOVED***
import uuid
import random
import string


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    print("...Running create confluence doc from local")
    load_dotenv()

# Configuration
BASE_URL =  f"https://nisum-team-aqnn9b9c.atlassian.net/wiki"
CONFLUENCE_API_V2 = f"api/v2"
SPACES_URL = f"{BASE_URL}/{CONFLUENCE_API_V2}/spaces"
SPACES_URL_V1= f"{BASE_URL}/rest/api/space"
USERNAME = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN_5")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

auth= HTTPBasicAuth(USERNAME, API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def clean_empty_spaces_with_dashes(name: str, max_length: int = 255) -> str:
    name = name.lower()
    name = name.replace(' ', '-')
    name = re.sub(r'[^a-z0-9\-]', '', name)
    name = re.sub(r'-{2,}', '-', name)
    name = name.strip('-')
    print("String example", name[:max_length])
    return name[:max_length]


def generate_auto_alias(name: str, max_length: int = 255) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', name.lower())

    if len(cleaned) < 3:
        cleaned = uuid.uuid4().hex[:12]

    return cleaned[:max_length]

def generate_confluence_space_key(name: str, max_length: int = 255, add_random_suffix: bool = False) -> str:

    cleaned = re.sub(r'[^A-Za-z0-9]', '', name).upper()

    if not cleaned:
        cleaned = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


    if add_random_suffix:
        suffix_length = 4
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=suffix_length))
        base_max = max_length - suffix_length
        cleaned = cleaned[:base_max]
        return f"{cleaned}{suffix}"

    return cleaned[:max_length]

def create_new_space(title, description):
    response = []

    name = clean_empty_spaces_with_dashes(title)
    key= generate_confluence_space_key(name, 255 , True)
    alias = generate_auto_alias(key)

    payload = json.dumps({
                "name": name,
                "key": key,
                "alias": alias,
                "description": {
                    "plain": {
                        "value": description,
                        "representation": "plain"
                    }
                }
            })

    url = f"{SPACES_URL_V1}"
    data = {}

    try:
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth)

        if response.status_code == 200:
            data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None

    return data


def delete_space(space_key: str):
    try:
        response = requests.request(
            "DELETE",
            url=f"{SPACES_URL_V1}/{space_key}",
            headers=headers,
            auth=auth
***REMOVED***

    except requests.exceptions.Timeout:
            print("⏳ Error: Timeout. Retrying...")
            retries += 1

    except requests.exceptions.ConnectionError:
            print("🔌 Error: Could not connect to Confluence. Check your connection.")
            return None

    except Exception as e:
            print(str(e))
            return None

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


def get_all_pages_in_space(confluence_space_key, max_retries=3):
    url = f"{SPACES_URL}/{confluence_space_key}/pages?depth=all"
    print(url)
    pages = []

    retries = 0

    try:
        response = requests.request(
                "GET",
                url,
                headers=headers,
                auth=auth,
                timeout=10
***REMOVED***

        # Validation Confluence API code response
        if response.status_code == 200:
                data = response.json()
                pages.extend([{"id": page["id"], "title": page["title"]} for page in data.get("results", [])])

                # Pagination handling
                url = SPACES_URL + data["_links"].get("next", "") if "_links" in data and "next" in data["_links"] else None

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
    url = f"{SPACES_URL}"

    # TODO: Add error handling
    response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth,
            timeout=10
***REMOVED***

    data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    print("data", data)
    return response.json()

if __name__ == "__main__":
    get_spaces()
    print("...Running spaces service module")