from WebSocket import WebSocket
import Config
from camera_pi import Camera
from BroadcastOutput import BroadcastOutput
import picamera

class Factory():
	@classmethod
	def Config(cls):
		return Config
	@classmethod
	def WebSocket(cls):
		return cls.singleton('_websocket', lambda:WebSocket(cls.Config(), cls.Camera()))
	@classmethod
	def BroadcastOutput(cls):
		return cls.singleton('_broadcastoutput', lambda:BroadcastOutput(cls.Config()))
	@classmethod
	def Camera(cls):
		return cls.singleton('_camera', lambda:Camera(cls.Config()))

	@classmethod
	def singleton(cls, name, d):
		if not hasattr(cls, name):
			setattr(cls, name, d())
		return cls.__dict__[name]
