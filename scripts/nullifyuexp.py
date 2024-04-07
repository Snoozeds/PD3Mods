import os

def replace_bytes_in_file(file_path, replacement_bytes):
    try:
        with open(file_path, 'rb') as file:
            file_bytes = bytearray(file.read())
    except IOError:
        print(f"Failed to read the file '{file_path}'. Skipping...")
        return

    # Replace the bytes where the file size is stored, in reverse order (little-endian)
    for i in range(8):
        file_bytes[-(i + 13)] = replacement_bytes[i]

    try:
        with open(file_path, 'wb') as file:
            file.write(file_bytes)
        print("Bytes nullified.")
    except IOError:
        print("Failed to write the modified bytes back to the file.")

def main():
    replacement_bytes = bytes.fromhex('0000000000000000')

    # Get all .uexp files in the current folder
    uexp_files = [file for file in os.listdir() if file.endswith('.uexp')]

    # Iterate through each .uexp file
    for file in uexp_files:
        print(f"Processing file: {file}")
        replace_bytes_in_file(file, replacement_bytes)

if __name__ == "__main__":
    main()
