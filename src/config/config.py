PAGE_PARENTS_IDS = {
        "CODA_GENERAL_DOCUMENTATION_ID": 5734416,
        '1': 12910597, # CODE
        '2': 12877838, # API
        '3': 12976156, #  TECHNICAL
        '4': 12943386, # USER
        '5': 12943396, # INSTALLATION_AND_CONFIG
        '6': 12976166, # TESTING
        '7': 12910631 # DEVELOPMENT_PROCESS
    }

SPACE_ID = 295237 # CONFLUENCE SPACE ID

PARENT_CODA_DOC_PAGE_ID = "5734416" # CoDa Documentation parent Page ID

DOC_TYPES = {
        "1": "Code",
        "2": "API",
        "3": "Technical",
        "4": "User",
        "5": "Installation & Configuration",
        "6": "Testing",
        "7": "Development Process",
    }

CONFLUENCE_API_BASE_URL = "https://nisum-team-aqnn9b9c.atlassian.net/wiki"

CONFLUENCE_SPACE_KEY="~7120208ad1e699b38643e5ac9b38b6b02e26f2"

MODEL_NAME= "Qwen/Qwen2.5-Coder-32B-Instruct" # Model for inferences in HF llama index

MODEL_FOR_EMBEDDINGS = "BAAI/bge-small-en-v1.5" # Model for embeddings