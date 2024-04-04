import os
import shutil
import time

def find_and_copy_files():
    # Prompt the user for locations
    names_ids_file = input("Enter the path to the IDs file: ")
    if not names_ids_file:
        print("Error: IDs file path cannot be empty.")
        return
    
    source_folder = input("Enter the source folder path: ")
    if not source_folder:
        print("Error: Source folder path cannot be empty.")
        return
    
    destination_folder = input("Enter the destination folder path: ")
    
    if not destination_folder:
        destination_folder = os.path.dirname(os.path.realpath(__file__))
        print("No destination folder supplied, assuming destination folder as current folder. Starting in 3...")
        time.sleep(1)
        print("No destination folder supplied, assuming destination folder as current folder. Starting in 3... 2...")
        time.sleep(1)
        print("No destination folder supplied, assuming destination folder as current folder. Starting in 3... 2... 1.")
        time.sleep(1)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    print("Started copying files.")

    start_time = time.time()

    with open(names_ids_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Split the line into name and ID
        name, _id = line.strip().split()

        # Find corresponding files with the same ID
        matching_files = []
        for root, _, files in os.walk(source_folder):
            for file in files:
                if _id in file and (file.endswith('.ubulk') or file.endswith('.uexp') or file.endswith('.uasset')):
                    matching_files.append(os.path.join(root, file))

        # Copy matching files to the destination folder
        for file_path in matching_files:
            shutil.copy(file_path, destination_folder)

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Files copied successfully! Took {time_taken:.2f} seconds.")

find_and_copy_files()
