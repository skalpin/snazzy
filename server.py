#!/usr/bin/env python

#from __future__ import (
	#unicode_literals,
	#absolute_import,
	#print_function,
	#division,
	#)
#native_str = str
#str = type('')

#import sys
#PY2 = sys.version_info.major == 3
import io
import os
#import shutil
from subprocess import Popen, PIPE
#from string import Template
#from struct import Struct
from threading import Thread
from time import sleep, time
#from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
#from wsgiref.simple_server import make_server

#from urlparse import parse_qs

import picamera
#from ws4py.websocket import WebSocket
#from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
#from ws4py.server.wsgiutils import WebSocketWSGIApplication

#import assemble
#import util
#import printer
#import flash

from StreamingHttpServer import StreamingHttpServer

###########################################
# CONFIGURATION
WIDTH = 1280
HEIGHT = 960
FRAMERATE = 24
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
#JSMPEG_MAGIC = b'jsmp'
#JSMPEG_HEADER = Struct(native_str('>4sHH'))
###########################################

#class StreamingWebSocket(WebSocket):
	#def opened(self):
		#self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)


class BroadcastOutput(object):
	def __init__(self, camera):
		print('Spawning background conversion process')
		self.converter = Popen([
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

	def write(self, b):
		self.converter.stdin.write(b)

	def flush(self):
		print('Waiting for background conversion process to exit')
		#self.converter.stdin.close()
		#self.converter.wait()


class BroadcastThread(Thread):
	def __init__(self, converter, websocket_server):
		super(BroadcastThread, self).__init__()
		self.converter = converter
		self.websocket_server = websocket_server

	def run(self):
		try:
			while True:
				buf = self.converter.stdout.read(512)
				if buf:
					self.websocket_server.manager.broadcast(buf, binary=True)
				elif self.converter.poll() is not None:
					break
		finally:
			self.converter.stdout.close()

def main():
	#led_flash = flash.Flash()

	#led_flash.on()
	print('Initializing camera')
	with picamera.PiCamera() as camera:
		camera.resolution = (WIDTH, HEIGHT)
		camera.framerate = FRAMERATE
		sleep(1) # camera warm-up time
		#print('Initializing websockets server on port %d' % WS_PORT)
		#websocket_server = make_server(
			#'', WS_PORT,
			#server_class=WSGIServer,
			#handler_class=WebSocketWSGIRequestHandler,
			#app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket))
		#websocket_server.initialize_websockets_manager()
		#websocket_thread = Thread(target=websocket_server.serve_forever)
		print('Initializing HTTP server on port %d' % HTTP_PORT)

		output = BroadcastOutput(camera)

		http_server = StreamingHttpServer(HTTP_PORT, camera, output)
		http_thread = Thread(target=http_server.serve_forever)
		#print('Initializing broadcast thread')

		#broadcast_thread = BroadcastThread(output.converter, websocket_server)
		print('Starting recording')
		camera.start_recording(output, 'yuv')
		#try:
			#print('Starting websockets thread')
			#websocket_thread.start()
		print('Starting HTTP server thread')
		http_thread.start()
		print('Starting broadcast thread')
		#broadcast_thread.start()
			#while True:
				##camera.wait_recording(1)
				#pass
		#except KeyboardInterrupt:
			#pass
		#finally:
			#print('Turning off flash')
			#led_flash.off()

			#print('Stopping recording')
			#camera.stop_recording()
		#print('Waiting for broadcast thread to finish')
		#broadcast_thread.join()
			#print('Shutting down HTTP server')
			#http_server.shutdown()
			#print('Shutting down websockets server')
			#websocket_server.shutdown()
		print('Waiting for HTTP server thread to finish')
		http_thread.join()
			#print('Waiting for websockets thread to finish')
			#websocket_thread.join()

if __name__ == '__main__':
	main()
