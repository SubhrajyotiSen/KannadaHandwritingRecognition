import sys	
import numpy
import scipy
import scipy.misc
from PIL import Image


# TODO: loop over all images
filename = sys.argv[1]

# main formula: http://i.imgur.com/wA7gEks.png

# initialize parameters to be used ( values have been generated after using numerous iterations)
s = 1
lmda = 10
epsilon = 0.0001

# open the image as an array of pixels
X = numpy.array(Image.open(filename))

# avrage value of pixel in original image
X_average = numpy.mean(X)

# scale the value of pixels
X = X - X_average

# calculate overall contrast of image
contrast = numpy.sqrt(lmda + numpy.mean(X**2))

# normalize
X = s * X / max(contrast, epsilon)

# save the image
scipy.misc.imsave(filename + '_contrast.png', X)

