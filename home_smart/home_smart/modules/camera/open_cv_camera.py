import os
from datetime import datetime
import numpy as np
import cv2
from .camera import Camera
from multiprocessing import Process

class OpenCvCamera(Camera):
    def __init__(self):
        super().__init__()

    @staticmethod
    def frames():
        # opened camera after sudo chmod 0777 /dev/video0
        # camera = cv2.VideoCapture(0 + cv2.CAP_FFMPEG)
        camera = cv2.VideoCapture(-1)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera (check permissions).')

        previous_frame = np.array([0, 1])

        while True:
            # read current frame
            _, img = camera.read()

            if (previous_frame.size > 8):
                # prev_frame_bw = cv2.cvtColor(previous_frame, cv2.COLOR_RGB2GRAY)
                # prev_frame_bw = cv2.GaussianBlur(previous_frame, (25, 25), 0)

                # cur_frame_bw = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                # cur_frame_bw = cv2.GaussianBlur(img, (25, 25), 0)

                # calculate diff as a float
                delta = cv2.norm(previous_frame, img)
                
                if delta > 6000.0:
                    # event occurred
                    # print("motion may have occurred")
                    img_name = "/var/www/home_smart/home_smart/tmp/motion_maybe_" + datetime.now().strftime("_%Y_%m_%d_%H_%M_%S") + ".jpg"
                    # result = cv2.imwrite(img_name, img)
                    p = Process(target=cv2.imwrite, args=(img_name,img))
                    p.start()
                    p.join()

            previous_frame = img

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()