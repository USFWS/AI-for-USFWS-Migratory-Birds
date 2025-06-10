import numpy as np
import cv2 as cv
import os

## Inputs: dir_images = directory for parent images; tiles_export = directory to export tiles to
dir_images = "C:/Users/bpickens/Desktop/SACR_detection/temp_parent_images"
tiles_export = "C:/Users/bpickens/Desktop/SACR_detection/temp_tiles/"
#os.chdir("C:/Users/folder")

# Define the function to split the image in half and pad it to make squares; going from 1280x720 pixels to 2 x 736x736 pixel images
def tile_file(file: str):
    img_name = file.split(os.path.sep)[-1].split('.')[0]

    # open image and store as numpy array
    img = cv.imread(file, cv.IMREAD_GRAYSCALE)

    tile_count = 0
    tile_L = img[0:720, 0:640]
    tile_R = img[0:720, 640:1280]
    # np.pad (top, bottom), (left, right), mean/constant/0/etc.
    tile_L_array = np.asarray(tile_L)
    tile_L = np.pad(tile_L_array, [(8, 8), (48, 48)], 'mean')
    tile_R_array = np.asarray(tile_R)
    tile_R = np.pad(tile_R_array, [(8, 8), (48, 48)], 'mean')

    img_new = os.path.basename(img_name)    
    tile_name_L = (tiles_export + img_new + "_tile_L.jpg")
    tile_name_R = (tiles_export + img_new + "_tile_R.jpg")

    print(tile_name_L)
    print(tile_name_R)

    cv.imwrite(tile_name_L, tile_L, [int(cv.IMWRITE_JPEG_QUALITY), 99])
    cv.imwrite(tile_name_R, tile_R, [int(cv.IMWRITE_JPEG_QUALITY), 99])

#items = os.listdir()
#items.remove('desktop.ini')

# Run the function
for (root, _, files) in os.walk(dir_images):
        for file in files:
            path = os.path.join(root, file)
            print(f"Tiling: {file}...")
            tile_file(path)
