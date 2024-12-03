import pandas as pd
import numpy as np
import glob
import os
from skimage import io

# Input: files = directory of files, export_csv = csv that reports brightness
files = glob.glob("C:/users/bpickens/desktop/SACR_detection/images/*.jpg")

export_csv = "C:/users/bpickens/desktop/SACR_detection/brightness_test2.csv"

mean_list = []
image_list = []
for file in files:
    print(file)
    file1 = os.path.basename(file)
    img = io.imread(file)
    mean_list.append(np.max(img))
    image_list.append(file1)

pd.DataFrame({"unique_image": image_list, "mean": mean_list}).to_csv(export_csv, index=True)