import pandas as pd
import os
import shutil

# The script searches a image directory and copies/moves images that are listed in a csv file
# the csv file should have column labeled as "unique_image_jpg"

# Data inputs:
# csv data= list of images to be copied/moved (column header of 'unique_image_jpg')
# root_dir = directory of images to search
# dest1 = destination folder to move/copy images into

csv_data = pd.read_csv("C:/users/bpickens/desktop/Crops/remove.csv")
root_dir = "C:/users/bpickens/desktop/removed"
dest1 = "C:/users/bpickens/desktop/removed2/"

x=1

csv_list = []
csv_list = csv_data['unique_image_jpg'].tolist()
# print(csv_list)

for root, dirs, files in os.walk(root_dir):
    for filename in files:
        if filename in csv_list:
            x = x + 1
            print ("Copied: ", x)
            path = os.path.join(root, filename)
            print ("path " , path)
            shutil.copy(path, dest1)  # can be shutil.move or shutil.copy
            print('Moved!!!')
        else:
            pass

