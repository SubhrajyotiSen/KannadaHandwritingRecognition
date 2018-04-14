import os
import sys	
import cv2
import numpy as np
import ntpath
from PIL import Image

# TODO: loop over all images
imageName = sys.argv[1]
fileName = filename = os.path.splitext(ntpath.basename(imageName))[0]

folder = "Segmented_" + filename	# Creating new folder to save the preprocessed images 
newfolder = os.path.join(os.getcwd(),folder) 
if not os.path.exists(newfolder): # Check if subfolder already exists
	os.makedirs(newfolder)

# open image using openCV
image = cv2.imread(imageName)

# grayscale the image
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# get threshold for pixel values
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

# dilate the image
kernel = np.ones((5,40), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
#im=Image.fromarray(img_dilation,'L')
#im.show()
# find contours

im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# For debbuging and seeing segments in a line
#for cnt in ctrs:
#	x,y,w,h = cv2.boundingRect(cnt)
#	cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),1)
#image2=Image.fromarray(gray,'L')
#image2.show()

# sort contours
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
sorted_ctrs = sorted_ctrs[0:]

for i, ctr in enumerate(sorted_ctrs):
	# Get bounding box
	x, y, w, h = cv2.boundingRect(ctr)
	# Used to remove stray elements
	if ((w*h)<1000):
		continue
	# Getting ROI
	roi = image[y:y+h, x:x+w]

	# save each segmented image
	cv2.imwrite(os.path.join(newfolder, 'word' + str(i) + '.png'), roi)