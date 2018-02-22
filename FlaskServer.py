#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, Response
from Factory import Factory
import Config

app = Flask(__name__, static_url_path='/static')
session_images = []
factory = Factory()

@app.route("/")
def root():
	return app.send_static_file('index.html')

@app.route("/preview")
def preview():
	session_images = []
	return render_template('preview2.html', Config=Config)

@app.route("/picture/<pic_number>")
def picture(pic_number):
	if self.server.capturing == False:
		print('took picture')
		image = factory.Camera().capture(pic_number)
		session_images.append(image)
		#self.server.flash.blink()
	if pic_number == '3':
		factory.Camera().assemble(session_images)
		session_images = []

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(factory.Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/preview/stop")
def preview_stop():
	factory.WebSocket().stop()
	return redirect('/')

@app.route("/<path:path>")
def get(path):
	return app.send_static_file(path)

if __name__ == '__main__':
	app.run(host='0.0.0.0', threaded=True)
