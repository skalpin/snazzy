from Camera import Camera
from WebSocket import WebSocket

class Booth(Camera, WebSocket):
	def start(self):
		self.init_camera()
		self.init_webSocket()
	def stop(self):
		self.release_camera()
		self.release_webSocket()
