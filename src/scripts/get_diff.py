import sys
import subprocess
from pathlib import Path

# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import env_utils

# Get workspace directory
workspace = env_utils.get_workspace()
print("Workspace before local validation:", workspace)

# Set diff file path
diff_file_path = workspace / "diff.txt"

print(f"Running in {'GitHub Actions' if env_utils.is_github_actions() else 'Local'}")
print("Diff file path:", diff_file_path)

print("Workspace after local validation:", workspace)
print("Diff file path:", diff_file_path)


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