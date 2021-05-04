# import cv2 as cv
from flask import (
    Blueprint, redirect, render_template, request
)
bp = Blueprint('home_smart', __name__)
print('routing home controller')
@bp.route('/')
def index():
    print('rendering home controller')
    return render_template('home_smart/index.html')
