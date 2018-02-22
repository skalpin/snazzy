from subprocess import Popen, PIPE
import io
import os

class BroadcastOutput(object):
	def __init__(self, config):
		print('Spawning background conversion process')
		self.converter = Popen([
			'avconv',
			'-f', 'rawvideo',
			'-pix_fmt', 'yuv420p',
			'-s', '%dx%d' % (config.WIDTH, config.HEIGHT),
			'-r', str(float(config.FRAMERATE)),
			'-i', '-',
			'-f', 'mpeg1video',
			'-b', '800k',
			'-r', str(float(config.FRAMERATE)),
			'-'],
			stdin=PIPE, stdout=PIPE, stderr=io.open(os.devnull, 'wb'),
			shell=False, close_fds=True)

	def write(self, b):
		self.converter.stdin.write(b)

	def flush(self):
		print('Waiting for background conversion process to exit')
		#self.converter.stdin.close()
		#self.converter.wait()
