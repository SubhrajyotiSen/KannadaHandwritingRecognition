from PIL import Image, ImageChops
import sys
import os 
import glob
import time
from joblib import Parallel, delayed

start_time = time.time()
rootdir = sys.argv[1]
ori = os.getcwd()
count = 0
"""
	The function below does the following:
	1) Rotate the image to the LEFT based in theta value
	2) Changes the new background to white
	3) Crops the image generated
	4) Saves the image 

"""
def rtl(im):
	img = Image.open(im)			
	img2 = img.convert('RGBA')
	theta = [10,15,20]
	for i in range(0,len(theta)):
		#print(theta[i])
		rot = img2.rotate(theta[i], resample=Image.BILINEAR,expand=True)
		fff = Image.new('RGBA', rot.size, (255,)*4)
		out = Image.composite(rot, fff, rot)
		out = out.convert(img.mode)
		bg = Image.new(out.mode, out.size, out.getpixel((0,0)))
		diff = ImageChops.difference(out, bg)				 
		diff = ImageChops.add(diff, diff, 2.0, -100)		 
		bbox = diff.getbbox()		
		if bbox:
			out = out.crop(bbox)
		out.save(str(theta[i])+"_L_"+im)

"""
	The function below does the following:
	1) Rotate the image to the RIGHT based in theta value
	2) Changes the new background to white
	3) Crops the image generated
	4) Saves the image 

"""
def rtr(im):
	img = Image.open(im)
	img2 = img.convert('RGBA')
	theta = [10,15,20]
	for i in range(0,len(theta)):
		#print(theta[i])
		rot = img2.rotate(-theta[i], resample=Image.BILINEAR,expand=True)
		fff = Image.new('RGBA', rot.size, (255,)*4)
		out = Image.composite(rot, fff, rot)
		out = out.convert(img.mode)
		bg = Image.new(out.mode, out.size, out.getpixel((0,0)))
		diff = ImageChops.difference(out, bg)				 
		diff = ImageChops.add(diff, diff, 2.0, -100)		 
		bbox = diff.getbbox()		
		if bbox:
			out = out.crop(bbox)
		out.save(str(theta[i])+"_R_"+im)

"""
	The function below does the following:
	1) Resizes the image as aspect_1 (64*128)
	2) Resizes the image as aspect_2 (128*64)
	3) Crops the image generated
	4) Saves the image 

"""
def ht(im):
	img = Image.open(im)
	new_img = img.resize((64,128))
	new_img.save("aspect_1_"+im)
	new_img = img.resize((128,64))
	new_img.save("aspect_2_"+im)

for root,dirs,files in os.walk(rootdir,topdown=False):
	for name in dirs:
		dir3 = os.path.join(root,name) 
		os.chdir(os.path.abspath(dir3))
		flist = glob.glob('*.jpg')
		Parallel(n_jobs=-1)(delayed(rtl)(n) for n in flist)
		Parallel(n_jobs=-1)(delayed(rtr)(n) for n in flist)
		os.chdir(ori)

for root,dirs,files in os.walk(rootdir,topdown=False):
	for name in dirs:
		dir3 = os.path.join(root,name) 
		os.chdir(os.path.abspath(dir3))
		flist = glob.glob('*.jpg')
		# changes the aspect ratio of all new images
		Parallel(n_jobs = -1)(delayed(ht)(n) for n in flist)
		flist2 = glob.glob('*.jpg')
		count += len(flist2)
		print ("number of images in ",name,": ",len(flist2))
		os.chdir(ori)

end_time = time.time()	# Used to stop time record
seconds=end_time - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print ("Total time: %dH:%02dM:%02dS" % (h, m, s))
print("total number of images created: ",count)
