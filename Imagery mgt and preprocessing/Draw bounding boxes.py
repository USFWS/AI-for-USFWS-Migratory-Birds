import pandas
import cv2 as cv
import os

## If the image_path and export path are the same, boxes will overwrite until an image has all of its boxes
# Inputs: annotations = csv of annotations with xmin, ymin, w, h
#######   image_path = path to source imagery
#####     export_path = path to export new images

annotations = 'E:/2023_May12_all_ducks/export_train.csv'
image_path = 'E:/2023_May12_all_ducks/train_good2/'
export_path = image_path

annotations = pandas.read_csv(annotations)
#annotations.columns = (['image_id', 'xmin', 'ymin', 'w', 'h', 'label_id', 'unique_image_jpg'])

for index, row in annotations.iterrows():  ## iterrows: Pandas iterate over rows
    source_path = image_path + row['unique_image_jpg']

    input = cv.imread(source_path, cv.IMREAD_COLOR)  # this
    print("source: ", source_path)
    check = os.path.exists(source_path)
    if check == True:
        xmin = row['xmin'] - 3
        ymin = row['ymin'] - 3
        w = row['w'] + 6
        h = row['h'] + 6
        xmax = xmin + w
        ymax = ymin +h
        print(xmin, ymin, w, h)

### Allows for different colors for different classes
       class_index = row['class_index']

        if class_index ==0:
            cv.rectangle (input, (xmin, ymin), (xmax, ymax), (0, 255, 0))
            new_name = export_path + row['unique_image_jpg']
            print("ducks: ", new_name)
            cv.imwrite(new_name, input, [int(cv.IMWRITE_JPEG_QUALITY), 95])

        if class_index ==1:
            cv.rectangle (input, (xmin, ymin), (xmax, ymax), (255, 0, 0))
            new_name = export_path + row['unique_image_jpg']
            print("cranes: ", new_name)
            cv.imwrite(new_name, input, [int(cv.IMWRITE_JPEG_QUALITY), 95])

