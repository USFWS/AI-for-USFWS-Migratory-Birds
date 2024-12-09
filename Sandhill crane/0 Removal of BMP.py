import glob
import os
import shutil

# Inputs: input path = path to directory of images, export_path = directory to move bmp's into
input_path = "D:/SACR_2023_imagery/Nontargets_2023_20March/20230320_202500/**/*.bmp"
export_path = "D:/SACR_2023_imagery/all_bmp"

dirs = os.listdir(input_path)

for f in glob.glob(input_path, recursive=True):
    print(input_path)
    shutil.move(f, export_path)