import os
from openai import OpenAI
from dotenv import load_dotenv


# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

# TODO: Refactor this workspace validation in an utility single module in that way can be reused in other scripts
# Get workspace directory from GitHub Actions
workspace = os.getenv("GITHUB_WORKSPACE", "LOCAL")
print("Workspace:", workspace)

# Set diff file path
diff_file_path = os.path.join(workspace, "diff.txt")

# Overwrite diff_file_path if running locally
if workspace == "LOCAL":
    print("Running locally...")
    diff_file_path = "diff.txt"

print("Diff file path:", diff_file_path)

# Open and read the .diff file as a text


with open(diff_file_path, "r", encoding="utf-8") as file:
    diff_content = file.read()
    print("diff file content in with: ", diff_content)
    # diff_text = diff_content


# Load .env only on local execution

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()


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
    2. **Generate a clear and concise title**: Provide a high-level summary of the changes.
    3. **Describe the modifications**: Specify what was added, removed, or updated.
    4. **Evaluate the impact**: Explain how these changes affect compatibility, performance, or system behavior.
    5. **Format the documentation in AsciiDoc**: Use structured headings, bullet points, and examples for clarity.

    ## Output Format:
    The generated documentation should follow this AsciiDoc structure:

    ```adoc
    = <Title summarizing changes>

    == Summary
    <Brief overview of the modifications>

    == Changes
    - <Detailed list of modifications>

    == Impact
    <Explanation of system-wide effects>

    == Code Diff
    ```
    diff
    {diff_content}
    """
print(prompt)


def summarize_changes(prompt):
    print("...Generating AsciiDoc documentation based on the provided `.diff")
    
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
    print(response.choices[0].message.content) ##  OUTPUT: The generated AsciiDoc documentation based on the provided `.diff` file.

    
    return response.choices[0].message.content


if __name__ == "__main__":

    summary = summarize_changes(prompt)
    with open("summary.adoc", "w") as f:
        f.write(summary) ## Write the generated AsciiDoc documentation to a summary.adoc file

    print("Doc Summary en summary.adoc")


