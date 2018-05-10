import sys
import os
import ntpath

from preprocessing.segmentation import segment
from preprocessing.augment import augment

from CNN.recognize_character import recognize
from CNN.ottakshara_dict import ottakshara_mapping 

from Unicode.seqgen import sequenceGen
from Unicode.printdoc import unicode_to_kn

def analyze(image):

	# directory name to store the segmented image
	dir = 'Segmented_' + os.path.splitext(ntpath.basename(image))[0]

	# call the segmentation script on the image
	segment(image)

	# augment each of the segmented images
	augment(dir)

	# sort the list of image names alphabetically
	flist = os.listdir(dir)
	flist.sort()

	predictions = {}

	# iterate through each image and predict its class
	for file in flist:
		# if image is an ottakshara
		if '-1' in file:
			predictions[file] = ottakshara_mapping[recognize(os.path.abspath(os.path.join(dir, file)),'ottakshara')]
		#if image in a regular character
		else:
			predictions[file] = recognize(os.path.abspath(os.path.join(dir, file)),'other')

	# generate the Unicode sequence based on predictions
	sequence = sequenceGen(predictions)

	# generate Kannada text from the Unicode sequence
	kannada_text = unicode_to_kn()

	# return the Kannada text
	return(kannada_text)

	
	



