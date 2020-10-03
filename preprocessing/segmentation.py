import os
import ntpath
import cv2

from preprocessing.segment_sentence import segment_sentence
from preprocessing.segment_word import segment_word
from preprocessing.segment_character import segment_character


def segment(file):
    rootdir = 'web_app/hwrkannada/hwrapp/static/hwrapp/images/Processed_' + \
        os.path.splitext(ntpath.basename(file))[0]
    # Generate directory name to store segmented images
    directory = rootdir + '/Segmented_' + \
        os.path.splitext(ntpath.basename(file))[0]

    # Check if subfolder already exists. If it doesn't, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Read the image as numpy array
    image = cv2.imread(file)

    # Get sentences as separate images
    sentences = segment_sentence(image, directory)

    for i in range(0, len(sentences)):
        # Get words as separate images
        words = segment_word(sentences[i], directory, i)

        for j in range(0, len(words)):
            # Get characters as separate images
            characters, ottaksharas = segment_character(words[j], directory)

            """ 
					Generate image name based on position in original image
				 	Format is LL-WW-CC-X where
				 		LL is line number
				 		WW is word number in LL
				 		CC is character number in WW
				 		X = 0 for regular character, 1 for ottakshara
			"""
            for key in characters:

                imageName = str(i+1).zfill(2) + '-' + str(j+1).zfill(2) + \
                    '-' + str(key+1).zfill(2) + '-0' + '.png'

                # save image
                cv2.imwrite(os.path.join(
                    directory, imageName), characters[key])

            for key in ottaksharas:

                imageName = str(i+1).zfill(2) + '-' + str(j+1).zfill(2) + \
                    '-' + str(key+1).zfill(2) + '-1' + '.png'

                # save image
                cv2.imwrite(os.path.join(directory, imageName),
                            ottaksharas[key])
