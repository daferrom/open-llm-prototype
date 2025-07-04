import sys
from pathlib import Path
import os
from openai import OpenAI


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import env_utils

# Get workspace directory
workspace = env_utils.get_workspace()

# Set diff file path
diff_file_path = workspace / "diff.txt"

# Load .env only on local execution
env_utils.load_env_if_local()

# Just for non-prod Check this Documentation for more detail about How to use OpenAI API with Azure with a Github GPT4 key just(token):
# https://www.youtube.com/watch?v=YP8mV_2RDLc

API_KEY = os.getenv("GH_GPT4_API_KEY")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=API_KEY
)

def get_api_ai_response(prompt):
    MODEL="gpt-4o"
    print(f"***...🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖 Requesting response to API AI , model {MODEL} 🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖...***")

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "",
            },
            {
                "role": "developer",
                "content": prompt
            }
        ],
        model=MODEL,
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    print(f"... API AI RESPONSE ✅: {response.choices[0].message.content} \n ==============================================")

    return response.choices[0].message.content