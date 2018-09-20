#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, Response
from Factory import Factory
import Config

app = Flask(__name__, static_url_path='/static')

Factory.Flash().on();

@app.route("/")
def root():
	return app.send_static_file('index.html')

@app.route("/preview")
def preview():
	color = request.args.get('color')
	Factory.Camera().new_session(color)
	return render_template('preview.html', Config=Config)

@app.route("/picture/<pic_number>")
def picture(pic_number):
	print('taking picture')
	Factory.Camera().capture(pic_number)
	#self.server.flash.blink()
	if pic_number == '3':
		Factory.Camera().assemble()
	return ''

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	cam = Factory.Camera()
	cam.start_camera_thread()
	return Response(gen(cam), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/preview/stop")
def preview_stop():
	return redirect('/')

@app.route("/<path:path>")
def get(path):
	return app.send_static_file(path)

if __name__ == '__main__':
	app.run(host='0.0.0.0', threaded=True)
