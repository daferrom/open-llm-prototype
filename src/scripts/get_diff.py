import subprocess

def get_git_diff():
    """Get the .diff file of the last commit."""
    diff = subprocess.run(["git", "diff", "HEAD^"], capture_output=True, text=True)
    return diff.stdout

if __name__ == "__main__":
    diff_text = get_git_diff()
    with open("diff.txt", "w") as f:
        f.write(diff_text)
    print("Changes Detected on diff.txt")