from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
import util
import sys
import datetime

padding_percent = 5

width_inches = 4
height_inches = 6
resolution = 600

width_px = width_inches * resolution
height_px = height_inches * resolution


padding = 80

#height_each = (height_px - padding * 4) / 3.0
#height_each = 520
#width_each = 480

#height_each = 520
#width_each = 480
height_each = 1040
width_each = 960




def get_height_each():
	return height_each

def assemble_outisde():
	print('assemble in another process')
	images = [];
	images.append(util.process('1.jpg', 1040))
	images.append(util.process('2.jpg', 1040))
	images.append(util.process('3.jpg', 1040))

	filename = assemble(images)
	print('assemble success!')

def assemble(images):
	print('background')
	print(width_px)
	print(height_px)
	background = Image(width=width_px, height=height_px, background=Color('white'))
	print('util.composite')
	util.composite_all(background, images, padding, height_each, width_each)
	print('background.transform')
	background.transform(str(width_px)+'x'+str(height_px), '95%')
	print('with image')
	underlay = Image(width=width_px, height=height_px, background=Color('white'))
	print('underlay.composite_channel')
	underlay.composite_channel('default_channels', background, 'over', int(width_px * 0.025), int(height_px * 0.025))
	print('constructing file name')
	filename = 'out' + str(datetime.datetime.now()) + '.jpg'
	print('underlay.save')
	underlay.save(filename=filename)
	print('return ' + filename)
	return filename


