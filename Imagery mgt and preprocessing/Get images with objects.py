import pandas
import os
import csv
import shutil

# This script is best used after a detection model has been run
# The script searches a directory (root_dir) and copies/moves parent images that contain an object to another folder.
# These parent images must be already identified in a csv file.

# Images are moved/copied to a new folder to reduce unnecessary data storage. If files are moved, the result
# will be a directory with images with objects and a root_dir with empty images; the input is a csv file with a list of parent images
# with objects in a column named "unique_image_jpg"

# Data inputs:
# csv data=list of parent images w objects (column header of unique_image_jpg), root_dir = dir of images, dest1 = folder for images w objects
csv_data = pandas.read_csv(
    "C:/Users/bpickens/Desktop/SACR_detection/RESULTS/survey_results/birds_per_jpg_yolov5x_survey_5_or_less.csv")
print(csv_data)
root_dir = "C:/Users/bpickens/Desktop/SACR_detection/RESULTS/survey_results/sacr_yolov5x_survey_visuals_June6"
dest1 = "C:/Users/bpickens/Desktop/SACR_detection/RESULTS/survey_results/sacr_yolov5_survey_conf10_less5birds/"

for index, row in csv_data.iterrows():
    target = row['unique_image_jpg']

    for folders, subfolders, files in os.walk(root_dir):
        if target in files:
            source = os.path.join(folders, target)
            print('Source', source)
            shutil.move(source, dest1)  # this can be changed to: shutil.move
            print ('Moved!!!')
        else:
            pass
            # print('Not moved')