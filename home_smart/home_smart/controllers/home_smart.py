# import cv2 as cv
from flask import (
    Blueprint, redirect, render_template, request
)
bp = Blueprint('home_smart', __name__)

@bp.route('/')
def index():
    return render_template('home_smart/index.html')
