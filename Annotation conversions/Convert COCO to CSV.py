import os
import pandas as pd
import json

# Inputs: working_dir= working directory, filename = name of coco json file that needs converted ;
# final_csv = output csv file
# The output csv will not contain images without annotations; to obtain those, please check the output of
# "...names_toCSV" file

working_dir = "C:/Users/bpickens/Desktop/test_coco"
filename = "hive_batch2_COCO.json"
final_csv = "converted_json_to_csv.csv"

# Set working directory
os.chdir(working_dir)

### STEP 1- EXPORT ANNOTATION DATA
# Outputs annotation data and image id index number
def convert_coco_json_to_csv(filename):
    js = json.load(open(filename, 'r'))  # read & parse JSON string and convert it to a Python Dictionary
    out_file = filename[:-5]
    out = open(out_file + '_json_data_to_CSV.csv', 'w')  # open for writing to file
    out.write('image_id, x_min,y_min,w,h,label_id \n')  #

    all_ids = []
    for im in js['images']:
        all_ids.append(im['file_name'])

    all_ids_ann = []
    for ann in js['annotations']:
        image_id = ann['image_id']
        # print(image_id)
        all_ids_ann.append(image_id)
        label_id = ann['category_id']
        all_ids_ann.append(label_id)
        #  print(label)
        x_min = ann['bbox'][0]
        #   print (x_min)
        all_ids_ann.append(x_min)
        y_min = ann['bbox'][1]
        all_ids_ann.append(y_min)
        w = ann['bbox'][2]
        all_ids_ann.append(w)
        h = ann['bbox'][3]
        all_ids_ann.append(h)

        out.write('{},{},{},{},{},{}\n'.format(image_id, x_min, y_min, w, h, label_id))

    all_ids = set(all_ids)
    all_ids_ann = set(all_ids_ann)
    no_annotations = list(all_ids - all_ids_ann)
    out.close()

## STEP 2- EXPORT CSV WITH IMAGE NAMES, IMAGE ID NUMBERS
def convert_coco_names_to_csv(csv_file):
    s = json.load(open(filename, 'r'))  # read & parse JSON string and convert it to a Python Dictionary
    out_file = filename[:-5]
    out2 = open(out_file + '_names_toCSV.csv', 'w')  # open for writing to file
    out2.write('image_id, unique_image_jpg \n')  #

    all_data = []
    for ann in s['images']:
        id = ann['id']
        # print (id)
        all_data.append(id)
        unique_image_jpg = ann['file_name']
        #  print(unique_image_jpg)
        all_data.append(unique_image_jpg)
        out2.write('{},{} \n'.format(id, unique_image_jpg))

# Run functions to get 2 csv files
convert_coco_json_to_csv(filename)
convert_coco_names_to_csv(filename)

# Read in; 1st, Erase extra image names at end of "data to csv" file
prefix = filename[:-5]
csv_names= ("".join([prefix,"_names_toCSV.csv"]))
csv_data = ("".join([prefix,"_json_data_to_CSV.csv"]))

csv_names = pd.read_csv(csv_names)
csv_data = pd.read_csv(csv_data)

# Merge
merge1 = csv_data.merge(csv_names, left_on= 'image_id', right_on = 'image_id' )
#print (merge1)
merge1.to_csv(final_csv, index=False)