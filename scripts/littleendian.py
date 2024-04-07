import os
import subprocess

input_dir = os.getcwd()
output_dir = os.path.join(input_dir, "little_endian")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)

            subprocess.run([
                "ffmpeg", "-i", input_file, "-c:a", "pcm_s16le", "-f", "wav", output_file
            ])

    print("All WAV files converted to little endian and saved in", output_dir)

except FileNotFoundError:
    try:
        for filename in os.listdir(input_dir):
            if filename.endswith(".wav"):
                input_file = os.path.join(input_dir, filename)
                output_file = os.path.join(output_dir, filename)

                subprocess.run([
                    "ffmpeg.exe", "-i", input_file, "-c:a", "pcm_s16le", "-f", "wav", output_file
                ])

        print("All WAV files converted to little endian and saved in", output_dir)
    except FileNotFoundError:   
        print("Error: ffmpeg not found. Please install ffmpeg.")
