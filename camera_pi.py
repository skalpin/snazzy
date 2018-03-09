import io
import os
import time
import picamera
from base_camera import BaseCamera
from Session import Session
import util
import assemble
import printer

class Camera(BaseCamera):
	def __init__(self, config):
		self._camera = None
		self._config = config
		self._session = None

	def new_session(self, color_choice):
		if color_choice == 'regular':
			color = None
		elif color_choice == 'bw':
			color = (128, 128)
		elif color_choice == 'sepia':
			color = (100, 155)

		if self._camera != None:
			self._camera.color_effects = color

		self._session = Session(color)

	def frames(self):
		self.get_camera()
		stream = io.BytesIO()
		for _ in self._camera.capture_continuous(stream, 'jpeg', use_video_port=True, resize=(640, 480)):
			# return current frame
			stream.seek(0)
			yield stream.read()

			# reset stream for next frame
			stream.seek(0)
			stream.truncate()

	def get_camera(self):
		while self._session == None:
			time.sleep(0)
		self._camera = picamera.PiCamera()
		self._camera.hflip = self._config.HFLIP
		self._camera.vflip = self._config.VFLIP
		self._camera.resolution = (self._config.WIDTH, self._config.HEIGHT)
		self._camera.framerate = self._config.FRAMERATE
		self._camera.color_effects = self._session.color_choice

	# Called after a timeout is reached in the base
	def close(self):
		self._camera.close()
		self._camera = None

	def capture(self, picnum):
		currentDir = os.getcwd()
		img_path = "%s/%s.jpg" % (currentDir, picnum)
		print('image path:' + img_path)
		self._camera.capture(img_path, splitter_port=1)
		image = util.process(img_path, assemble.get_height_each())
		self._session.session_images.append(image)

	def assemble(self):
		print('assembling images')
		filename = assemble.assemble(self._session.session_images)
		printer.print_file(filename)
		#clear out the session images
		self._session = None
