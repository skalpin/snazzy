from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from wsgiref.simple_server import make_server
from struct import Struct
from threading import Thread
native_str = str
str = type('')

WIDTH = 1280
HEIGHT = 960
WS_PORT = 8084
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct(native_str('>4sHH'))

class StreamingWebSocket(WebSocket):
	def opened(self):
		self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)

class WebSocketInterface():
	def init_webSocket(self):
		raise NotImplementedError
	def release_webSocket(self):
		raise NotImplementedError

class WebSocketHandler(WebSocketInterface):
	def init_webSocket(self):
		websocket_server = make_server(
			'', WS_PORT,
			server_class=WSGIServer,
			handler_class=WebSocketWSGIRequestHandler,
			app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket))
		websocket_server.initialize_websockets_manager()
		self._websocket_thread = Thread(target=websocket_server.serve_forever)
		self._websocket_server = websocket_server
		self._websocket_thread.start()
	def release_webSocket(self):
		self._websocket_server.shutdown()
		self._websocket_thread.join()

class WebSocket(WebSocketHandler):
	pass
