import pandas
import cv2 as cv
import os
import torch
import PIL
from PIL import Image
from torchvision import transforms
import csv
import shutil

## Inputs: root_path = root directory, flight_name = flight folder, model_path = model to apply
root_path = "D:/"
flight_name = "20250125_123300"
model_path = 'C:/users/bpickens/Desktop/MODELS FOR USE/2024_Nov20_swin_s_augment15_focal_scripted.pt'

# Optional inputs, available to narrow down the results by probability
max_prob_threshold = 1.0
min_prob_threshold = 0.0

## Automated paths
jpg_path = root_path + flight_name + "/JPG_" + flight_name + "/"
detection_results = root_path + flight_name + "/Metadata_" + flight_name + "_detections.csv"
detection_results = pandas.read_csv(detection_results)

# crops with context exports
export_path_bird = root_path + flight_name + "/crops_w_context_birds/"
export_path_nonbird = root_path + flight_name + "/crops_w_context_nonbird/"
export_path_artif = root_path + flight_name + "/crops_w_context_artif/"

if not os.path.exists(export_path_bird):
    os.mkdir(export_path_bird)
if not os.path.exists(export_path_nonbird):
    os.mkdir(export_path_nonbird)
if not os.path.exists(export_path_artif):
    os.mkdir(export_path_artif)

# crops for inference
export_path_bird_i = root_path + flight_name + "/crops_inference_birds/"
export_path_nonbird_i = root_path + flight_name + "/crops_inference_nonbird/"
export_path_artif_i = root_path + flight_name + "/crops_inference_artif/"
image_dir = export_path_bird_i

# new_csv = path/name of csv file of results to export
# image_dir = directory of images to apply inference to
# root_export = directory where species folders are set up
# crop_dir = for annotation, point towards crops with context; otherwise can be image_dir
# Optional (if new model is applied): idx_to_label = index to the corresponding label in the model
# transform_test = transform to be applied prior to inference
new_csv = root_path + flight_name + "/classify_" + flight_name + ".csv"
root_export = root_path + flight_name + "/classification_results/"
print("export", root_export)
crop_dir = export_path_bird

if not os.path.exists(export_path_bird_i):
    os.mkdir(export_path_bird_i)
if not os.path.exists(export_path_nonbird_i):
    os.mkdir(export_path_nonbird_i)
if not os.path.exists(export_path_artif_i):
    os.mkdir(export_path_artif_i)
if not os.path.exists(root_export):
    os.mkdir(root_export)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device") # must print "Using cuda device" to work

detection_results.columns = (['unique_image_jpg', 'class', 'score', 'xmin', 'ymin', 'w', 'h', 'unique_BB'])
dirs = os.listdir(jpg_path)  # get all files in folder

# Get all of the image names without the path
file_list = []
for file in dirs:
    basename = os.path.splitext(file)[0] + ".jpg"  # take basename (not path) and add .jpg
    file_list.append(basename)

matches = detection_results[detection_results['unique_image_jpg'].isin(file_list)]
print("matches with csv: ", len(matches))

