import pandas
import cv2 as cv
import os

##Input: image_path = dir with parent images; csv_data = detection csv from inference
# export_path_[bird/nonbird/artif] = specify folders for each class
image_path = "F:/2023_Jan11_090400/"
csv_data = pandas.read_csv("F:/2023_Jan11_090400_YOLO8.csv")

# crops with context exports
export_path_bird = "F:/crops_w_context_bird_test/"
export_path_nonbird = "F:/crops_w_context_nonbird_test/"
export_path_artif = "F:/crops_w_context_artif_test/"

# crops for inference
# crops with context exports
export_path_bird_i = "F:/inference_crops_bird_test/"
export_path_nonbird_i = "F:/inference_crops_nonbird_test/"
export_path_artif_i = "F:/inference_crops_artif/"

if not os.path.exists(export_path_bird_i):
    os.mkdir(export_path_bird_i)

if not os.path.exists(export_path_nonbird_i):
    os.mkdir(export_path_nonbird_i)

if not os.path.exists(export_path_artif_i):
    os.mkdir(export_path_artif_i)

csv_data.columns = (['unique_image_jpg', 'class', 'score', 'xmin', 'ymin', 'w', 'h', 'unique_BB'])
# print(csv_data)

dirs = os.listdir(image_path)  # get all files in folder
print("image path: ", len(dirs))

# Get all of the image names without the path
file_list = []
for file in dirs:
    basename = os.path.splitext(file)[0] + ".jpg"  # take basename (not path) and add .jpg
   # print(basename)
    file_list.append(basename)

matches = csv_data[csv_data['unique_image_jpg'].isin(file_list)]
print("matches with csv: ", len(matches))

for index, row in matches.iterrows():  ## iterrows: Pandas iterate over rows
    new_path = image_path + row['unique_image_jpg']  # +'.jpg'
    print(new_path)
    temp1 = cv.imread(new_path, cv.IMREAD_COLOR)  # this is good

    temp1.shape
    x = row['xmin'] - 400
    if x < 0:
        x = 0
    y = row['ymin'] - 200
    if y < 0:
        y = 0

    w = row['w'] + 800  # given that x, y are already set back by 10
    h = row['h'] + 400
    cat1 = row['class']
    print(cat1)

    xmin_box = row['xmin'] - 10
    if xmin_box < 0:
        xmin_box = 0
    ymin_box = row['ymin'] - 10
    if ymin_box < 0:
        ymin_box = 0
    xmax_box = row['xmin'] + row['w'] + 10
    ymax_box = row['ymin'] + row['h'] + 10
    # print(xmin_box, ymin_box, xmax_box, ymax_box)

    # (x, y starting points), (x,y end points)
    cv.rectangle(temp1, (xmin_box, ymin_box), (xmax_box, ymax_box), (0, 255, 0))

    ############# INPUT HERE
    if cat1 == "bird" or cat1 == 1:
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path_bird + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "nonbird" or cat1 == 3:
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path_nonbird + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "manmade" or cat1 == 2:
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path_artif + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    ## Crops for inference
   # new_path2 = path + row['unique_image_jpg']  # +'.jpg'
    #temp1 = cv.imread(new_path2, cv.IMREAD_COLOR)  # this is good

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
    if cat1 == "bird" or cat1 == 1:
        export_path = export_path_bird_i
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "nonbird" or cat1 == 3:
        export_path = export_path_nonbird_i
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "manmade" or cat1 == 2:
        export_path = export_path_artif_i
        crops = temp1[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])
