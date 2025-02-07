
import pandas as pd
import os
import shutil

# The script searches a image directory and copies/moves images that are listed in a csv file
# the csv file should have column labeled as "unique_image_jpg"

# Data inputs:
# root_dir = directory of images to search
# dest1 = destination folder to move/copy images into

root_dir = "D:/Boresight/photos2"
dest1 = "D:/Boresight/monroe_photos/"

for root, dirs, files in os.walk(root_dir):
    print (files)
    for filename in files:
        if filename.endswith(".jpg"):
            filepath = os.path.join(root, filename)
            print(filepath)
            export_path = dest1 + filename
            shutil.copy(filepath, export_path)