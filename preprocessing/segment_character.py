import cv2
import numpy as np
import os
import sys

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
	
	# Creating new folder to save the preprocessed images
	fileName = filename = os.path.splitext(imageName)[0]
	folder = "Segmented_Char_" + filename	
	
	newfolder = os.path.join(os.getcwd(),folder) 
	if not os.path.exists(newfolder): # Check if subfolder already exists
		os.makedirs(newfolder)
	image = cv2.imread(imageName)
	# convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	
	# smooth the image to avoid noises
	gray = cv2.medianBlur(gray,5)
	
	# Apply adaptive threshold
	thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
	thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
	
	
	# Find the contours
	im2,cnts,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	
	# Get sorted contours
	(cnts, boundingBoxes) = sort_contours(cnts, method="left-to-right")
	
	# For each contour, find the bounding rectangle and draw it
	for i,cnt in enumerate(cnts):
		x,y,w,h = cv2.boundingRect(cnt)
		# Ignore small contours - Considered to be unwanted elements
		print(w*h)
		if ((w*h)<500):
			continue
	
		# Find the segmented character and store
		roi = image[y:y+h, x:x+w]
		cv2.imwrite(os.path.join(newfolder, 'segment' + str(i) + '.png'), roi)
