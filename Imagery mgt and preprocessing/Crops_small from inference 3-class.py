import pandas
import cv2 as cv
import os

##Input: path = dir with parent images; csv_data = detection csv from inference
# export_path_[bird/nonbird/artif] = specify folders for each class
path = "D:/images_w_objects_2024/2024_Jan5_parent_images/"
csv_data = pandas.read_csv("D:/YOLO_2024_Jan5_detections.csv")
export_path_bird = "D:/detection_crops_for_inference_2024/2024_Jan5_bird_crops/"
export_path_nonbird = "D:/detection_crops_for_inference_2024/2024_Jan5_nonbird_crops/"
export_path_artif = "D:/detection_crops_for_inference_2024/2024_Jan5_artif_crops/"

os.mkdir(export_path_bird)
os.mkdir(export_path_nonbird)
os.mkdir(export_path_artif)

csv_data.columns = (['class', 'score', 'xmin', 'ymin', 'w', 'h', 'unique_image_jpg', 'unique_BB'])
#print(csv_data)

dirs = os.listdir(path)  # get all files in folder
print(len(dirs))

# Get all of the image names without the path
file_list = []
for file in dirs:
    basename = os.path.splitext(file)[0] + ".jpg"  # take basename (not path) and add .jpg
    # print(basename)
    file_list.append(basename)

matches = csv_data[csv_data['unique_image_jpg'].isin(file_list)]
print(len(matches))

for index, row in matches.iterrows():  ## iterrows: Pandas iterate over rows
    new_path = path + row['unique_image_jpg']  # +'.jpg'
    print(new_path)
    temp1 = cv.imread(new_path, cv.IMREAD_COLOR)  # this is good

    temp1.shape
    x = row['xmin'] - 10
    if x < 0:
        x = 0
    y = row['ymin'] - 10
    if y < 0:
        y = 0

    cat1 = row['class']
    print(cat1)
    w = row['w'] + 20
    h = row['h'] + 20
    # print(xmin_box, ymin_box, xmax_box, ymax_box)

    # Specify each class name below (cat1, cat2, etc.)
    if cat1 == "bird":
        export_path = export_path_bird
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])
        temp5 = export_path + row['unique_BB'] + '.jpg'

    if cat1 == "nonbird":
        export_path = export_path_nonbird
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "manmade":
        export_path = export_path_artif
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])
    print("writing!")