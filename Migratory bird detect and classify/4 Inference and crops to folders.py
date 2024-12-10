import torch
import PIL
from PIL import Image
#from torch.utils.tensorboard.summary import image
from torchvision import transforms
import csv
from os.path import basename
import os
import shutil
import pandas

# Inputs:
# new_csv = path/name of csv file of results to export
# image_dir = directory of images to apply inference to
# root_export = directory where species folders are set up
# crop_dir = for annotation, point towards crops with context; otherwise can be image_dir
# Optional (if new model is applied): idx_to_label = index to the corresponding label in the model
# model_path = pytorch classification model saved as script file
# transform_test = transform to be applied prior to inference

new_csv = "E:/a_classify_seabirds/classify_brpe.csv"
image_dir = "C:/users/aware/desktop/BRPE_bp/"
root_export = "E:/a_classify_seabirds/classify_results1/"
crop_dir = image_dir

model_path = 'E:/a_classify_seabirds/2024_Nov20_swin_s_augment15_focal_scripted.pt'
prob_threshold = 1.0

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device") # must print "Using cuda device" to work

# load model
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

csv_data = pandas.read_csv(new_csv)

for index, row in csv_data.iterrows():
    score1 = row['score1']
    print(score1)
    if score1 <  prob_threshold:
        print("Okay")
        target = crop_dir + row['unique_image_jpg']  # +'.jpg'
        print('Target : ', target)
        cat1 = row['label1']
        print("Class: ", cat1)

        for folders, subfolders, files in os.walk(crop_dir):
            name = basename(target)
            print ("name: ", name)
            if name in files:
                dir2 = root_export + row['label1']
                if not os.path.exists(dir2):
                    os.makedirs(dir2)
                dest = root_export + row['label1'] + '/' + name

                print ("Destination : ", dest)
                shutil.copy(target, dest)  # this can be changed to: shutil.move
            else:
                pass
    else:
        print("Too high!")
