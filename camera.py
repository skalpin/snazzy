import time

import picamera
import os
from os.path import join

camera = picamera.PiCamera()
class BoothCamera():
	def __init__(self, camera):
		self.camera = camera

	def take(self, img_name):
		currentDir = os.getcwd()
		outputDir = "%s/%s/" % (currentDir, timeMillis)

		img_path = "%s%s.jpg" % (outputDir, image_name)
		camera.capture(img_path, use_video_port=False)
		return img_path


	
