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

print("diff file content: ", diff_content)

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


prompt = f"""You are an expert technical writer specializing in software documentation. Your task is to generate documentation in AsciiDoc (`.adoc` format) based on the provided Git `.    diff` file. The documentation should clearly describe the modifications, including added, removed, or changed functionality.
            ## Instructions:
            1. **Analyze the `.diff` file**: Identify the affected functions, methods, classes, or modules.
            2. **Describe the changes**: Summarize what was modified, added, or removed.
            3. **Explain the impact**: Detail how these changes affect the system, including compatibility, performance, or behavior.
            4. **Generate AsciiDoc content**: Structure the documentation with appropriate headings, bullet points, and examples.

            ## Output Format:
            The generated documentation should follow this AsciiDoc structure:

            ## Diff Input:
            ```diff
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



# ```adoc
# = Documentation: Changes to `calculator.js`

# == Overview

# This document outlines the changes made to the `calculator.js` file. The modifications involve the addition of a logging statement to the `sumar` function.

# == Changes in the Code

# === Modified Function: `sumar`

# ```diff
#  function sumar(a, b) {
# +    console.log(`Sumando ${a} + ${b}`);
#      return a + b;
#  }
# ```

# - **Change Description**:
#   A `console.log` statement was added at the beginning of the `sumar` function to log the numbers being added.
  
# - **Added Line**: 
#   ```javascript
#   console.log(`Sumando ${a} + ${b}`);
#   ```

# == Impact of the Change

# === Behavior Changes

# - **Logging Added**:
#   - The function `sumar` now outputs a message to the console every time it is called. 
#   - The message includes the two numbers passed to the function, formatted as: `Sumando <a> + <b>`.

# === Compatibility

# - **No Breaking Changes**:
#   - Existing functionality is not altered. The function still returns the sum of the two arguments as before.
#   - There are no changes to the function signature or return type.

# === Performance Considerations

# - **Minimal Impact**:
#   - The addition of the `console.log` statement introduces a negligible performance impact, which may be noticeable only in very high-frequency executions or resource-constrained environments.

# == Recommendations for Developers

# - **Debugging Aid**:
#   - The added `console.log` statement can be helpful for debugging purposes to verify the inputs to the `sumar` function.
  
# - **For Production Environments**:
#   - If logging is not desirable in production, consider wrapping the `console.log` statement in a conditional check to enable it only in development mode. For example:
#     ```javascript
#     if (process.env.NODE_ENV === 'development') {
#         console.log(`Sumando ${a} + ${b}`);
#     }
#     ```

# == Example Usage

# === Before the Change

# ```javascript
# const result = sumar(3, 5);
# // Output: (No console output)
# ```

# === After the Change

# ```javascript
# const result = sumar(3, 5);
# // Console Output: Sumando 3 + 5
# ```

# The return value (`result`) remains unchanged: `8`.

# == Conclusion

# This update improves the debuggability of the `sumar` function without altering its core functionality. Developers are encouraged to review the logging requirements in production environments to avoid unnecessary console output.
# ```