for index, row in matches.iterrows():  ## iterrows: Pandas iterate over rows
    new_path = jpg_path + row['unique_image_jpg']  # +'.jpg'
    print("Source: ", new_path)
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

    xmin_box = row['xmin'] - 15
    if xmin_box < 0:
        xmin_box = 0
    ymin_box = row['ymin'] - 15
    if ymin_box < 0:
        ymin_box = 0
    xmax_box = row['xmin'] + row['w'] + 15
    ymax_box = row['ymin'] + row['h'] + 15
    # print(xmin_box, ymin_box, xmax_box, ymax_box)

    # (x, y starting points), (x,y end points)
    cv.rectangle(temp1, (xmin_box, ymin_box), (xmax_box, ymax_box), (0, 255, 0))

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
    temp2 = cv.imread(new_path, cv.IMREAD_COLOR)
    temp2.shape
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
# Make it square? Or not
#    if w > h:
 #       h = w
  #  else:
   #     w = h
    # print(xmin_box, ymin_box, xmax_box, ymax_box)

    # Specify each class name below (cat1, cat2, etc.)
    if cat1 == "bird" or cat1 == 1:
        export_path = export_path_bird_i
        crops = temp2[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "nonbird" or cat1 == 3:
        export_path = export_path_nonbird_i
        crops = temp2[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

    if cat1 == "manmade" or cat1 == 2:
        export_path = export_path_artif_i
        crops = temp2[y:(y + h), x:(x + w)]
        cv.imwrite(export_path + row['unique_BB'] + '.jpg', crops, [int(cv.IMWRITE_JPEG_QUALITY), 95])

###### Classification inference
# Load model
model = torch.jit.load(model_path)
model.to(device)

transform_test = transforms.Compose([
    transforms.Resize((224,224)), transforms.ToTensor(),
    transforms.Normalize(mean= (0.2335, 0.2444, 0.2143), std=(0.1369,0.1149, 0.1031))
])

idx_to_label = {0: "ATPU", 1:"BCPE",
                            2: "BLSC", 3: "BOGU",
                            4: "BRPE", 5: "BUFF", 6: "CANG", 7: "COEI",
                            8: "COGO", 9: "COLO", 10: "DCCO",
                            11: "GBBG", 12: "HERG",
                            13: "HOGR",
                            14: "LAGU", 15: "LTDU",
                            16: "NOGA", 17: "not_wildlife",
                            18: "RBME", 19: "REDH",
                            20: "ROYT", 21: "RTLO", 22: "SCAU", 23: "SNGO", 24: "SUSC",
                            25: "TUSW", 26: "WWSC", 27: "error"
                           }
species_list = list(idx_to_label.values())

with open(new_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['unique_image_jpg', 'label1', 'label2', 'label3', 'score1', 'score2', 'score3'])

def classify(model, transform_test, source):
    model = model.eval()
    image = PIL.Image.open(source)
    image = transform_test(image).float()
    image = image.to(device)
    image = image.unsqueeze(0)
    output = model(image)
    # print(output.data)
    softmax = torch.nn.functional.softmax(output, dim=1)

    top3_prob, top3_label = torch.topk(softmax, 3)
    # print("tops: ", top3_prob,top3_label)
    label1 = top3_label[0, 0]
    label2 = top3_label[0, 1]
    label3 = top3_label[0, 2]
    score1 = top3_prob[0, 0]
    score2 = top3_prob[0, 1]
    score3 = top3_prob[0, 2]
    label1 = label1.data.cpu().numpy()
    label2 = label2.data.cpu().numpy()
    label3 = label3.data.cpu().numpy()
    print(label1, label2, label3)
    if label1 > 26 or label2 > 26 or label3 > 26:
        label1 = 26
        label2 = 26
        label3 = 26

    score1 = score1.data.cpu().numpy()
    score2 = score2.data.cpu().numpy()
    score3 = score3.data.cpu().numpy()
    species_list = list(idx_to_label.values())

    label1 = species_list[label1]
    label2 = species_list[label2]
    label3 = species_list[label3]

    print(label1, label2, label3)

    with open(new_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, label1, label2, label3, score1, score2, score3])

for root, dirs, files in os.walk(image_dir):
    for file in files:
        source = os.path.join(root, file)
        name = os.path.basename(source)
        #print ("name: ", name)
        classify(model, transform_test, source)
    else:
        pass

# This part does the moving
dirs = os.listdir(crop_dir)  # get all files in folder
detection_results = pandas.read_csv(new_csv)

for index, row in detection_results.iterrows():
    score1 = row['score1']
    print(score1)
    if score1 <  max_prob_threshold and score1 > min_prob_threshold:
        target = crop_dir + row['unique_image_jpg']  # +'.jpg'
        print('Target : ', target)
        cat1 = row['label1']
        print("Class: ", cat1)

        for folders, subfolders, files in os.walk(crop_dir):
            base = os.path.basename(target)
            if base in files:
                dir2 = root_export + row['label1']
                print("okay")
                if not os.path.exists(dir2):
                    os.makedirs(dir2)
                dest = root_export + row['label1'] + '/' + name

                print ("Destination : ", dest)
                shutil.copy(target, dest)  # this can be changed to: shutil.move
            else:
                pass
    else:
        print("Too high!")


