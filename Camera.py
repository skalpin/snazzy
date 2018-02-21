WIDTH = 1280
HEIGHT = 960
FRAMERATE = 24
import picamera
from time import sleep
from ResourceQueue import ResourceQueue

class CameraHandlerInterface():
	def init_camera(self):
		raise NotImplementedError
	def release_camera(self):
		raise NotImplementedError

class CameraHandler(CameraHandlerInterface):
	def init_camera(self):
		print('init camera')
		camera = picamera.PiCamera()
		camera.resolution = (WIDTH, HEIGHT)
		camera.framerate = FRAMERATE
		sleep(1) # camera warm-up time
		self._camera = camera
		self._camera_queue = ResourceQueue('camera', self._camera)
		self._camera_converter = Popen([
			'avconv',
			'-f', 'rawvideo',
			'-pix_fmt', 'yuv420p',
			'-s', '%dx%d' % camera.resolution,
			'-r', str(float(camera.framerate)),
			'-i', '-',
			'-f', 'mpeg1video',
			'-b', '800k',
			'-r', str(float(camera.framerate)),
			'-'],
			stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
			shell=False, close_fds=True)
	def release_camera(self):
		self._camera.__exit__(None, None, None)
		self._camera_queue.stop()
	def camera_queue_get(self):
		if self._camera == None:
			self.init_camera()
		return self._camera_queue

class Camera(CameraHandler):
	pass
