from PIL import Image
import os
import sys
import glob
'''
	This script is used to create MNIST like dataset image
	where each row is a character
	rootdir is the source of the image data which is used to create the rows
	no_in_line specifies number of characters to put in each line 
'''
rootdir = sys.argv[1]
ori = os.getcwd()
no_in_line = sys.argv[2]
y_offset = 0

len_dirs = len(os.listdir(rootdir))
final_img = Image.new("L", (52*int(no_in_line), 52*len_dirs))

for root, dirs, files in os.walk(rootdir, topdown=False):
    dirs.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for name in dirs:
        if not os.path.isdir(os.path.join(rootdir, name)):
            continue
        dir3 = os.path.join(root, name)
        os.chdir(os.path.abspath(dir3))

        flist = glob.glob('*.jpg')
        flist.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        flist = flist[:len(no_in_line)]
        lines = Image.new("L", (52*int(no_in_line), 52))

        x_offset = 0
        for im in flist:
            img = Image.open(im)
            lines.paste(img, (x_offset, 0))
            x_offset += 52

        final_img.paste(lines, (0, y_offset))
        y_offset += 52
        os.chdir(ori)
final_img.save(str(rootdir)+'.jpg')
