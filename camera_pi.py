import io
import time
import picamera
from base_camera import BaseCamera

class Camera(BaseCamera):
	def __init__(self):
		self._camera = None
	def frames(self):
		self._camera = picamera.PiCamera()
		stream = io.BytesIO()
		for _ in self._camera.capture_continuous(stream, 'jpeg', use_video_port=True):
			# return current frame
			stream.seek(0)
			yield stream.read()

			# reset stream for next frame
			stream.seek(0)
			stream.truncate()
	def close(self):
		self._camera.close()
	def capture(self, picnum):
		print('capturing an image %s' % picnum)
	def assemble(self):
		print('assembling images')
