from skimage.morphology import skeletonize_3d
from skimage import color
import cv2
from skimage.util import invert
from scipy.misc import toimage

# Read and store image
image = sys.argv[1]
filename = filename = os.path.splitext(image)[0]
image = cv2.imread(imageName, 0)
# The given image should be in Grayscale or Binary format
# skeletonize_3d assumes White as foreground and black as background.
# Hence we invert the image (This can be removed based on what form of input images we decide to provide at later stage)
image = color.rgb2gray(invert(image))
# skeletonize_3d is mainly used for 3D images but can be used for 2D also.
# Advantage - Removes spurs and provides better output
skeleton = skeletonize_3d(image)

# Saving output image
im = toimage(skeleton)
im.save(filename + "_skeletonised.png")

# show image
cv2.imshow("skeleton", skeleton)
cv2.waitKey(0)
