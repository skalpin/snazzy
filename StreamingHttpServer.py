from http.server import BaseHTTPRequestHandler, HTTPServer
from StreamingHttpHandler import StreamingHttpHandler
import io
import sys
PY2 = sys.version_info.major == 2

class StreamingHttpServer(HTTPServer):
	def __init__(self, port, ws_port, camera, output):
		self.port = port
		self.ws_port = ws_port
		self.camera = camera
		self.output = output
		#self.flash = flash
		self.recording = True
		#self.capturing = False
		self.color = ''
		self.color_effect = (100, 150)
		self.session_images = []
		## Eurgh ... old-style classes ...
		if PY2:
			HTTPServer.__init__(self, ('', HTTP_PORT), StreamingHttpHandler)
		else:
			super(StreamingHttpServer, self).__init__(('', port), StreamingHttpHandler)

	def get_file(self, filename):
		with io.open(filename, 'r') as f:
			return f.read()

	def get_file_bytes(self, filename):
		with io.open(filename, 'rb') as f:
			return f.read()

	#def capture(self, image_name):
		#currentDir = os.getcwd()

		#img_path = "%s/%s.jpg" % (currentDir, image_name)
		#print('image path:' + img_path)
		#self.camera.capture(img_path, use_video_port=True)
		#image = util.process(img_path, assemble.get_height_each())
		#self.session_images.append(image)

	#def assemble(self):
		#filename = assemble.assemble(self.session_images)
		#printer.print_file(filename)
