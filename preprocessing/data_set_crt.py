from joblib import Parallel, delayed
from PIL import Image, ImageChops, ImageOps, ImageFilter
from scipy import misc
from scipy.misc import toimage
from skimage import io, filters, transform
from skimage.morphology import skeletonize_3d
from skimage.util import random_noise
import cv2
import glob
import numpy as np
import os
import PIL
import scipy
import sys
import time

'''
	This program is used to augment and original data set 
	It increase the total number of images in the data set
	The augmentation includes change in the following mathods
	1) Change in aspect ratio, Output ratio: 1:2
	2) Change in rotaion with +15 degree, Output ratio: 1:1 
	3) Change in rotaion with -15 degree, Output ratio: 1:1
	4) Addition of noise to the images, Output ratio: 1:2
	The ordering of the above function and origianl set produces the following
	Ratio of original image to augmented image is 1:10

'''

start_time = time.time()
rootdir = sys.argv[1]
size = sys.argv[2]
res = int(size)
ori = os.getcwd()
count = 0


def gaussianresize(image):
    global res
    ori = os.getcwd()
    path = ori + '/' + image
    img = io.imread(path)
    img = np.invert(img)
    img = filters.gaussian(img, 3, multichannel=True)
    img = transform.resize(img, (res, res), mode='constant')
    misc.imsave(path, img)


def fixedsize(image):
    ori = os.getcwd()
    path = ori + '/' + image
    img = io.imread(path)
    # img = np.invert(img)
    img = transform.resize(img, (208, 208), mode='constant')
    misc.imsave(path, img)


def denoise(image):
    img = cv2.imread(image)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    cv2.imwrite(image, img)


def GaussianBlur(image): 		# Used for plane images
    img = io.imread(image, as_grey=True)
    img = random_noise(img, mode='salt')
    img = misc.toimage(img)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    img.save(image)


def noise(image):
    image2 = misc.imread(image, mode="L")
    noisy1 = image2 + 1 * image2.std() * np.random.random(image2.shape)
    img = Image.fromarray(noisy1)
    img = img.convert("L")
    img.save("n"+image)


def contrast(image):
    s = 1
    lmda = 10
    epsilon = 0.0001
    X = np.array(Image.open(image))
    X_average = np.mean(X)
    X = X - X_average
    contrast = np.sqrt(lmda + np.mean(X**2))
    X = s * X / max(contrast, epsilon)
    scipy.misc.imsave(image, X)


def thin(image):				# Used for thining images
    img = cv2.imread(image, 0)
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    skeleton = skeletonize_3d(thresh)
    img = toimage(skeleton)
    img.save(image)


def rtl(image):
    img = Image.open(image)
    img2 = img.convert('RGBA')
    theta = [15]
    for i in range(0, len(theta)):
        rot = img2.rotate(theta[i], resample=Image.BILINEAR, expand=True)
        fff = Image.new('RGBA', rot.size, (255,)*4)
        out = Image.composite(rot, fff, rot)
        out = out.convert(img.mode)
        out.save(str(theta[i])+"L"+image)


def rtr(image):
    img = Image.open(image)
    img2 = img.convert('RGBA')
    theta = [15]
    for i in range(0, len(theta)):
        rot = img2.rotate(-theta[i], resample=Image.BILINEAR, expand=True)
        fff = Image.new('RGBA', rot.size, (255,)*4)
        out = Image.composite(rot, fff, rot)
        out = out.convert(img.mode)
        out.save(str(theta[i])+"R"+image)


def ht(image):
    img = Image.open(image)
    new_img = img.resize((156, 208))
    new_img.save("a1"+image)
    new_img = img.resize((208, 156))
    new_img.save("a2"+image)


