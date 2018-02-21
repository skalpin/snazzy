from write_info import write_info
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep, time
from urllib.parse import parse_qs
from string import Template

WIDTH = 1280
HEIGHT = 960
COLOR = u'#444'
BGCOLOR = u'#333'

class StreamingHttpHandler(BaseHTTPRequestHandler):
	def do_HEAD(self):
		self.do_GET()
	def do_GET(self):
		if self.path == '/':
			write_info(5, "get /")
			self.send_response(301)
			self.send_header('Location', '/static/index.html')
			self.end_headers()
			return
		elif self.path.startswith('/static'):
			write_info(5, "get /static")
			if self.path.endswith('.js'):
				content_type = 'application/javascript'
				content = self.server.get_file(self.path[1:]).encode('utf-8')
			elif self.path.endswith('.html'):
				content_type = 'text/html; charset=utf-8'
				content = self.server.get_file(self.path[1:]).encode('utf-8')
			elif self.path.endswith('.css'):
				content_type = 'text/css; charset=utf-8'
				content = self.server.get_file(self.path[1:]).encode('utf-8')
			elif self.path.endswith('.woff2'):
				content_type = 'font/woff2'
				content = self.server.get_file_bytes(self.path[1:])
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
				ADDRESS='%s:%d' % (self.request.getsockname()[0], self.server.ws_port),
				WIDTH=WIDTH, HEIGHT=HEIGHT, COLOR=COLOR, BGCOLOR=BGCOLOR)).encode('utf-8')
		elif self.path == '/stop':
			print('stop recording called')
			if self.server.recording == True:
				self.server.camera.stop_recording()
				self.server.recording = False

			content_type = 'text/json; charset=utf-8'
			content = "{success: true}".encode('utf-8')
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
			content = "{src : 'from_server.jpg'}".encode('utf-8')
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
			content.encode('utf-8')
		else:
			self.send_error(404, 'File not found')
			return
		#content = content.encode('utf-8')
		self.send_response(200)
		self.send_header('Content-Type', content_type)
		self.send_header('Content-Length', len(content))
		self.send_header('Last-Modified', self.date_time_string(time()))
		self.end_headers()
		if self.command == 'GET':
			self.wfile.write(content)
