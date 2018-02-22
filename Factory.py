from WebSocket import WebSocket
import Config
from camera_pi import Camera
from BroadcastOutput import BroadcastOutput

class Factory():
	def __init__(self):
		self._config = None
		self._wss = None
		self._camera = None
		self._broadcast_output = None
	def Config(self):
		if self._config == None:
			self._config = Config
		return self._config
	def Camera(self):
		if self._camera == None:
			self._camera = Camera(self.Config(), self.BroadcastOutput())
		return self._camera
	def WebSocket(self):
		if self._wss == None:
			self._wss = WebSocket(self.Config(), self.Camera())
		return self._wss
	def BroadcastOutput(self):
		if self._broadcast_output == None:
			self._broadcast_output = BroadcastOutput(self.Config())
		return self._broadcast_output
	def Camera(self):
		if self._camera == None:
			self._camera = Camera()
		return self._camera
