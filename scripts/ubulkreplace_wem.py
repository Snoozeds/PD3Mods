### Replaces all .ubulk files with the single .wem file, then renames/converts all the .wem files to .ubulk
### Practically only useful to change multiple sounds at once to the same sound.

import os
import shutil

def replace_ubulk_with_wem(ubulk_folder, wem_file):
    for ubulk_file in os.listdir(ubulk_folder):
        if ubulk_file.endswith('.ubulk'):
            ubulk_path = os.path.join(ubulk_folder, ubulk_file)
            new_wem_name = ubulk_file[:-6] + '.wem'
            new_wem_path = os.path.join(ubulk_folder, new_wem_name)
            shutil.copyfile(wem_file, new_wem_path)
            os.remove(ubulk_path)
            print(f'Replaced {ubulk_file} with {new_wem_name}')

def rename_wem_to_ubulk(ubulk_folder, input_wem_file):
    for file_name in os.listdir(ubulk_folder):
        if file_name.endswith('.wem') and file_name != input_wem_file:
            wem_path = os.path.join(ubulk_folder, file_name)
            new_ubulk_name = os.path.splitext(file_name)[0] + '.ubulk'
            new_ubulk_path = os.path.join(ubulk_folder, new_ubulk_name)
            os.rename(wem_path, new_ubulk_path)
            print(f'Renamed {file_name} to {new_ubulk_name}')

ubulk_folder = os.getcwd()
input_wem_file = 'input.wem'
replace_ubulk_with_wem(ubulk_folder, input_wem_file)
rename_wem_to_ubulk(ubulk_folder, input_wem_file)
