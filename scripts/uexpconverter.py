import os
import json
import binascii

def find_and_replace_size(hex_data, old_size_hex, new_size_hex):
    # Check if the old size is found in the hex data
    if old_size_hex not in hex_data:
        print("Old size not found in hex data.")
        return hex_data

    new_hex_data = hex_data.replace(old_size_hex, new_size_hex)

    # Check if the replacement was successful
    if new_hex_data == hex_data:
        print("Replacement failed. Old size not replaced with new size.")

    return new_hex_data

def get_old_size_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for item in data:
            if 'DataChunks' in item and item['DataChunks']:
                return item['DataChunks'][0]['BulkData']['SizeOnDisk']
    return None

def main():
    json_files_dir = "json_files"
    
    # Iterate over uexp files in the current directory
    for uexp_file in os.listdir():
        if uexp_file.endswith(".uexp"):
            uexp_file_name = os.path.splitext(uexp_file)[0]
            ubulk_file = uexp_file_name + ".ubulk"
            
            if os.path.exists(ubulk_file):
                print("Processing:", uexp_file)
                
                # Get old size from JSON file
                json_file_path = os.path.join(json_files_dir, uexp_file_name + ".json")
                old_size = get_old_size_from_json(json_file_path)
                if old_size is None:
                    print("Error: Old size not found in JSON file for", uexp_file)
                    continue
                
                new_size = os.path.getsize(ubulk_file)
                
                old_size_hex = hex(old_size)[2:].zfill(8)  # Remove "0x" prefix
                old_size_hex = ''.join(reversed([old_size_hex[i:i+2] for i in range(0, len(old_size_hex), 2)]))
                new_size_hex = hex(new_size)[2:].zfill(8)  # Remove "0x" prefix
                new_size_hex = ''.join(reversed([new_size_hex[i:i+2] for i in range(0, len(new_size_hex), 2)]))

                # Open corresponding uexp file and replace size
                with open(uexp_file, 'rb') as uexp:
                    hex_data = binascii.hexlify(uexp.read()).decode()

                hex_data = find_and_replace_size(hex_data, old_size_hex, new_size_hex)

                # Write back to uexp file
                with open(uexp_file, 'wb') as uexp:
                    uexp.write(binascii.unhexlify(hex_data))
                
                print("Size replaced successfully.")
            else:
                print("No ubulk file found for:", uexp_file)

if __name__ == "__main__":
    main()
