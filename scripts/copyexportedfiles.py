import os
import shutil
import time
import json

def get_appdata_path():
    return os.getenv('APPDATA') or os.path.expanduser('~/.config')

def get_options_file_path():
    appdata_path = get_appdata_path()
    return os.path.join(appdata_path, "snoozeds_copyexportedfiles_options.json")

def load_options_from_json():
    options_file_path = get_options_file_path()
    if os.path.exists(options_file_path):
        with open(options_file_path, 'r') as json_file:
            return json.load(json_file)
    else:
        return {"directories": []}

def save_options_to_json(options):
    options_file_path = get_options_file_path()
    with open(options_file_path, 'w') as json_file:
        json.dump(options, json_file, indent=4)

def get_file_extensions_choice():
    print("Choose the type of files to copy:")
    print("[1] .uasset, .ubulk, .uexp")
    print("[2] .json")
    print("[3] .uasset, .ubulk, .uexp, .json")
    choice = input("Enter the number corresponding to your choice: ")
    
    if choice == '1':
        return ['.uasset', '.ubulk', '.uexp']
    elif choice == '2':
        return ['.json']
    elif choice == '3':
        return ['.uasset', '.ubulk', '.uexp', '.json']
    else:
        print("Invalid choice. Defaulting to [1] .uasset, .ubulk, .uexp")
        return ['.uasset', '.ubulk', '.uexp']

def prompt_for_directory(directories):
    if not directories:
        return None
    print("Found previously used directories, type the number to select or skip:")
    for idx, directory in enumerate(directories):
        print(f"[{idx + 1}] {directory}")
    print("skip")
    choice = input("Enter your choice: ").strip().lower()
    if choice == "skip" or not choice:
        print("skipping...")
        return None
    if choice.isdigit() and 1 <= int(choice) <= len(directories):
        return directories[int(choice) - 1]
    return None

def find_and_copy_files():
    options = load_options_from_json()
    directories = options["directories"]

    source_folder = prompt_for_directory(directories)
    if not source_folder:
        source_folder = input("Enter the source folder path: ")
        if not source_folder:
            print("Error: Source folder path cannot be empty.")
            return

        if source_folder not in directories:
            directories.append(source_folder)
            save_options_to_json({"directories": directories})

    ids_file_path = input("Enter the path to the IDs file (Leave blank to assume IDs.txt): ")
    if not ids_file_path:
        ids_file_path = "IDs.txt"

    if not os.path.exists(ids_file_path):
        print("Error: IDs file or IDs.txt not found.")
        return

    destination_folder = input("Enter the destination folder path (Leave blank for script's folder): ")
    if not destination_folder:
        destination_folder = os.path.dirname(os.path.realpath(__file__))

    file_extensions = get_file_extensions_choice()

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    print("Started copying files.")

    start_time = time.time()

    with open(ids_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0]
            _id = parts[-1]
        else:
            name = None
            _id = line

        print(f"Searching for files with ID: {_id}")
        matching_files = []
        for root, _, files in os.walk(source_folder):
            for file in files:
                if _id in file and any(file.endswith(ext) for ext in file_extensions):
                    matching_files.append(os.path.join(root, file))
                    print(f"Found matching file: {file}")

        # Check if any matching files were found
        if not matching_files:
            print(f"No files found for ID: {_id} in {source_folder}")

        # Copy matching files to the destination folder
        for file_path in matching_files:
            print(f"Copying file: {file_path} to {destination_folder}")
            shutil.copy(file_path, destination_folder)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Took {time_taken:.2f} seconds.")

find_and_copy_files()
