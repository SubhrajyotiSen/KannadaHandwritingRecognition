import os
import sys
import cv2

image = sys.argv[1]
filename = filename = os.path.splitext(image)[0]

# open image using openCV
img = cv2.imread(image)

# denoise image
dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

# save image
cv2.imwrite(filename + '_denoise.png', dst)
