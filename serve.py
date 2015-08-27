from flask import Flask, render_template
import picamera
import time
import os

app = Flask(__name__)
static_dir = 'static'
seq = [1,2,3]
width = 1024
height = 768


@app.route("/", methods=['GET'])
def hello():
	templateData = {'pic_path' : []}
	return render_template("index.html", **templateData)

@app.route("/", methods=['POST'])
def take_pic():
	try:
		camera = picamera.PiCamera();
		camera.vflip = True
		camera.resolution = (width, height)
		camera.start_preview();
		time.sleep(1)
	
		all_paths = []
		for i in seq:
			pic_path = static_dir + '/foo' + str(int(time.time())) + '.jpg'
			time.sleep(1)
			camera.capture(pic_path)
			all_paths.append(pic_path)
	except:
		pass
	finally:
		camera.close()

	templateData = {'pic_path' : all_paths}
	return render_template("index.html", **templateData)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80, debug=True)
