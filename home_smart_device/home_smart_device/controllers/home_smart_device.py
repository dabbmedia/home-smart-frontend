# import cv2 as cv
from flask import (
    Blueprint, redirect, render_template, request, Response
)
import home_smart_device

bp = Blueprint('home_smart_device', __name__)

@bp.route('/')
def index():
    return render_template('home_smart_device/index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/video-feed', methods=('GET', 'POST'))
def video_feed():
    return Response(gen(home_smart_device.OpenCvCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
