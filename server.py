#!/usr/bin/env python

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
native_str = str
str = type('')

import sys
PY2 = sys.version_info.major == 2
import io
import os
import shutil
from subprocess import Popen, PIPE
from string import Template
from struct import Struct
from threading import Thread
from time import sleep, time
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from wsgiref.simple_server import make_server

from urlparse import parse_qs

import picamera
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

import assemble
import util
import printer
import flash

###########################################
# CONFIGURATION
WIDTH = 1280
HEIGHT = 960
FRAMERATE = 24
HTTP_PORT = 8082
WS_PORT = 8084
COLOR = u'#444'
BGCOLOR = u'#333'
JSMPEG_MAGIC = b'jsmp'
JSMPEG_HEADER = Struct(native_str('>4sHH'))
###########################################


class StreamingHttpHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/static/index.html')
            self.end_headers()
            return
        elif self.path.startswith('/static'):
            if self.path.endswith('.js'):
                content_type = 'application/javascript'
            elif self.path.endswith('.html'):
                content_type = 'text/html; charset=utf-8'
            content = self.server.get_file(self.path[1:])

        elif self.path.startswith('/preview'):
            params = parse_qs(self.path.split("?")[1])            
            self.server.color = params['color'][0]
            self.server.color_effects = None
            self.server.session_images = []
            if self.server.color == 'sepia':
                self.server.color_effects = (100, 155)
            elif self.server.color == 'bw':
                self.server.color_effects = (128, 128)
            self.server.camera.color_effects = self.server.color_effects
            self.server.camera.contrast = 20
            self.server.camera.sharpness = 20
            if self.server.recording == False:
                self.server.camera.start_recording(self.server.output, 'yuv')
                self.server.recording = True

            content_type = 'text/html; charset=utf-8'
            tpl = Template(self.server.get_file('static/preview.html'))

            content = tpl.safe_substitute(dict(
                ADDRESS='%s:%d' % (self.request.getsockname()[0], WS_PORT),
                WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR, BGCOLOR=BGCOLOR))           
        elif self.path == '/stop':
            print('stop recording called')
            if self.server.recording == True:
		        self.server.camera.stop_recording()
                        self.server.recording = False

            content_type = 'text/json; charset=utf-8'
            content = "{success: true}"
        elif self.path.startswith('/picture'):
            pic_number = self.path.split("/")[-1]
            if self.server.capturing == False:
                print('took picture')
                self.server.capturing = True
                self.server.capture(pic_number)
                self.server.capturing = False
                #self.server.flash.blink()
            if pic_number == '3':
                self.server.assemble()
            content_type = 'text/json; charset=utf-8'
            content = "{src : 'from_server.jpg'}"
        elif self.path.startswith('/settings'):
            params = parse_qs(self.path.split("?")[1])
            color_effect_params = params['color_effect']
            (u, v) = color_effect_params[0].split(",")
            (u, v) = (int(u), int(v))
            self.server.color_effects = (u, v)

            contrast_param = params['contrast'][0]
            self.server.contrast = int(contrast_param)

            brightness_param = params['brightness'][0]
            self.server.brightness = int(brightness_param)

            self.server.camera.stop_recording()

            self.server.camera.color_effects = self.server.color_effects
            self.server.camera.brightness = self.server.brightness
            self.server.camera.contrast = self.server.contrast

            self.server.camera.start_recording(self.server.output, 'yuv')

            #print(str(self.server.camera.color_effects))
            content_type = 'text/json; charset=utf-8'
            content = "{'success' : true, 'color_effect' : %d, %d}" % (u,v)
        else:
            self.send_error(404, 'File not found')
            return
        content = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', len(content))
        self.send_header('Last-Modified', self.date_time_string(time()))
        self.end_headers()
        if self.command == 'GET':
            self.wfile.write(content)


class StreamingHttpServer(HTTPServer):
    def __init__(self, camera, output, flash):
        self.camera = camera
        self.output = output
        self.flash = flash
        self.recording = False
        self.capturing = False
        self.color = ''
        self.color_effect = (100, 150)
        self.session_images = []
        # Eurgh ... old-style classes ...
        if PY2:
            HTTPServer.__init__(self, ('', HTTP_PORT), StreamingHttpHandler)
        else:
            super(StreamingHttpServer, self).__init__(
                    ('', HTTP_PORT), StreamingHttpHandler)

    def get_file(self, filename):
        with io.open(filename, 'r') as f:
            return f.read()

    def capture(self, image_name):
        currentDir = os.getcwd()

        img_path = "%s/%s.jpg" % (currentDir, image_name)
        print('image path:' + img_path)
        self.camera.capture(img_path, use_video_port=True)
        image = util.process(img_path, assemble.get_height_each())
        self.session_images.append(image)

    def assemble(self):
        filename = assemble.assemble(self.session_images)
        printer.print_file(filename)


class StreamingWebSocket(WebSocket):
    def opened(self):
        self.send(JSMPEG_HEADER.pack(JSMPEG_MAGIC, WIDTH, HEIGHT), binary=True)


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
    led_flash = flash.Flash()

    led_flash.on()
    print('Initializing camera')
    with picamera.PiCamera() as camera:
        camera.resolution = (WIDTH, HEIGHT)
        camera.framerate = FRAMERATE
        sleep(1) # camera warm-up time
        print('Initializing websockets server on port %d' % WS_PORT)
        websocket_server = make_server(
            '', WS_PORT,
            server_class=WSGIServer,
            handler_class=WebSocketWSGIRequestHandler,
            app=WebSocketWSGIApplication(handler_cls=StreamingWebSocket))
        websocket_server.initialize_websockets_manager()
        websocket_thread = Thread(target=websocket_server.serve_forever)
        print('Initializing HTTP server on port %d' % HTTP_PORT)
        
        output = BroadcastOutput(camera)

        http_server = StreamingHttpServer(camera, output, led_flash)
        http_thread = Thread(target=http_server.serve_forever)
        print('Initializing broadcast thread')

        broadcast_thread = BroadcastThread(output.converter, websocket_server)
        print('Starting recording')
        #camera.start_recording(output, 'yuv')
        try:
            print('Starting websockets thread')
            websocket_thread.start()
            print('Starting HTTP server thread')
            http_thread.start()
            print('Starting broadcast thread')
            broadcast_thread.start()
            while True:
                #camera.wait_recording(1)
                pass
        except KeyboardInterrupt:
            pass
        finally:
            print('Turning off flash')
            led_flash.off()

            print('Stopping recording')
            camera.stop_recording()
            print('Waiting for broadcast thread to finish')
            broadcast_thread.join()
            print('Shutting down HTTP server')
            http_server.shutdown()
            print('Shutting down websockets server')
            websocket_server.shutdown()
            print('Waiting for HTTP server thread to finish')
            http_thread.join()
            print('Waiting for websockets thread to finish')
            websocket_thread.join()


if __name__ == '__main__':
    main()
