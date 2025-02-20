import torch
import PIL
from PIL import Image
from torchvision import transforms
import csv
from os.path import basename
import os
import shutil
import pandas

# Inputs:
# drive path = e.g., "D:/"
# flight_name = name of flight folder
# crops_to_export = for annotation, with be ".../crops_w_context_birds/ ; for small crops type:
drive_path = "D:/"
flight_name = "20250210_120000"
crops_to_export = "D:/20250210_120000/crops_w_context_birds/"

# Optional inputs (if new model is applied): idx_to_label = index to the corresponding label in the model
# model_path = pytorch classification model saved as script file
# transform_test = transform to be applied prior to inference
# small_crops = directory of images to apply inference to
model_path = 'C:/users/bpickens/desktop/MODELS FOR USE/2024_Nov20_swin_s_augment15_focal_scripted.pt'
prob_threshold = 1.0
small_crops = drive_path + flight_name + "/" + "crops_inference_birds/"

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device") # must print "Using cuda device" to work

classify_csv = drive_path + flight_name + "/" + "classify_" + flight_name + ".csv"
classify_export_path = drive_path + flight_name + "/" + "classify/"

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

with open(classify_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['unique_image_jpg', 'label1', 'label2', 'score1', 'score2'])

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
    label1 = top3_label[0, 0]
    label2 = top3_label[0, 1]
    score1 = top3_prob[0, 0]
    score2 = top3_prob[0, 1]
    label1 = label1.data.cpu().numpy()
    label2 = label2.data.cpu().numpy()
    if label1 > 26 or label2 > 26:
        label1 = 26
        label2 = 26

    score1 = score1.data.cpu().numpy()
    score2 = score2.data.cpu().numpy()
    species_list = list(idx_to_label.values())

    label1 = species_list[label1]
    label2 = species_list[label2]

    print(label1, label2)

    with open(classify_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, label1, label2, score1, score2])
x=0
for root, dirs, files in os.walk(small_crops):
    for file in files:
        source = os.path.join(root, file)
        name = os.path.basename(source)
        x= x+1
        print("Processing: ", x)
        classify(model, transform_test, source)
    else:
        pass

# This part does the moving
dirs = os.listdir(crops_to_export)  # get all files in folder

csv_data = pandas.read_csv(classify_csv)

for index, row in csv_data.iterrows():
    score1 = row['score1']
    if score1 <  prob_threshold:
        target = crops_to_export + row['unique_image_jpg']  # +'.jpg'
        cat1 = row['label1']

        for folders, subfolders, files in os.walk(crops_to_export):
            name = basename(target)
            if name in files:
                dir2 = classify_export_path + row['label1']
                if not os.path.exists(dir2):
                    os.makedirs(dir2)
                dest = classify_export_path + row['label1'] + '/' + name

                print ("Destination : ", dest)
                shutil.copy(target, dest)  # this can be changed to: shutil.move
            else:
                pass
    else:
        pass
