from math import sqrt
import sys
import cv2
import numpy as np
import os
# Blob_log is used for blob detection in an image.
from skimage.feature import blob_log
from skimage.color import rgb2gray
from PIL import Image, ImageDraw

j = 0  # Count for image name.
Original_img = sys.argv[1]
image = cv2.imread(Original_img)
image_gray = rgb2gray(image)

filename = os.path.splitext(Original_img)[0]

# Creating new folder to save the preprocessed images.
folder = "Segmented_" + filename
newfolder = os.path.join(os.getcwd(), folder)
if not os.path.exists(newfolder): 	# Check if subfolder already exists.
    os.makedirs(newfolder)

# List of blobs in an image.
blobs_log = blob_log(image_gray, max_sigma=10, num_sigma=25, threshold=.01)
# Now we draw the blobs on the image.
blob_img = Image.open(Original_img)
draw = ImageDraw.Draw(blob_img)
# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
for blob in blobs_log:
    y, x, r = blob
    if r > 5:  # If the radii is lager than 5 units we discard.
        continue
    r = r+5  # Remaning blobs are required and therefore size is increased.
    draw.ellipse((x-r, y-r, x+r, y+r), fill=(0, 0, 0, 255))
# Save the image with blobs drawed.
blob_img.save('blob.png', 'png')
blob_name = 'blob.png'
blob_img_cv = cv2.imread(blob_name)  # Image passed for dilation.
Original_img_cv = cv2.imread(Original_img)  # Image used for cropping words.
gray = cv2.cvtColor(blob_img_cv, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

kernel = np.ones((5, 0), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
# debug1=Image.fromarray(img_dilation,'L')
# debug1.show()
im2, ctrs, hier = cv2.findContours(
    img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# for cnt in ctrs:
# 	x,y,w,h = cv2.boundingRect(cnt)
# 	cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),1)
# debug2=Image.fromarray(gray,'L')
# debug2.show()

sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
sorted_ctrs = sorted_ctrs[0:]

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)
    # Used to remove stray elements
    # print(w*h)
    if ((w*h) < 5000):
        continue
    # Getting ROI
    roi = Original_img_cv[y:y+h, x:x+w]
    cv2.imwrite(os.path.join(newfolder, 'word' + str(j) + '.png'), roi)
    j += 1
os.remove("blob.png")
print("Word segmentation done.")
