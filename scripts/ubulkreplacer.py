### Duplicates the original .wav file (input.wav) to new .wav files with the ID of each ubulk file (xxxxxxxxxx.wav)
### Useful for Bence's Uexp Utility.
### Practically only useful to change multiple sounds at once to the same sound.

import os
import shutil

def create_wav_files(custom_wav_path):

    script_dir = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(script_dir)

    # Iterate through each file
    for file in files:
        if file.endswith('.ubulk'):
            # Extract the ID from the filename
            file_id = os.path.splitext(file)[0]

            destination_wav_path = os.path.join(script_dir, file_id + '.wav')
            shutil.copy(custom_wav_path, destination_wav_path)

            print(f"Created {file_id}.wav")

create_wav_files('input.wav')
