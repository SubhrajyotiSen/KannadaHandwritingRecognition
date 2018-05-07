import sys
import os
import ntpath

from preprocessing.segmentation import segment
from preprocessing.augment import augment

from CNN.recognize_character import recognize

from Unicode.seqgen import sequenceGen

from ottakshara_dict import ottakshara_mapping 

image = sys.argv[1]
dir = 'Segmented_' + os.path.splitext(ntpath.basename(image))[0]

segment(image)

augment(dir)

flist = os.listdir(dir)
flist.sort()

predictions = {}

for file in flist:
	if '-1' in file:
		predictions[file] = ottakshara_mapping[recognize(os.path.abspath(os.path.join(dir, file)),'ottakshara')]
	else:
		predictions[file] = recognize(os.path.abspath(os.path.join(dir, file)),'other')

predictions = sorted(predictions.items(), key = lambda x : x[1])
predictions = dict((key, value) for (key, value) in predictions)

sequenceGen(predictions)

	
	



