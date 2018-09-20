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

def assemble(images):
	print('in assemble')
	print('background')
	background = Image(width=width_px, height=height_px, background=Color('white'))
	print('util composite_all')
	util.composite_all(background, images, padding, height_each, width_each)
	print('background again')
	background.transform(str(width_px)+'x'+str(height_px), '95%')
	with Image(width=width_px, height=height_px, background=Color('white')) as underlay:
		underlay.composite_channel('default_channels', background, 'over', int(width_px * 0.025), int(height_px * 0.025))
		#filename = '/media/pi/PICSTORE/BoothPhotos/' + str(datetime.datetime.now()).replace(":","") + '.jpg'
		filename = 'out' + str(datetime.datetime.now()) + '.jpg'
		underlay.save(filename=filename)
		return filename


