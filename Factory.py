from WebSocket import WebSocket
import Config
from Camera import Camera
from BroadcastOutput import BroadcastOutput

class FactoryType(type):
	@property
	def Config_get(cls):
		if getattr(cls, '_config', None) is None:
			cls._config = Config
		return cls._config

	@property
	def Camera_get(cls):
		if getattr(cls, '_camera', None) is None:
			cls._camera = Camera(cls._config)
			print(cls._camera)
		return cls._camera

	@property
	def WebSocketServer_get(cls):
		if getattr(cls, '_websocketserver', None) is None:
			cls._websocketserver = WebSocket(cls._config, Camera_get)
		return cls._websocketserver

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
