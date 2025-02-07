import cv2
import glob
import os
import numpy
import skimage
from skimage.exposure import is_low_contrast
import pandas as pd

# Input: files = directory of files, export_csv = csv that reports brightness
files = glob.glob("C:/Brad/a_detection_of_seabirds/images_w_objects_cvat_reviewed/*.jpg")
export_csv = "C:/Brad/a_detection_of_seabirds/results image_character_cvat.csv"

mean_list = []
image_list = []
contrast_list = []
x=0
for file in files:
    x= x+1
    print(x)
    file1 = os.path.basename(file)
    img = cv2.imread(file)
    mean_list.append(numpy.mean(img))
    image_list.append(file1)
    # add below
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contrast = gray.std()
    contrast_list.append(contrast)

    #if (is_low_contrast(gray, 0.03)):
     #   low_contrast_list.append ("low contrast")
    #else:
     #   low_contrast_list.append("normal contrast")

pd.DataFrame({"unique_image": image_list, "mean": mean_list, "contrast": contrast_list}).to_csv(export_csv, index=True)
