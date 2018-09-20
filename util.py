from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

def crop_square_center(image):
	width = image.width
	height = image.height
	print((width - height) / 2)
	image.crop(width=height, height=height, left=int((width - height)/2), top=0)

def crop_center(image, width, height):
	image_width = image.width
	image_height = image.height
	image.crop(width=width, height=height, left=(image_width - width)/2, top=(image_height-height)/2)

def crop_resize(image, size):
	image.resize(int(size), int(size))
	crop_center(image, width, height)


def overlay():
	with Image(filename="booth_background.png") as overlay:
		with Image(filename="0.jpg") as underlay:
			underlay.composite_channel('default_channels', overlay, 'over', 0, 0)
			underlay.save(filename="composited.jpg")

def blur_edges(image, border):
	rect = Image(width=image.width, height=image.height, background=Color('white'))
	drawing = Drawing()

	drawing.rectangle(left=border, top=border, width=image.width - 2 * border, height=image.height - 2 * border, radius=100)
	drawing(rect)
	rect.negate()

	rect.gaussian_blur(radius=10, sigma=15)

	with Drawing() as draw:
		draw.composite('multiply', 0, 0, image.width, image.height, rect)
		draw(image)

def process(path, height_each):
	image = Image(filename=path)
	crop_square_center(image)
	image.resize(width=1040, height=960)
	return image

def composite_all(background, images, padding, width_each, height_each):
	print('first column')
	#First column
	print('first column image 1')
	background.composite(images[0], padding, padding)
	print('first column image 2')
	background.composite(images[1], padding, int(height_each + padding * 2))
	print('first column image 3')
	background.composite(images[2], padding, int(height_each * 2 + padding * 3))

	print('second column')
	#Second column
	col2_padding = int(padding * 3 + width_each)

	print('second column image 1')
	background.composite(images[0], col2_padding, padding)
	print('second column image 2')
	background.composite(images[1], col2_padding, int(height_each + padding * 2))
	print('second column image 3')
	background.composite(images[2], col2_padding, int(height_each * 2 + padding * 3))

	print('with image background as overlay')
	with Image(filename="booth_background.png") as overlay:
		print('overlay.resize')
		overlay.resize(width=overlay.width*2, height=overlay.height*2)
		print('composite all background.composite_channel')
		background.composite_channel('default_channels', overlay, 'over', 0, 0)

