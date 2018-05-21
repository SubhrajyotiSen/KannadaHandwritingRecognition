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
import random  # Module to generate random numbers

start_time = time.time()  # Used to start time record
rootdir = sys.argv[1]		# Take input as path to root of dataset
# Take input as number of images to put into validation set
validation_size = sys.argv[2]
ori = os.getcwd()				# Save current directory for looping stage
folder = "valid"     # Creating new folder to save the preprocessed images
# Creating the path to the new folder
newfolder = os.path.join(os.path.dirname(ori), folder)
if not os.path.exists(newfolder):  # Check if directory already exists
    os.makedirs(newfolder)  # Making new directory


def getRandomFile(path):
    """
    Returns a random filename, chosen among the files of the given path.
    """
    files = os.listdir(path)
    index = random.randrange(0, len(files))
    return files[index]


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
        # We	make a path with'name' to the new folder
        subfolder = os.path.join(newfolder, name)
        if not os.path.exists(subfolder):  # Check if subfolder already exists
            os.makedirs(subfolder)  # We make the folder
        # The cropped images have been saved in the same folder as original images
        # We will now move them to the new folder in there specified subfolder
        src = os.getcwd() 	# source directory is the path of the  subfolder we are currently in
        dst = subfolder 	# The destination is the new subfolder created
        # We make a loop which iterates through each files in the directory
        print(src)
        for x in range(30):
            f1 = getRandomFile(src)
            src_file = os.path.join(src, f1)  # Path to source file
            dst_file = os.path.join(dst, f1)  # Path to destination file
            if os.path.exists(dst_file):		# prior to processing with this program
                os.remove(dst_file)			# Basic overwiter function
            # This makes usre we only move those files and overwrite if it existes
            shutil.move(src_file, dst_file)
        os.chdir(subfolder)
        # Creats a list of files that end with '.png' later we can add '.PNG'
        flist = glob.glob('*.jpg')
        # The function below is used to parallelize the image processing
        # n_jobs is the number of cores to use (-1 is all cores)
        # Delayed is used to run the function 'ct' with argument 'n' from list 'flist'
        print("done with ", name)  # Once done with
        # At the end of the loop we move back to original directory so that looping can start again
        os.chdir(ori)

end_time = time.time()  # Used to stop time record
seconds = end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print("Total time: %dH:%02dM:%02dS" % (h, m, s))
