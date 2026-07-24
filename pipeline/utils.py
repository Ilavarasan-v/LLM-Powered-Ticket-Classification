"""
utils.py

Utility functions used across the project.
"""

import json
import os


# --------------------------------------------------
# Create Folder
# --------------------------------------------------

def create_output_directory():

    os.makedirs("outputs", exist_ok=True)


# --------------------------------------------------
# Save JSON
# --------------------------------------------------

def save_json(data, filename):

    create_output_directory()

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------------------------
# Load JSON
# --------------------------------------------------

def load_json(filename):

    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as file:

        return json.load(file)


# --------------------------------------------------
# Log Invalid Response
# --------------------------------------------------

def log_invalid_response(ticket_id, response, error):

    create_output_directory()

    log_file = "outputs/invalid_responses.json"

    if os.path.exists(log_file):

        with open(log_file, "r", encoding="utf-8") as file:

            logs = json.load(file)

    else:

        logs = []

    logs.append({

        "ticket_id": ticket_id,

        "raw_response": response,

        "error": str(error)

    })

    with open(log_file, "w", encoding="utf-8") as file:

        json.dump(

            logs,

            file,

            indent=4,

            ensure_ascii=False

        )


# --------------------------------------------------
# Print Section Header
# --------------------------------------------------

def print_header(title):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)


# --------------------------------------------------
# Print Success
# --------------------------------------------------

def print_success(message):

    print(f"✅ {message}")


# --------------------------------------------------
# Print Error
# --------------------------------------------------

def print_error(message):

    print(f"❌ {message}")