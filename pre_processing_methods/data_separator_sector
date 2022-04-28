import os
import json
import shutil

# utility imports
from tqdm import tqdm

'''
===================================================================================================================
METHOD: (folders_in)
yields all directories within a directory
===================================================================================================================
'''


def folders_in(dir_path):
    for fname in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, fname)):
            yield os.path.join(dir_path, fname)


'''
===================================================================================================================
METHOD: (separate_data)
Will iterate over all content of a directory and 

PARAMS:
dir_path:   path to directory containing the questions you want to process
dest_path:  destination directory where the language separated data will be stored
debug:      indicate if debug logging is activated
===================================================================================================================
'''


def separate_data(dir_path, dest_path, debug=False):
    dirs = [dir_path]
    while len(dirs) > 0:
        next_dir_path = dirs[0]
        separate_data_helper(next_dir_path, dest_path)

        # check if dir contains other dirs and add these to the dirs list
        dirs.extend(list(folders_in(next_dir_path)))
        dirs.remove(next_dir_path)
    
    # print some statistics
    if debug:
        total_count = 0
        for lang_dir in os.listdir(dest_path):
            lang_dir_path = os.path.join(dest_path, lang_dir)
            print(lang_dir + ": " + str(len([name for name in os.listdir(
                lang_dir_path) if os.path.isfile(os.path.join(lang_dir_path, name))])))
            total_count += len([name for name in os.listdir(
                lang_dir_path) if os.path.isfile(os.path.join(lang_dir_path, name))])
        print("TOTAL COUNT: " + str(total_count))


'''
===================================================================================================================
METHOD: (separate_data_helper)
helper method for sector separation

PARAMS:
dir_path:   path to directory containing the questions you want to process
dest_path:  destination directory where the language separated data will be stored
===================================================================================================================
'''


def separate_data_helper(dir_path, dest_path):

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    if os.path.isdir(dir_path):
        pbar = tqdm(os.listdir(dir_path))
        for file_name in pbar:
            try:
                file_path = os.path.join(dir_path, file_name)
                if not os.path.isdir(file_path):
                    sector_name = "__default__"
                    with open(file_path) as file:
                        try:
                            json_file = json.load(file)
                            sector_name = json_file["Metadata"]["Sector"]
                        except:
                            sector_name = "__default__"

                    dest_folder_path = os.path.join(dest_path, sector_name)
                    if not os.path.exists(dest_folder_path):
                        os.makedirs(dest_folder_path)

                    dest_file_path = os.path.join(dest_folder_path, file_name)
                    shutil.copyfile(file_path, dest_file_path)
                    pbar.set_description("")
            except:
                pbar.set_description(file_name + " was not processed")

'''
d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(d)
# Example usage
temp = os.path.join(d, "Language Seperated Questions")
src = os.path.join(temp, "en")
dest = os.path.join(d, "English Sector Separated")
dirs = os.listdir(src)
separate_data(src, dest, True)
'''