import os
from PIL import Image

## Inputs: input_path = dir of orignal images; export_path = dir to place resized images
# new_width = width of crop in pixels, new_height = height of crop in pixels
new_width = 224
new_height = 224
input_path = "F:/AMAPPS_CLASSIFY/winter_train_crops"
export_path = "F:/AMAPPS_CLASSIFY/winter_train_crops_224x_224/"
os.mkdir(export_path)

def batch_resize (img):
    for name in os.listdir (input_path):
        source = os.path.join(input_path, name)
        print(source)
        input = Image.open(source)
        resize_img = input.resize((new_width, new_height), Image.Resampling.BICUBIC) # Resize by width and height
        resize_img.save (export_path + name, quality = 95)

# Loop to implement
for img in input_path:
    batch_resize(img)
print("done!")