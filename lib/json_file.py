import os
import json

def load_json(file):
    file_path = os.path.join("data", file)
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file} contains invalid JSON.")
        return None
    except Exception as e:
        print(f"An error occurred while loading {file}: {e}")
        return None

def write_json(data, file):
    file_path = os.path.join("data", file)
    try:
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=4)  # Added indent for better readability
    except Exception as e:
        print(f"An error occurred while writing to {file}: {e}")
