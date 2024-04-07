import os
import shutil
import time
import json

def load_options_from_json():
    options_file_path = "options.json"
    if os.path.exists(options_file_path):
        with open(options_file_path, 'r') as json_file:
            return json.load(json_file)
    else:
        return None

def save_options_to_json(options):
    options_file_path = "options.json"
    with open(options_file_path, 'w') as json_file:
        json.dump(options, json_file, indent=4)

def find_and_copy_files():
    options = load_options_from_json()
    if options:
        ids_file_path = options.get('ids_file_path', "IDs.txt")
        source_folder = options.get('source_folder', "")
        destination_folder = options.get('destination_folder', "")
    else:
        ids_file_path = input("Enter the path to the IDs file (Leave blank to assume IDs.txt): ")
        if not ids_file_path:
            ids_file_path = "IDs.txt"

        if not os.path.exists(ids_file_path):
            print("Error: IDs file or IDs.txt not found.")
            return
        
        source_folder = input("Enter the source folder path: ")
        if not source_folder:
            print("Error: Source folder path cannot be empty.")
            return
        
        destination_folder = input("Enter the destination folder path (Leave blank for script's folder): ")
        if not destination_folder:
            destination_folder = os.path.dirname(os.path.realpath(__file__))

        save_to_json = input("Do you want to save these options to an options.json file so you don't have to type the same answers in the future? (y/n): ").lower()
        if save_to_json == 'y' or save_to_json == "yes":
            if not os.path.exists("options.json"):
                save_options_to_json({
                    'ids_file_path': ids_file_path,
                    'source_folder': source_folder,
                    'destination_folder': destination_folder
                    })

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
                if _id in file and (file.endswith('.ubulk') or file.endswith('.uexp') or file.endswith('.uasset')):
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
