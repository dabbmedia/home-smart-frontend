# 
# From:
# https://github.com/miguelgrinberg/flask-video-streaming/blob/master/base_camera.py
# 
import time
import threading
from .camera_event import CameraEvent

class Camera(object):
    thread = None
    frame = None
    last_access = 0
    event = CameraEvent()

    def __init__(self):
        if Camera.thread is None:
            Camera.last_access = time.time()

            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        Camera.event.wait()
        Camera.event.clear()

        return Camera.frame

    @staticmethod
    def frames():
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            Camera.frame = frame
            Camera.event.set()
            time.sleep(0)

            if time.time() - Camera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break

        Camera.thread = None