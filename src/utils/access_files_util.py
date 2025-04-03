import json

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_file_as_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
