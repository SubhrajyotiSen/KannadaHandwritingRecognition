#!/usr/bin/env python
# This module provides access to some variables used or maintained by the interpreter.
import sys
# This module provides a portable way of using operating system dependent functionality.
import os
# The module offers a number of high-level operations on files and collections of files.
import shutil
import time 	# This module provides various time-related functions.
# The glob module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell.
import glob
# The Python Imaging Library (PIL) adds image processing capabilities to your Python interpreter.
from PIL import Image, ImageChops
# scikit-image is a collection of algorithms for image processing.
from skimage import color
from skimage.morphology import skeletonize_3d
from skimage.util import invert
# Lightweight pipelining: using Python functions as pipeline jobs.
from joblib import Parallel, delayed
import cv2 	# Open CV is uesd image processing
# It provides routines for numerical integration and optimization.
from scipy.misc import toimage

# This function is used to crop and thin the image file
# We pass th 'im' file as a parameter


def ct(im):
    img = Image.open(im)
    # This is used to save a background and save the corner pixel
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    # Which is specified by getpixel(0,0)
    diff = ImageChops.difference(img, bg)
    # Diff holds the difference with main 'im' and 'bg'
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()		# The difference box is generated
    if bbox:					# If the box existes it is saved
        img = img.crop(bbox)
        img.save(im)
    image = cv2.imread(im, 0)
    # The given image should be in Grayscale or Binary format
    # skeletonize_3d assumes White as foreground and black as background.
    # Hence we invert the image (This can be removed based on what form of input images we decide to provide at later stage)
    image = color.rgb2gray(invert(image))
    # skeletonize_3d is mainly used for 3D images but can be used for 2D also.
    # Advantage - Removes spurs and provides better output
    skeleton = skeletonize_3d(image)
    # Saving output image
    image = toimage(skeleton) 	# Takes a numpy array and returns a PIL image
    image.save(im)


start_time = time.time()  # Used to start time record
count = 0 					# Count for no.of files
rootdir = sys.argv[1]		# Take aregument from command line
ori = os.getcwd()				# Save current directory for looping stage
# Creating new folder to save the preprocessed images
folder = "Preprocessed_Images"
# Creating the path to the new folder
newfolder = os.path.join(os.getcwd(), folder)
if not os.path.exists(newfolder):  # Check if directory already exists
    os.makedirs(newfolder)  # Making new directory

# The loop below is used to iterate through each folder and subfolder
# It generats a tupel root,dirs,files
# Root is the current directory
# Dirs is a List of all subfolders in the root
# Files is a List of all files inside each folder
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in dirs: 	# Looping through each folder inside rootdir
        # print("started with ",name) For Debbuging
        # Create new path to the current subfolder in the loop specified by 'name'
        dir3 = os.path.join(root, name)
        # We are moving into the folder specified by dir3 using the absolute path
        os.chdir(os.path.abspath(dir3))
        # Now since we are inside the requied directory we check for images
        # The loop below is used to iterate through each file that ends with '.png' later we can add '.PNG'
        # We make a path with'name' to the new folder
        dst = os.path.join(newfolder, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        # The cropped images have been saved in the same folder as original images
        # We will now move them to the new folder in there specified subfolder
        src = os.getcwd() 	# source directory is the path of the  subfolder we are currently in
        shutil.copytree(src, dst, symlinks=False, ignore=None)
        os.chdir(dst)		# Now we move into the subfolder
        # Creats a list of files that end with '.png' later we can add '.PNG'
        flist = glob.glob('*.png')
        count = count+len(flist)  # Count number of files being processed
        # The function below is used to parallelize the image processing
        # n_jobs is the number of cores to use (-1 is all cores)
        # Delayed is used to run the function 'ct' with aregument 'n' from list 'flist'
        Parallel(n_jobs=-1)(delayed(ct)(n) for n in flist)
        print("done with ", name)  # Once done with
        # At the end of the loop we move back to original directory so that looping can start again
        os.chdir(ori)

end_time = time.time()  # Used to stop time record
seconds = end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print("Total time: %dH:%02dM:%02dS" % (h, m, s))
print("Total number of images processed:", count)
