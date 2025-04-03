import sys
from pathlib import Path


# Add 'src' to sys.path for allowing utils import
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import env_utils , access_files_util


def load_diff_content(file_name):
    # Get workspace directory
    workspace = env_utils.get_workspace()
    print("Workspace:", workspace)

    # Set diff file path
    diff_file_path = workspace / file_name

    # Open and read the .diff file as a text
    return access_files_util.read_file(diff_file_path)