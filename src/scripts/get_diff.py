import subprocess
import os

# TODO: Refactor this worskpace validation in an utility single module in that way can be reused in other scripts
# Get workspace directory from GitHub Actions
workspace = os.getenv("GITHUB_WORKSPACE", ".")
print("Workspace before local validation:", workspace)

# Set diff file path
diff_file_path = os.path.join(workspace, "diff.txt")

# Overwrite diff_file_path if running locally
if workspace == ".":
    print("Running locally...")
    diff_file_path = "diff.txt"

print("Workspace after local validation:", workspace)
print("Diff file path:", diff_file_path)

#TODO: This can be converted to a git command

def get_git_diff():
    """Get the .diff file of the last  HEAD commit and the previous one"""
    diff = subprocess.run(["git", "diff", "HEAD^","HEAD"], capture_output=True, text=True)
    return diff.stdout

if __name__ == "__main__":
    diff_text = get_git_diff()
    with open(diff_file_path, "w") as f:
        f.write(diff_text)
    print("diff_text:", diff_text)
    print("Changes Detected on diff.txt")