import time

import picamera
import os
from os.path import join

camera = picamera.PiCamera()

def warmup(width, height):
	camera.resolution = (width, height)
	camera.start_preview()
	camera.exposure_mode = 'sports'
	#camera.sharpness = 100
	#camera.image_effect = 'washedout'
	#camera.image_effect_params = (10, 128, 128)
	#camera.color_effects = (10, 0)
	#warmup camera
	time.sleep(5)

def take(num, width, height):
	timeMillis = str(int(time.time()))
	os.mkdir(timeMillis)
	currentDir = os.getcwd()
	outputDir = "%s/%s/" % (currentDir, timeMillis)
	captured_paths = []
	
	camera.resolution = (width, height)		
	for i in range(num):
		img_path = "%s%d.jpg" % (outputDir, i)
		camera.capture(img_path, use_video_port=False)
		captured_paths.append(img_path)

	return captured_paths

def done():
	camera.close()


	