def size208(image):
    desired_size = 208
    im = Image.open(image).convert('L')
    old_size = im.size
    ratio = float(208)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    im = im.resize(new_size, Image.ANTIALIAS)
    new_im = Image.new("RGB", (208, 208))
    new_im = PIL.ImageOps.invert(new_im)
    new_im.paste(im, ((208-new_size[0])//2, (208-new_size[1])//2))
    new_im.save(image)


def blur(image):
    img = cv2.imread(image, 0)
    blurred = cv2.blur(img, (5, 5))
    cv2.imwrite(image, blurred)


def crop(image):
    img = Image.open(image)
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        img = img.crop(bbox)
        img.save(image)


def padding(image):
    old_im = Image.open(image)
    old_size = old_im.size
    new_size = ((old_size[0]+100), (old_size[1]+100))
    new_im = Image.new("RGB", new_size)
    new_im = ImageOps.invert(new_im)
    new_im.paste(old_im, (int((new_size[0]-old_size[0])/2),
                          int((new_size[1]-old_size[1])/2)))
    new_im.save("pad"+image)
    os.remove(image)


def binerize(image):
    img = cv2.imread(image, 0)
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(image, thresh)


def binerize_inv(image):
    img = cv2.imread(image, 0)
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(image, thresh)


for root, dirs, files in os.walk(rootdir, topdown=False):
    # Sorts the dires by number
    dirs.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for name in dirs:
        if not os.path.isdir(os.path.join(rootdir, name)):
            continue
        dir3 = os.path.join(root, name)
        os.chdir(os.path.abspath(dir3))

        flist = glob.glob('*.jpg')
        # Crops all the original image for faster processing
        Parallel(n_jobs=-1)(delayed(crop)(n) for n in flist)
        Parallel(n_jobs=-1)(delayed(fixedsize)(n)
                            for n in flist)			# Resizes all images to fixed size
        Parallel(n_jobs=-1)(delayed(denoise)(n)
                            for n in flist)			# Removes noise from all images
        Parallel(n_jobs=-1)(delayed(contrast)(n)
                            for n in flist)			# Increase contrast for all images
        flist1 = glob.glob('*.jpg')
        Parallel(n_jobs=-1)(delayed(ht)(n)
                            for n in flist1)				# Augmentation: changes the aspect ratio
        # Augmentation: rotates the image to the left
        Parallel(n_jobs=-1)(delayed(rtl)(n) for n in flist1)
        # Augmentation:	rotates the image to the right
        Parallel(n_jobs=-1)(delayed(rtr)(n) for n in flist1)
        flist2 = glob.glob('*.jpg')
        # Smoothing: first binerize to remove stray noise
        Parallel(n_jobs=-1)(delayed(binerize)(n) for n in flist2)
        # Smoothing: blur to smooth the pixelated edges
        Parallel(n_jobs=-1)(delayed(blur)(n) for n in flist2)
        # Smoothing: second binerize to get clear output
        Parallel(n_jobs=-1)(delayed(binerize)(n) for n in flist2)
        flist3 = glob.glob('*.jpg')
        # Croping since rotated images have added padding
        Parallel(n_jobs=-1)(delayed(crop)(n) for n in flist3)
        Parallel(n_jobs=-1)(delayed(padding)(n)
                            for n in flist3)			# Adding fixed padding to all images
        flist4 = glob.glob('*.jpg')
        Parallel(n_jobs=-1)(delayed(size208)(n)
                            for n in flist4)			# Resizing to redues line cuts
        flist5 = glob.glob('*.jpg')
        # Resize to ML specification and adds gaussian blur
        Parallel(n_jobs=-1)(delayed(gaussianresize)(n) for n in flist5)
        Parallel(n_jobs=-1)(delayed(noise)(n)
                            for n in flist5)			# Adds noise to all images and renames

        # Used to prevent lose of images when over wirting with same name
        flist6 = glob.glob('*.jpg')
        coount = 10000
        for n in flist6:
            os.rename(n, str(coount) + ".jpg")
            coount += 1
        flist7 = glob.glob('*.jpg')
        coount = 0
        for n in flist7:							# Used to rename the files from 0 to n
            os.rename(n, str(coount) + ".jpg")
            coount += 1

        flist8 = glob.glob('*.jpg')
        count += len(flist8)
        print("number of images in", name, ":", len(flist8))
        os.chdir(ori)

end_time = time.time()
seconds = end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
if count == 0:
    print("No new folders to process")
else:
    print("=============================================")
    print("total number of images created:", count)
    print("Total time: %dH:%02dM:%02dS" % (h, m, s))
