# This script generates a tab-separated values file named "generated.tsv" with the following columns:
# PD2 ID    PD2 Speech    PD3 ID    PD3 Speech    PD3 Name    Notes
# 
# PD3 ID values are extracted from the names of WAV files located in a folder named "WAV" within the same directory (e.g., filenames like 451199311.wav).
# Corresponding PD3 Name values are extracted from JSON files located in a folder named "json_files" within the same directory (e.g., filenames like 451199311.json).
# 
# File structure:
# - json_files
#     - (JSON files)
# - WAV
#     - (WAV files)
# - tsvgenerator.py

import os
import json
import csv

def get_medianame(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for item in data:
            if 'Properties' in item and 'MediaName' in item['Properties']:
                return item['Properties']['MediaName']
    return None

# Function to process WAV files and create TSV
def create_tsv(wav_folder, json_folder, tsv_file):
    with open(tsv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['PD2 ID', 'PD2 Speech', 'PD3 ID', 'PD3 Speech', 'PD3 Name', 'Notes'])
        
        # Get all WAV files and sort them based on their ID, lowest to highest
        wav_files = [filename for filename in os.listdir(wav_folder) if filename.endswith('.wav')]
        wav_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
        
        for filename in wav_files:
            pd3_id = os.path.splitext(filename)[0]
            pd3_speech = ''
            json_file = os.path.join(json_folder, pd3_id + '.json')
            pd3_name = get_medianame(json_file) if os.path.exists(json_file) else ''
            writer.writerow(['', '', pd3_id, pd3_speech, pd3_name, '', ''])

if __name__ == '__main__':
    wav_folder = 'WAV'
    json_folder = 'json_files'
    tsv_file = 'generated.tsv'
    create_tsv(wav_folder, json_folder, tsv_file)
