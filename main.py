from flask import Flask, render_template, Response, request,redirect,url_for
from necklace_camera import NecklaceVideoCamera
from tshirt_camera import TshirtVideoCamera
from makeup_camera import MakeupVideoCamera
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

_red = 133
_green = 21
_blue = 21

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route("/get_rgb", methods=["POST"], strict_slashes=False)
def get_rgb():
    global _red,_green,_blue
    if request.method == "POST":
        red = int(request.form["r"])
        green = int(request.form["g"])
        blue = int(request.form["b"])

        if red == -1 and blue == -1 and green == -1:
            pass
        if red and blue and green:
            _red = red
            _blue = blue
            _green = green
    return render_template(url_for('index'))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
def makeup_gen(camera):
    while True:
        frame = camera.get_frame(_red,_blue,_green,0.5)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed_makeup')
def video_feed_makeup():
    return Response(makeup_gen(MakeupVideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_necklace')
def video_feed_necklace():
    return Response(gen(NecklaceVideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_tshirt')
def video_feed_tshirt():
    return Response(gen(TshirtVideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080, debug=True)
