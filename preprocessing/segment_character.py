import cv2
import numpy as np
import os
import sys
import ntpath

""" To sort the contours in 4 ways
		left-to-right
		right-to-left
		top-to-bottom
		bottom-to-top
"""

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
 
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
 
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
 
	# construct the list of bounding boxes and sort them from top to bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

if __name__ == '__main__':
	# TODO: loop over all images
	imageName = sys.argv[1]
	j=0
	# Creating new folder to save the preprocessed images
	fileName = filename = os.path.splitext(ntpath.basename(imageName))[0]
	folder = "Segmented_Char_" + filename	
	newfolder = os.path.join(os.getcwd(),folder) 
	if not os.path.exists(newfolder): # Check if subfolder already exists
		os.makedirs(newfolder)

	image = cv2.imread(imageName)
	# convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
	ret,thresh2 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
	# debug1=Image.fromarray(thresh,'L')
	# debug1.show()

	kernel = np.ones((5,5), np.uint8)
	img_dilation = cv2.dilate(thresh, kernel, iterations=1)
	im2,cnts, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	(cnts, boundingBoxes) = sort_contours(cnts, method="left-to-right")

	# For each contour, find the bounding rectangle and draw it
	for i,cnt in enumerate(cnts):
		x,y,w,h = cv2.boundingRect(cnt)
		# Ignore small contours - Considered to be unwanted elements
		if ((w*h)<100):
			continue
		print(w*h)
		# Find the segmented character and store
		roi = thresh2[y:y+h, x:x+w]
		cv2.imwrite(os.path.join(newfolder, 'Letter' + str(j) + '.png'), roi)
		j+=1
