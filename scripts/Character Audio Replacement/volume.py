# This script increases the volume of WAV audio files if their dBA level (loudness) is below a specified threshold.
# If the dBA level is below the threshold, it increases the volume by the gain factor (2.0).
# The modified audio is then saved back to the original file using ffmpeg. (I recommend backing up files in case something goes wrong.)
# Ensure that ffmpeg is installed for this script to work or use an executable file in the same directory and change "ffmpeg" to "ffmpeg.exe".

import os
import librosa
import soundfile as sf
import subprocess

# Function to increase volume if dBA level is below threshold
def increase_volume_if_below_threshold(file_path, threshold, gain):
    # Load the WAV file
    y, sr = librosa.load(file_path, sr=None, mono=False)

    rms = librosa.feature.rms(y=y)
    dba = librosa.A_weighting(librosa.amplitude_to_db(rms))

    # Check if dBA level is below threshold
    if dba.min() < threshold:
        y *= gain

        temp_file = os.path.splitext(file_path)[0] + "_temp.wav"
        sf.write(temp_file, y.T, sr, format='WAV', subtype='PCM_16')

        # Use ffmpeg to convert to little endian
        subprocess.run(['ffmpeg', '-i', temp_file, '-acodec', 'pcm_s16le', '-ar', '44100', '-ab', '1411k', '-y', file_path])

        os.remove(temp_file)

directory = '.'

# Threshold dBA level and the gain to apply if below threshold
threshold_dba = -30
gain = 2.0

# Iterate through all WAV files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        file_path = os.path.join(directory, filename)
        increase_volume_if_below_threshold(file_path, threshold_dba, gain)
