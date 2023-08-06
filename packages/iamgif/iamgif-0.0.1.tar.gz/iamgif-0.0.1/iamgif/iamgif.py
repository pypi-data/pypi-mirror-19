from image2gif import writeGif

import PIL.Image
import PIL.ImageDraw
import PIL.ImageSequence

import os


def create(text, dir_path):

	img = PIL.Image.new('RGB', (800, 800), (255, 255, 255))
	d = PIL.ImageDraw.Draw(img)

	os.mkdir(dir_path+'/tempdir')

	ctr = 1
	images = []

	for i in range(len(text)):
	    d.text((10, 10), text[:ctr], fill=(0, 0, 0))
	    img.save(dir_path+"/tempdir/"+str(ctr)+".png", "png")
	    images.append(PIL.Image.open(dir_path+"/tempdir/"+str(ctr)+".png"))
	    ctr = ctr + 1

	writeGif(dir_path+'/animation.gif', images, duration=0.1)

	os.system('rm -R ' + dir_path+'/tempdir')