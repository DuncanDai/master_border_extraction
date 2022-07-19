import os 
from shutil import copy

old_path = r'/media/dinggen/hdd1/Image'
new_path = r'/home/dinggen/Documents/Proj_KITMA/kitma/images'
# new_path = r'smb://192.168.1.102/d/My_Data/me_Docs/Masterarbeit/images' # different platform: error

# choose_files = range()

# Get 
sub_dirs = os.listdir(old_path)
dirs_num = len(sub_dirs)
for sub_dir in sub_dirs:
    print(f'The subdirectory is {sub_dir}.')
    src_path = os.path.join(old_path, sub_dir)
    dst_path = os.path.join(new_path, sub_dir)

    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)
    break

    
    




