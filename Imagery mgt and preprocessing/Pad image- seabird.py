import os
from PIL import Image, ImageOps

## Inputs: dir_images = directory for parent images; tiles_export = directory to export tiles to

source_images = "C:/Users/bpickens/Desktop/Hive batch2 images above 50birds/"
export_path = "C:/users/bpickens/desktop/Hive_batch2_test/"

def pad_this (img):
    pad_w = 352
    pad_h = 134
    temp1 = Image.open(img)
    padding = (pad_w, pad_h, pad_w, pad_h)
    pad_img = ImageOps.expand(temp1, padding)
    pad_img.save (export_path + img, quality = 95)
    print ("padded!")

# Loop to implement
os.chdir(source_images)

for im in os.listdir(source_images):
    pad_this(im)