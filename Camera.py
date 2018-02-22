import picamera
from time import sleep
from ResourceQueue import ResourceQueue
import os
import assemble

class Camera():
	def __init__(self, config, output):
		self._config = config
		self._output = output
		print('init camera')
		camera = picamera.PiCamera()
		camera.resolution = (self._config.WIDTH, self._config.HEIGHT)
		camera.framerate = self._config.FRAMERATE
		sleep(1) # camera warm-up time
		self._camera = camera
		self._camera_queue = ResourceQueue('camera', self._camera)
		self.converter = output.converter
	def release_camera(self):
		self._camera.__exit__(None, None, None)
		self._camera_queue.stop()
	def start_recording(self):
		self._camera.start_recording(self._output, 'yuv')
	def stop_recording(self):
		self._camera_queue.add(lambda cam: cam.stop_recording())
	def capture_image(self, image_name):
		currentDir = os.getcwd()

		img_path = "%s/%s.jpg" % (currentDir, image_name)
		print('image path:' + img_path)
		#should maybe be done on queue
		self._camera.capture(img_path, use_video_port=True)
		return util.process(img_path, assemble.get_height_each())
	def assemble(self, session_images):
		filename = assemble.assemble(session_images)
		print('saved file ', filename)
		#printer.print_file(filename)
