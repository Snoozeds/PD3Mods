import os
import shutil
import subprocess

def generate_blank_audio(output_file, destination_dir):
    # Use ffmpeg to generate 1 second of blank audio
    command = ["ffmpeg", "-f", "lavfi", "-i", "aevalsrc=0", "-t", "1", output_file]
    subprocess.run(command, check=True)

def copy_and_rename_wav(source_dir, dest_dir, source_filename, dest_filename):
    source_path = os.path.join(source_dir, source_filename)
    dest_path = os.path.join(dest_dir, dest_filename)

    if os.path.exists(source_path):
        print("Copying and renaming:", source_path, "->", dest_path)
        shutil.copyfile(source_path, dest_path)
    else:
        print("Error: File we are replacing with does not exist:", source_path)
        with open("error_log.txt", "a") as log_file:
            log_file.write(f"Error: File we are replacing with does not exist: {source_path}\n")


def process_tsv(tsv_file, dir1, dir2, destination_dir, filesReplacingColumn, filesReplacingWithColumn):
    print("Processing TSV file:", tsv_file)
    # Read the TSV file and extract the columns for files to replace and files to replace with
    with open(tsv_file, 'r') as tsv:
        lines = tsv.readlines()
        # Get the header line
        header = lines[0].strip().split('\t')
        # Find the indices of the columns
        filesReplacingColumnIndex = header.index(filesReplacingColumn)
        filesReplacingWithColumnIndex = header.index(filesReplacingWithColumn)

        for line in lines[1:]: # Skip header line
            columns = line.strip().split('\t')
            file_to_replace = columns[filesReplacingColumnIndex]
            file_to_replace_with = columns[filesReplacingWithColumnIndex]

            # Check if the file to replace exists in either directory
            source_dir = None
            if os.path.exists(os.path.join(dir1, file_to_replace_with + ".english.wav")):
                source_dir = dir1
            elif os.path.exists(os.path.join(dir2, file_to_replace_with + ".english.wav")):
                source_dir = dir2
            elif file_to_replace_with == "MUTE":
                generate_blank_audio(os.path.join(destination_dir, file_to_replace + ".wav"), destination_dir)

            if source_dir:
                print("File to replace:", file_to_replace)
                print("File to replace with:", file_to_replace_with)
                copy_and_rename_wav(source_dir, destination_dir, file_to_replace_with + ".english.wav", file_to_replace + ".wav")
            elif not source_dir and file_to_replace_with != "MUTE":
                print("Error: File to replace not found in either directory:", file_to_replace_with)
                with open("error_log.txt", "a") as log_file:
                    log_file.write(f"Error: File to replace not found in either directory: {file_to_replace_with}\n")


if __name__ == "__main__":
    # Directories to check for the WAV files
    dir1 = "Normalised - char_hila"
    dir2 = "Normalised - robbers_mission_gen"
    destination_dir = "RenamedLittleEndian"

    # tsv file to read
    tsv_file = "map.tsv"

    # Get the IDs of the WAV files
    filesReplacingColumn = "PD3 ID"
    filesReplacingWithColumn = "PD2 ID"

    process_tsv(tsv_file, dir1, dir2, destination_dir, filesReplacingColumn, filesReplacingWithColumn)
