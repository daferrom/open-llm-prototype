import sys
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import env_utils

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

# Get workspace directory
workspace = env_utils.get_workspace()
print("Workspace:", workspace)

# Set diff file path
diff_file_path = workspace / "diff.txt"


# Open and read the .diff file as a text

with open(diff_file_path, "r", encoding="utf-8") as file:
    diff_content = file.read()
    print("diff file content in with: ", diff_content)


# Load .env only on local execution
env_utils.load_env_if_local()

API_KEY = os.getenv("GH_GPT4_API_KEY")

if not API_KEY:
    raise ValueError("API KEY GH_GPT4_API_KEY is not set")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=API_KEY
)

print("...USING API_KEY GH_GPT4_API_KEY....") ## OUTPUT: USING API_KEY GH_GPT$_API


prompt = f"""
    You are an expert technical writer specializing in software documentation. Your task is to generate documentation in AsciiDoc (`.adoc` format) based on the provided Git `.diff` file. The documentation should clearly describe the modifications, including added, removed, or changed functionality.

    ## Instructions:
    1. **Analyze the `.diff` file**: Identify the affected functions, methods, classes, or modules.
    2. **Generate a clear and concise title**: Provide a high-level meaningful title of the changes.
    3. **Summarize the changes**: Write a brief summary of the modifications made in the code.
    3. **Describe the modifications**: Specify what was added, removed, or updated.
    4. **Assess the impact**: Explain how these changes affect the system in terms of compatibility, performance, or behavior.
    5. **Generate valid XHTML output**: Ensure correct syntax, including lowercase tags, self-closing elements (`<br />`, `<img />`), and properly quoted attributes.

    ## Output Format:
    The generated documentation should follow this XHTML structure:

    ```xml
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title> <!--Here should be place the title generated--> </title>
    </head>
    <body>
    <h1><!--Here must be placed the title generated--></h1>

    <h2>Summary</h2>
    <p><!--Here must be placed the summary generated--></p>

    <h2>Changes</h2>
    <ul>
        <li><strong>Modified Components:</strong> AI should list the affected components or files with the description of the modifications.</li>
        <li><strong>Key Changes:</strong> AI should summarize the main modifications.</li>
    </ul>

    <h2>Impact</h2>
    <p><!--Here must be placed the evaluation of the impact --></p>

    <h2>Code Diff</h2>
    <pre><code>
    {diff_content}
    </code></pre>
</body>
</html>
    """
print(prompt)


def summarize_changes(prompt):
    print("...Generating XHTML documentation based on the provided `.diff")
    
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
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    print(response.choices[0].message.content) 
    return response.choices[0].message.content ##  OUTPUT: The generated XHTML Doc documentation based on the provided `.diff` file.


if __name__ == "__main__":

    summary = summarize_changes(prompt)
    with open("summary.xhtml", "w") as f:
        f.write(summary) ## Write the generated doc in xhtml

    print("Doc Summary en summary.xhtml")


