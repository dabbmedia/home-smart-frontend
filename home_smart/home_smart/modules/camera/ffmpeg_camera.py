import os, sys, subprocess
import ffmpeg as ff
from datetime import datetime
from .camera import Camera

class FfmpegCamera(Camera):
    video_source = 0

    def __init__(self):
        print("****ffmpeg camera class constructed****")
        super().__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        print("getting frame w ffmpeg")

        while True:
            try:
                out, _ = (
                    ff
                    .input('/dev/video0')
                    .filter('select', 'gte(n,{})'.format(1))
                    .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
                    .run(capture_stdout=True)
                )
                # out = ffmpeg.output(out_filename, pix_fmt='yuv420p')
                yield out
            except OSError as e:
                # print >>sys.stderr, "Execution failed:", e
                print ("Execution failed: %s", e)