import sys
import os
import ntpath

from preprocessing.segmentation import segment
from preprocessing.augment import augment

from CNN.recognize_character import recognize

from Unicode.seqgen import sequenceGen
from Unicode.printdoc import unicode_to_kn

def analyze(image):
	
	# directory name to store the segmented image
	dir = 'Segmented_' + os.path.splitext(ntpath.basename(image))[0]

	# call the segmentation script on the image
	segment(image)

	# augment each of the segmented images
	augment(dir)

	# recognize all images in the directory
	predictions = recognize(os.path.join(os.getcwd(),dir))

	# generate the Unicode sequence based on predictions
	sequence = sequenceGen(predictions)

	# generate Kannada text from the Unicode sequence
	kannada_text = unicode_to_kn(sequence)

	# return the Kannada text
	return(kannada_text)

	
	



