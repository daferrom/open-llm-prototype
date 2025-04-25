***REMOVED***quests
from requests.auth import HTTPBasicAuth
import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv



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
TASKS_URL_V1= f"{BASE_URL}/rest/api/"
USERNAME = os.getenv("MY_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN_5")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")

auth= HTTPBasicAuth(USERNAME, API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_long_running_task(task_id:str):
    response = requests.request(
                "GET",
                url=f"{TASKS_URL_V1}longtask/{task_id}",
                headers=headers,
                auth=auth
        ***REMOVED***

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    
if __name__ == "__main__":
    get_long_running_task("32604161")