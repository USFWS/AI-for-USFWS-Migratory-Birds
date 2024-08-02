import pandas
import cv2 as cv
import os

# Inputs: path = dir with parent images with objects in them; export_path = dir for object crops
path = "F:/AMAPPS_CLASSIFY/winter_parent_images/"
export_path ="F:/AMAPPS_CLASSIFY/winter_object_crops/"

# Input csv file with unique_image_jpg, xmin, ymin, w, and h of annotation; check on data types
csv_data = pandas.read_csv("F:/AMAPPS_CLASSIFY/train_test_grouped3.csv")
datatypes = csv_data.dtypes

# change data type as needed
csv_data['w'] = csv_data['w'].astype('int64')
# datatypes

dirs = os.listdir(path)
file_list = []
for file in dirs:
    basename = os.path.splitext(file)[0] + ".jpg"  # take basename (not path) and add .jpg
    file_list.append(basename)
matches = csv_data[csv_data['unique_image_jpg'].isin(file_list)]

for index, row in matches.iterrows():
    new_path = path + row['unique_image_jpg']  # +'.jpg'
    # print(new_path)
    temp1 = cv.imread(new_path, cv.IMREAD_COLOR)
    temp1.shape
    x = row['xmin'] - 10  # this number can be adjusted, depending on the desired buffer size around the object
    if x < 0:
        x = 0
    y = row['ymin'] - 10  # this number can be adjusted, depending on the desired buffer size around the object
    if y < 0:
        y = 0
    w = row['w'] + 20  # this number can be adjusted, depending on the desired buffer size around the object
    print(w)
    h = row['h'] + 20  # this number can be adjusted, depending on the desired buffer size around the object
    # print(xmin_box, ymin_box, xmax_box, ymax_box)

    crops = temp1[y:(y + h), x:(x + w)]
    cv.imwrite(export_path + row['object_id_jpg'], crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])
    temp5 = export_path + row['object_id_jpg']
    print(temp5)