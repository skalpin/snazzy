from flask import Flask, render_template, request, redirect
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
    wsAddress = factory.WebSocket().start()
    session_images = []
    return render_template('preview2.html', Config=Config, ADDRESS=wsAddress)

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

@app.route("/preview/stop")
def preview_stop():
    factory.WebSocket().stop()
    return redirect('/')

@app.route("/<path:path>")
def get(path):
    return app.send_static_file(path)
