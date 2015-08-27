from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
import util
import sys
import time

padding_percent = 5

width_inches = 4
height_inches = 6
resolution = 300

width_px = width_inches * resolution
height_px = height_inches * resolution


padding = 40

#height_each = (height_px - padding * 4) / 3.0
height_each = 520
width_each = 480


background = Image(width=width_px, height=height_px, background=Color('white'))

def get_height_each():
	return height_each

def assemble(images):
	util.composite_all(background, images, padding, height_each, width_each)

	#display(background)
	background.save(filename='out' + str(int(time.time())) + '.jpg')


