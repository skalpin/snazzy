import picamera
from time import sleep
from ResourceQueue import ResourceQueue
import os
import assemble

class Camera():
    def __init__(self, config):
        self._config = config
        print('init camera')
        camera = picamera.PiCamera()
        camera.resolution = (self._config.WIDTH, self._config.HEIGHT)
        camera.framerate = self._config.FRAMERATE
        sleep(1) # camera warm-up time
        self._camera = camera
        self._camera_queue = ResourceQueue('camera', self._camera)
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
    def release_camera(self):
        self._camera.__exit__(None, None, None)
        self._camera_queue.stop()
    def start_recording(self):
        self._camera_queue.add(lambda cam: cam.start_recording(output, 'yuv'))
    def stop_recording(self):
        self._camera_queue.add(lambda cam: cam.stop_recording())
    def capture_image(self, image_name):
        currentDir = os.getcwd()

        img_path = "%s/%s.jpg" % (currentDir, image_name)
        print('image path:' + img_path)
        #should maybe be done on queue
        self._camera.capture(img_path, use_video_port=True))
        return util.process(img_path, assemble.get_height_each())
    def assemble(self, session_images):
        filename = assemble.assemble(session_images)
        print('saved file ', filename)
        #printer.print_file(filename)
