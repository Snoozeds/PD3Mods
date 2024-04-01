## Launches Bence's Uexp Utility multiple times for each .wav file in the directory.
## Make sure you have the .uasset, .ubulk and .uexp files for the sound you want to replace, and that the .wav has the same ID as its name.
## May lag out lower end PCs, feel free to up the first time.sleep()'s time.

################################################ IMPORTANT: #############################################
# Please do NOT run this from IDLE as it will spam your PC with command prompt windows.                 #
# Instead, open command prompt, cd to where the script and .wav files are located and run py auto.py    #
#########################################################################################################


import os
import subprocess
import time

script_dir = os.path.dirname(os.path.abspath(__file__))

# Sort
wav_files = sorted([file for file in os.listdir(script_dir) if file.endswith('.wav') and not file.endswith('.re.wav')])
total_wav_files = len(wav_files)

missing_files = []

# Prompt whether or not to delete each .wav file
delete_wav = input("Do you want to delete each .wav file in this directory after processing it? (yes/y/no/n): ").lower().strip()

if delete_wav in ["yes", "y"]:
    delete_wav = True
else:
    delete_wav = False

start_time = time.time()

# Text printing colors
RED_TEXT = "\033[91m"
GREEN_TEXT = "\033[92m"
CYAN_TEXT = "\033[96m"
DEFAULT_TEXT = "\033[0m"

# Iterate through each file in the directory
for index, filename in enumerate(wav_files, start=1):
    wav_file = os.path.join(script_dir, filename)
    id_name = os.path.splitext(filename)[0]

    print(f"{GREEN_TEXT}Processing {filename}{CYAN_TEXT} ({index}/{total_wav_files}){DEFAULT_TEXT}")

    # Run BencesUexpUtility.exe for each .wav file
    process = subprocess.Popen(["BencesUexpUtility.exe", filename], cwd=script_dir)
    time.sleep(0.4)
    process.kill()
    time.sleep(1)

    if delete_wav:
        os.remove(wav_file)
        print(f"{RED_TEXT}Deleted {filename}{CYAN_TEXT} ({index}/{total_wav_files}){DEFAULT_TEXT}")

end_time = time.time()

# Calculate time took
total_seconds = end_time - start_time
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

print(f"Processed all files, took {'{0} minutes '.format(minutes) if minutes >= 1 else ''}{seconds} seconds.")
