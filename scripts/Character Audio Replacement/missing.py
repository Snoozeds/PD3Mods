import os

def check_missing_files(tsv_file, destination_dir, filesReplacingColumn):
    print("Checking for missing files in destination directory:", destination_dir)
    
    # Read the TSV file and extract the PD3 IDs
    with open(tsv_file, 'r') as tsv:
        lines = tsv.readlines()
        # Get the header line
        header = lines[0].strip().split('\t')
        # Find the index of the PD3 ID column
        pd3_id_index = header.index(filesReplacingColumn)

        # Extract PD3 IDs from the TSV file
        pd3_ids = set()
        for line in lines[1:]: # Skip header line
            columns = line.strip().split('\t')
            pd3_id = columns[pd3_id_index]
            pd3_ids.add(pd3_id)

    # Get the list of files in the destination directory
    destination_files = os.listdir(destination_dir)
    
    # Compare PD3 IDs against destination files
    missing_files = []
    for pd3_id in pd3_ids:
        if pd3_id + ".wav" not in destination_files:
            missing_files.append(pd3_id)

    if missing_files:
        print("Missing files found in destination directory:")
        for missing_file in missing_files:
            print("- ", missing_file)
    else:
        print("No missing files found in destination directory.")

if __name__ == "__main__":
    # TSV file and destination directory
    tsv_file = "map.tsv"
    destination_dir = "RenamedLittleEndian"
    # Column containing PD3 IDs
    filesReplacingColumn = "PD3 ID"

    check_missing_files(tsv_file, destination_dir, filesReplacingColumn)
