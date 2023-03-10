'''
This script will create a grid of images and overlay the filenames. It is
useful for quickly compiling numerous images together into a single file.
'''

import os
import numpy as np
from skimage import io
import cv2

# Set the path to the directory containing the images
image_dir = 'D:/Brumell Lab Dropbox/Andrew Sydor/Andrew Sydor/Trainee Projects/James- Rab10/Correlative/Summer 2022 FIB-SEM Sample/Correlation/Run 2/Flow Denoising/Tests/TrakEM2 First'

# Set the number of rows and columns in the grid
num_rows = 13
num_cols = 5

# Get the filenames of all the images in the directory
image_filenames = os.listdir(image_dir)

# Create an empty list to store the images and the filenames
images = []
tif_filenames = []

# Load slice 33 from each image and add it to the list
slice = 33 # change slice number here

for filename in image_filenames:
    # Ensure that the image is a tif stack
    if filename.endswith('.tif'):
        img = io.imread(os.path.join(image_dir, filename))
        img_33 = img[slice,:,:]
        images.append(img_33)
        tif_filenames.append(filename)

# Get the dimensions of the largest image
max_width = max(image.shape[1] for image in images)
max_height = max(image.shape[0] for image in images)

# Create a new image to hold the grid of images and filenames
# The +50 is to allow for the addition of whitespace between each image.
grid_image = np.ones((num_rows * (max_height + 50), num_cols * (max_width + 50)), dtype=np.uint8) * 255

# Add the filenames to the bottom of each image
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        if index < len(images):
            image = images[index] #retrieve image
            filename = tif_filenames[index] # retrieve filename
            width = image.shape[1]
            height = image.shape[0]
            # adjust the image placement such that we have whitespace (50 px) added around each image
            x = j * (max_width + 50) + 25 + (max_width - width) // 2
            y = i * (max_height + 50) + 25 + (max_height - height) // 2
            grid_image[y:y+height, x:x+width] = image
            # Add the filename at the top of the image
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1
            thickness = 2
            color = (255,255,255) # white
            text_size, _ = cv2.getTextSize(filename, font, font_scale, thickness)
            text_x = x + (width - text_size[0]) // 2
            text_y = y + 25
            cv2.putText(grid_image, filename, (text_x, text_y), font, font_scale, color, thickness)

# Save the grid image
io.imsave('SPGF_tests-Run2-afterTrakEM2.png', grid_image)
