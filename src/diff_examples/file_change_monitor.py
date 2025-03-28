import os
import time
import hashlib
import logging

# Looging Config|
logging.basicConfig(
    filename="file_changes.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

WATCHED_DIR = "watched_folder"  # Folder to check
SCAN_INTERVAL = 5


def get_file_hash(file_path):
    """Generates hash SHA256 of the file content"""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except FileNotFoundError:
        return None


def scan_directory(directory):
    """Scans files in the directory and returns their hashes."""
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = get_file_hash(file_path)
    return file_hashes


def monitor_changes():
    """Track changes in a folder"""
    if not os.path.exists(WATCHED_DIR):
        os.makedirs(WATCHED_DIR)
        logging.info(f"Created watched directory: {WATCHED_DIR}")

    previous_state = scan_directory(WATCHED_DIR)
    logging.info("Monitoring started...")

    while True:
        time.sleep(SCAN_INTERVAL)
        current_state = scan_directory(WATCHED_DIR)

        # Detect modified or new files
        for file, hash in current_state.items():
            if file not in previous_state:
                logging.info(f"New file detected: {file}")
            elif previous_state[file] != hash:
                logging.info(f"Modified file: {file}")

        # Detect Deleted files
        for file in previous_state.keys():
            if file not in current_state:
                logging.info(f"Deleted file: {file}")

        previous_state = current_state


if __name__ == "__main__":
    monitor_changes()
