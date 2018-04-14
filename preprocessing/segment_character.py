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

def segment_character(image):

	ret,thresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
	ret,thresh2 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
	im2,ctrs, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	(ctrs, boundingBoxes) = sort_contours(ctrs, method="left-to-right")

	characters = []

	# For each contour, find the bounding rectangle and draw it
	for i,cnt in enumerate(ctrs):
		x,y,w,h = cv2.boundingRect(cnt)

		# Ignore small contours - Considered to be unwanted elements
		if ((w*h)<100):
			continue
		
		# Find the segmented character and store
		roi = thresh2[y:y+h, x:x+w]

		characters.append(roi)

	return characters
		

