from flask import Flask, render_template, request, redirect
from Factory import Factory
import Config

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/test")
def test():
    return render_template('test.html', Config=Config)

@app.route("/preview")
def preview():
    wsAddress = Factory.WebSocketServer.start()
    return render_template('preview2.html', Config=Config, ADDRESS=wsAddress)

@app.route("/preview/stop")
def preview_stop():
    Factory.WebSocketServer.stop()
    return redirect('/')

@app.route("/<path:path>")
def get(path):
    return app.send_static_file(path)
