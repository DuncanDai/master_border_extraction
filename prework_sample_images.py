#!/usr/bin/python3 
import os 
from shutil import copy

# env: ubuntu
old_path = r'/media/dinggen/hdd1/Image'
new_path = r'/home/dinggen/Documents/Proj_KITMA/kitma/images'
# new_path = r'smb://192.168.1.102/d/My_Data/me_Docs/Masterarbeit/images' # different platform: error

# Get the directories 
sub_dirs = os.listdir(old_path)
dirs_num = len(sub_dirs)

for sub_dir in sub_dirs:
    print(f'The subdirectory is {sub_dir}.')
    src_path = os.path.join(old_path, sub_dir)
    dst_path = os.path.join(new_path, sub_dir)

    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)
    
    files = [f for f in os.listdir(src_path)]   # output of os.listdir(src_path) is a list of 'XXX.png'
    files_num = len(files)
    # choose 20 images in each directory/folder
    choose_files_index = list(range(0, files_num, files_num//19))

    for index in choose_files_index:
        src_file = os.path.join(src_path, files[int(index)])
        copy(src_file, dst_path)