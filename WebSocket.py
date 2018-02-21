from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
from wsgiref.simple_server import make_server
from threading import Thread
import socket
import Factory

class StreamingWebSocket(WebSocket):
    def opened(self):
        self.send(Factory.Config.JSMPEG_HEADER.pack(Factory.Config.JSMPEG_MAGIC, Factory.Config.WIDTH, Factory.Config.HEIGHT), binary=True)

class WebSocket():
    def __init__(self,config):
        self._config = config
    def start(self):
        websocket_server = make_server(
                '', self._config.WS_PORT,
                server_class=WSGIServer,
                handler_class=WebSocketWSGIRequestHandler,
                app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket))
        websocket_server.initialize_websockets_manager()
        self._websocket_thread = Thread(target=websocket_server.serve_forever)
        self._websocket_server = websocket_server
        self._websocket_thread.start()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        return '%s:%d' % (sock.getsockname()[0], self._config.WS_PORT) 
    def stop(self):
        self._websocket_server.shutdown()
        self._websocket_thread.join()
