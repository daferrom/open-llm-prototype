***REMOVED***quests
from requests.auth import HTTPBasicAuth
import sys
from pathlib import Path
import os
import json
from dotenv import load_dotenv

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))




# Load env variables from .env
if os.getenv("GITHUB_ACTIONS") is None:
    # print("...Running Pages Service confluence doc from local")
    load_dotenv()

# Configuration
CONFLUENCE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki/rest/api"
CONFLUENCE_BASE_URL = "https://nisum-team-aqnn9b9c.atlassian.net"
CONFLUENCE_API_V2 = "/wiki/api/v2"
BASE_URL = f"{CONFLUENCE_BASE_URL}{CONFLUENCE_API_V2}/pages"
BASE_URL_SPACES = f"{CONFLUENCE_BASE_URL}{CONFLUENCE_API_V2}/spaces"

SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

USERNAME = os.getenv("MY_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
IMAGE_PATH = "architecture_diagram.png"

auth= HTTPBasicAuth(USERNAME, CONFLUENCE_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_pages_in_space(space_id):
    """ Get all pages in space"""

    url = f"{BASE_URL_SPACES}/{space_id}/pages"

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    data = response.json()
    pages = data["results"]
    return pages

def get_page_content_by_id(page_id):
    response = requests.request(
        "GET",
        f"{BASE_URL}/{page_id}?body-format=storage",
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
    print("get_child_pages response: ", response_data)    
    return response_data

def post_subpage(space_id, title, parent_id, content_xhtml):
    # Convert parent_id to string
    parent_id = str(parent_id)

    # Set data Sub-Page payload
    payload = json.dumps({
        "spaceId": space_id,
        "status": "current",
        "title": title,
        "parentId": parent_id,
        "body": {
            "representation": "storage",
            "value": content_xhtml
        }
    })
    
    print("🚀 Posting Sub-Page to Confluence with your payload:", payload)

    # Validate parent page existence
    parent_check_url = f"{BASE_URL}/{parent_id}"
    print(f"Parent check URL: {parent_check_url}")
    post_base_url = BASE_URL
    print("post_base_url", post_base_url)
    
    parent_check = requests.get(parent_check_url, headers=headers, auth=auth)
    

    if parent_check.status_code != 200:
        print(f"❌ Parent page not found or inaccessible: {parent_check.status_code}")
        print(parent_check.text)
        return None

    try:
        response = requests.post(
            post_base_url,
            headers=headers,
            auth=auth,
            data=payload,
            timeout=10
***REMOVED***
        if response.status_code in [200, 201]:
            print(f"✅ Sub-Page created successfully on space!")
            page_url = response.json().get("_links", {}).get("base", "") + response.json().get("_links", {}).get("webui", "")
            print("🔗 PAGE URL:", page_url)
            return response
        else:
            print(f"❌ Error creating the Sub-Page: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None

def get_all_pages():
    
    my_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }
    # Debug logs for credential verification (without revealing actual values)
    # print(f"Username present: {USERNAME is not None and USERNAME != ''}" )
    # print(f"API token present: {CONFLUENCE_API_TOKEN is not None and CONFLUENCE_API_TOKEN != ''}")

    

    url = f"{BASE_URL}"
    print(url)
    pages = []
    retries = 0



    try:
        response = requests.get(url=url, headers=my_headers, auth=auth)
            # Validation Confluence API code response
        if response.status_code == 200:
            data = response.json()
            pages.extend([{"id": page["id"], "title": page["title"], "version": page["version"]["number"]} for page in data.get("results", [])])

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

def create_documentation_page(title,  content_xhtml, parent_page_id=None, space_key=SPACE_KEY):
    data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content_xhtml,
                "representation": "storage"
            }
        }
    }
    if parent_page_id:
        data["ancestors"] = [{"id": parent_page_id}]

    auth = (USERNAME, CONFLUENCE_API_TOKEN)

    # # POST Request to create confluence page
    response = requests.post(f"{CONFLUENCE_URL}/content", headers=headers, auth=auth, data=json.dumps(data))

    return response

def getContentBytitle(title,parent_page_id):
    try:
        return requests.request(
            "GET",
            f"{CONFLUENCE_URL}/content/search?cql=title='{title}' AND ancestor=${parent_page_id}&expand=body.storage,version",
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
        auth = (USERNAME, CONFLUENCE_API_TOKEN)

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
***REMOVED***
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

def delete_page(id):
    """Delete a documentation page on Confluence by its ID.

    This function sends a DELETE request to the Confluence API to remove a specific page
    identified by its ID. It handles various HTTP status codes and potential errors that
    might occur during the request.

    Args:
        id (str): The ID of the Confluence page to be deleted.

    Returns:
        requests.Response: The response object if the deletion was successful.
        None: If any error occurs during the deletion process.

    Raises:
        requests.exceptions.Timeout: If the request times out.
        requests.exceptions.ConnectionError: If there's a connection error.
        Exception: For any unexpected errors during execution.

    Response Status Codes:
        200: Page successfully deleted
        401: Authentication failed
        403: Insufficient permissions
        404: Page not found

    Example:
        >>> response = delete_page("123456")
        >>> if response:
        >>>     print("Page deleted successfully")

    Note:
        The function requires global variables BASE_URL, headers, and auth to be properly
        configured before use.
    """

    try:
        response = requests.request(
            "DELETE",
            url=f"{BASE_URL}/{id}",
            headers=headers,
            auth=auth
***REMOVED***
        if response.status_code == 200 or response.status_code == 204:
            print(f"✅ Page deleted successfully!, No content response expected")
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

def upload_image_as_attachment(fileName):
    unique_filename = fileName
    unique_image_path = os.path.join(os.path.dirname(IMAGE_PATH), unique_filename)
    UPLOAD_URL = f"{CONFLUENCE_URL}/wiki/rest/api/content/{PAGE_ID}/child/attachment"

    with open(unique_image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "X-Atlassian-Token": "no-check",  
    }

    files = {
        "file": (unique_filename, image_data),
    }
    response = requests.post(
        UPLOAD_URL,
        headers=headers,
        auth=auth,
        files=files,
    )

    if response.status_code == 200:
        print("Imagen cargada exitosamente.")
        attachment_data = response.json()
        attachment_id = attachment_data["results"][0]["id"]
        return attachment_id
    else:
        print(f"Error al cargar la imagen: {response.status_code} - {response.text}")
        return None
if __name__ == "__main__":
    print("\n")